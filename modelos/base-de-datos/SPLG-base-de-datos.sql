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
-- Name: cash_box_kind_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.cash_box_kind_enum AS ENUM (
    'cash',
    'bank',
    'wallet'
);


--
-- Name: cash_category_direction_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.cash_category_direction_enum AS ENUM (
    'income',
    'expense'
);


--
-- Name: cash_category_system_code_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.cash_category_system_code_enum AS ENUM (
    'driver_settlement',
    'customer_payment',
    'commission_payment',
    'cash_surplus',
    'cash_shortage',
    'transfer_in',
    'transfer_out',
    'purchase',
    'fuel',
    'traffic_fine',
    'order_payment'
);


--
-- Name: cash_movement_direction_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.cash_movement_direction_enum AS ENUM (
    'in',
    'out'
);


--
-- Name: cash_movement_method_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.cash_movement_method_enum AS ENUM (
    'cash',
    'transfer',
    'card',
    'mercadopago',
    'check'
);


--
-- Name: cash_movement_reference_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.cash_movement_reference_type_enum AS ENUM (
    'manual',
    'session_opening',
    'session_closing',
    'driver_settlement',
    'customer_payment',
    'purchase_receipt',
    'fuel_load',
    'traffic_fine',
    'driver_liquidation',
    'box_transfer',
    'reversal',
    'order_payment'
);


--
-- Name: cash_session_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.cash_session_status_enum AS ENUM (
    'open',
    'closed'
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
-- Name: commission_entry_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.commission_entry_type_enum AS ENUM (
    'delivery_commission',
    'settlement_shortage',
    'traffic_fine',
    'adjustment',
    'legacy_balance'
);


--
-- Name: commission_rule_basis_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.commission_rule_basis_enum AS ENUM (
    'per_unit',
    'per_order',
    'percent_of_total'
);


--
-- Name: configurable_process_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.configurable_process_enum AS ENUM (
    'fleet_planner',
    'repurchase',
    'route_batching',
    'cylinder_recovery',
    'express_dispatch',
    'stock_control',
    'dispatch',
    'scheduled_tasks'
);


--
-- Name: coverage_zone_surcharge_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.coverage_zone_surcharge_type_enum AS ENUM (
    'fixed',
    'percentage'
);


--
-- Name: customer_account_entry_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.customer_account_entry_type_enum AS ENUM (
    'sale_charge',
    'payment',
    'credit_note',
    'debit_note'
);


--
-- Name: customer_account_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.customer_account_status_enum AS ENUM (
    'active',
    'blocked',
    'closed'
);


--
-- Name: customer_account_tax_condition_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.customer_account_tax_condition_enum AS ENUM (
    'registered',
    'monotax',
    'exempt',
    'final_consumer'
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
-- Name: driver_liquidation_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.driver_liquidation_status_enum AS ENUM (
    'draft',
    'approved',
    'paid',
    'voided'
);


--
-- Name: driver_settlement_difference_resolution_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.driver_settlement_difference_resolution_enum AS ENUM (
    'none',
    'charged_to_driver',
    'absorbed'
);


--
-- Name: driver_settlement_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.driver_settlement_status_enum AS ENUM (
    'open',
    'submitted',
    'approved'
);


--
-- Name: employee_attendance_source_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.employee_attendance_source_enum AS ENUM (
    'panel',
    'driver_app'
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
-- Name: employee_leave_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.employee_leave_status_enum AS ENUM (
    'requested',
    'approved',
    'rejected',
    'cancelled'
);


--
-- Name: employee_leave_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.employee_leave_type_enum AS ENUM (
    'vacation',
    'sick',
    'work_accident',
    'study',
    'marriage',
    'birth',
    'bereavement',
    'unpaid',
    'suspension',
    'unjustified_absence',
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
-- Name: fuel_payment_method_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.fuel_payment_method_enum AS ENUM (
    'cash_box',
    'driver_cash',
    'card',
    'fuel_account'
);


--
-- Name: fuel_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.fuel_type_enum AS ENUM (
    'diesel',
    'gasoline',
    'cng',
    'lpg'
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
    'driver',
    'employee'
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
    'transfer',
    'account'
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
    'online',
    'account'
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
-- Name: payment_refund_kind_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.payment_refund_kind_enum AS ENUM (
    'full',
    'express_surcharge'
);


--
-- Name: payment_refund_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.payment_refund_status_enum AS ENUM (
    'pending',
    'succeeded',
    'failed'
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
-- Name: plan_document_kind_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.plan_document_kind_enum AS ENUM (
    'insurance',
    'vtv',
    'hazmat_vehicle_permit',
    'driver_license',
    'hazmat_driver_course',
    'psychophysical',
    'art_coverage',
    'service',
    'generic'
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
-- Name: tire_event_type_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.tire_event_type_enum AS ENUM (
    'mount',
    'unmount',
    'rotate',
    'retread',
    'retire'
);


--
-- Name: tire_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.tire_status_enum AS ENUM (
    'in_stock',
    'mounted',
    'retired'
);


--
-- Name: traffic_fine_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.traffic_fine_status_enum AS ENUM (
    'pending',
    'appealed',
    'paid',
    'voided'
);


--
-- Name: truck_load_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.truck_load_status_enum AS ENUM (
    'loading',
    'on_route',
    'returned',
    'closed',
    'closed_with_difference',
    'cancelled'
);


--
-- Name: vehicle_accident_status_enum; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.vehicle_accident_status_enum AS ENUM (
    'reported',
    'under_review',
    'repairing',
    'closed'
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
-- Name: cobro_de_cuenta_maximo(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.cobro_de_cuenta_maximo() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       DECLARE v_deuda numeric;
       BEGIN
         IF current_setting('splg.bypass_saldos', true) = 'on' THEN RETURN NEW; END IF;
         SELECT coalesce(sum(CASE WHEN "type" IN ('sale_charge', 'debit_note') THEN "amount" ELSE -"amount" END), 0) INTO v_deuda
           FROM "customer_account_entry" WHERE "account_id" = NEW."account_id";
         IF NEW."amount" > v_deuda THEN
           RAISE EXCEPTION 'El cobro (%) supera la deuda de la cuenta (%)', NEW."amount", v_deuda
             USING ERRCODE = '23514', CONSTRAINT = 'CHK_customer_account_entry_cobro_mayor_a_la_deuda';
         END IF;
         RETURN NEW;
       END $$;


--
-- Name: employee_leave_no_overlap(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.employee_leave_no_overlap() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
      BEGIN
        IF NEW."status" IN ('requested', 'approved') THEN
          PERFORM pg_advisory_xact_lock(hashtext('employee_leave'), hashtext(NEW."employee_id"::text));
          IF EXISTS (
            SELECT 1 FROM "employee_leave" l
            WHERE l."employee_id" = NEW."employee_id"
              AND l."leave_id" <> NEW."leave_id"
              AND l."status" IN ('requested', 'approved')
              AND l."start_date" <= NEW."end_date"
              AND l."end_date" >= NEW."start_date"
          ) THEN
            RAISE EXCEPTION 'La licencia se superpone con otra del mismo empleado'
              USING ERRCODE = '23P01';
          END IF;
        END IF;
        RETURN NEW;
      END;
      $$;


--
-- Name: es_cuil_valido(text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.es_cuil_valido(cuil text) RETURNS boolean
    LANGUAGE sql IMMUTABLE PARALLEL SAFE
    AS $$
         SELECT es_cuit_valido(cuil) AND left(cuil, 2) IN ('20', '23', '24', '27')
       $$;


--
-- Name: es_cuit_valido(text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.es_cuit_valido(cuit text) RETURNS boolean
    LANGUAGE sql IMMUTABLE PARALLEL SAFE
    AS $_$
         SELECT CASE
           WHEN cuit IS NULL OR cuit !~ '^(20|23|24|27|30|33|34)[0-9]{9}$' THEN false
           ELSE (
             SELECT CASE WHEN r = 0 THEN 0 ELSE 11 - r END
               FROM (
                 SELECT mod(sum(substr(cuit, i, 1)::int * (ARRAY[5,4,3,2,7,6,5,4,3,2])[i]), 11) AS r
                   FROM generate_series(1, 10) AS i
               ) AS s
           ) = substr(cuit, 11, 1)::int
         END
       $_$;


--
-- Name: fabricacion_de_envase_no_futura(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.fabricacion_de_envase_no_futura() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       BEGIN
         IF current_setting('splg.bypass_reglas', true) = 'on' THEN RETURN NEW; END IF;
         IF NEW."manufactured_at" IS NOT NULL
            AND (TG_OP = 'INSERT' OR NEW."manufactured_at" IS DISTINCT FROM OLD."manufactured_at")
            AND NEW."manufactured_at" > now() + interval '5 minutes' THEN
           RAISE EXCEPTION 'La fecha de fabricación del envase (%) es futura', NEW."manufactured_at"
             USING ERRCODE = '23514', CONSTRAINT = 'CHK_cylinder_fabricacion_futura';
         END IF;
         RETURN NEW;
       END $$;


--
-- Name: libro_de_solo_agregar(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.libro_de_solo_agregar() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
      BEGIN
        IF TG_OP = 'DELETE' AND pg_trigger_depth() > 1 THEN
          RETURN OLD;
        END IF;
        IF TG_TABLE_NAME = 'commission_entry' AND TG_OP = 'UPDATE'
           AND (to_jsonb(NEW) - 'liquidation_id') = (to_jsonb(OLD) - 'liquidation_id') THEN
          RETURN NEW;
        END IF;
        RAISE EXCEPTION '% es un libro de sólo agregar: no se modifican ni se borran asientos', TG_TABLE_NAME;
      END;
      $$;


--
-- Name: odometro_de_carga_monotono(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.odometro_de_carga_monotono() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       DECLARE v_anterior integer; v_siguiente integer;
       BEGIN
         IF current_setting('splg.bypass_reglas', true) = 'on' THEN RETURN NEW; END IF;
         IF NEW."deletedAt" IS NOT NULL OR NEW."odometer_correction_note" IS NOT NULL THEN RETURN NEW; END IF;
         SELECT "odometer_km" INTO v_anterior FROM "fuel_load"
           WHERE "car_id" = NEW."car_id" AND "deletedAt" IS NULL AND "fuel_load_id" <> NEW."fuel_load_id" AND "loaded_at" <= NEW."loaded_at"
           ORDER BY "loaded_at" DESC, "odometer_km" DESC LIMIT 1;
         SELECT "odometer_km" INTO v_siguiente FROM "fuel_load"
           WHERE "car_id" = NEW."car_id" AND "deletedAt" IS NULL AND "fuel_load_id" <> NEW."fuel_load_id" AND "loaded_at" > NEW."loaded_at"
           ORDER BY "loaded_at" ASC, "odometer_km" ASC LIMIT 1;
         IF (v_anterior IS NOT NULL AND NEW."odometer_km" < v_anterior)
            OR (v_siguiente IS NOT NULL AND NEW."odometer_km" > v_siguiente) THEN
           RAISE EXCEPTION 'El kilometraje de la carga (%) no encaja entre el de la carga anterior (%) y el de la siguiente (%)', NEW."odometer_km", v_anterior, v_siguiente
             USING ERRCODE = '23514', CONSTRAINT = 'CHK_fuel_load_odometro_monotono';
         END IF;
         RETURN NEW;
       END $$;


--
-- Name: odometro_de_neumatico_monotono(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.odometro_de_neumatico_monotono() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       DECLARE v_ultimo integer;
       BEGIN
         IF current_setting('splg.bypass_reglas', true) = 'on' THEN RETURN NEW; END IF;
         IF NEW."car_id" IS NULL THEN RETURN NEW; END IF;
         SELECT max("odometer_km") INTO v_ultimo FROM "tire_event" WHERE "tire_id" = NEW."tire_id" AND "car_id" = NEW."car_id";
         IF v_ultimo IS NOT NULL AND NEW."odometer_km" < v_ultimo THEN
           RAISE EXCEPTION 'El kilometraje del movimiento (%) es menor que el último del neumático en el vehículo (%)', NEW."odometer_km", v_ultimo
             USING ERRCODE = '23514', CONSTRAINT = 'CHK_tire_event_odometro_monotono';
         END IF;
         RETURN NEW;
       END $$;


--
-- Name: odometro_de_tarea_monotono(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.odometro_de_tarea_monotono() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       DECLARE v_anterior integer; v_siguiente integer;
       BEGIN
         IF current_setting('splg.bypass_reglas', true) = 'on' THEN RETURN NEW; END IF;
         IF NEW."status" <> 'done' OR NEW."odometer_km" IS NULL OR NEW."car_id" IS NULL OR NEW."performed_at" IS NULL THEN RETURN NEW; END IF;
         SELECT "odometer_km" INTO v_anterior FROM "maintenance_task"
           WHERE "car_id" = NEW."car_id" AND "status" = 'done' AND "odometer_km" IS NOT NULL AND "task_id" <> NEW."task_id" AND "performed_at" <= NEW."performed_at"
           ORDER BY "performed_at" DESC, "odometer_km" DESC LIMIT 1;
         SELECT "odometer_km" INTO v_siguiente FROM "maintenance_task"
           WHERE "car_id" = NEW."car_id" AND "status" = 'done' AND "odometer_km" IS NOT NULL AND "task_id" <> NEW."task_id" AND "performed_at" > NEW."performed_at"
           ORDER BY "performed_at" ASC, "odometer_km" ASC LIMIT 1;
         IF (v_anterior IS NOT NULL AND NEW."odometer_km" < v_anterior)
            OR (v_siguiente IS NOT NULL AND NEW."odometer_km" > v_siguiente) THEN
           RAISE EXCEPTION 'El kilometraje de la tarea (%) no encaja entre el de la anterior (%) y el de la siguiente (%)', NEW."odometer_km", v_anterior, v_siguiente
             USING ERRCODE = '23514', CONSTRAINT = 'CHK_maintenance_task_odometro_monotono';
         END IF;
         RETURN NEW;
       END $$;


--
-- Name: payment_estado_no_retrocede(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.payment_estado_no_retrocede() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       BEGIN
         IF OLD.status = NEW.status
            OR OLD.status = 'pending'
            OR (OLD.status = 'approved' AND NEW.status = 'refunded') THEN
           RETURN NEW;
         END IF;
         RAISE EXCEPTION 'El estado del pago no puede pasar de % a %', OLD.status, NEW.status
           USING ERRCODE = '23514', CONSTRAINT = 'CHK_payment_estado_no_retrocede';
       END $$;


--
-- Name: rendicion_sin_fecha_futura(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.rendicion_sin_fecha_futura() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       BEGIN
         IF current_setting('splg.bypass_reglas', true) = 'on' THEN RETURN NEW; END IF;
         IF NEW."business_date" > (now() AT TIME ZONE 'America/Argentina/Buenos_Aires')::date THEN
           RAISE EXCEPTION 'No se abre la rendición de un día futuro (%)', NEW."business_date"
             USING ERRCODE = '23514', CONSTRAINT = 'CHK_driver_settlement_fecha_futura';
         END IF;
         RETURN NEW;
       END $$;


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


--
-- Name: transicion_de_estado_claims(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.transicion_de_estado_claims() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       BEGIN
         IF OLD."status" IS NOT DISTINCT FROM NEW."status"
            OR current_setting('splg.bypass_transiciones', true) = 'on'
            OR (OLD."status"::text || '>' || NEW."status"::text) = ANY (ARRAY['in_process>rejected', 'in_process>resolved', 'pending>in_process', 'pending>rejected', 'pending>resolved', 'rejected>in_process', 'resolved>in_process']) THEN
           RETURN NEW;
         END IF;
         RAISE EXCEPTION 'El reclamo no puede pasar de % a %', OLD."status", NEW."status"
           USING ERRCODE = '23514', CONSTRAINT = 'CHK_claims_transicion_de_estado';
       END $$;


--
-- Name: transicion_de_estado_customer_account(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.transicion_de_estado_customer_account() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       BEGIN
         IF OLD."status" IS NOT DISTINCT FROM NEW."status"
            OR current_setting('splg.bypass_transiciones', true) = 'on'
            OR (OLD."status"::text || '>' || NEW."status"::text) = ANY (ARRAY['active>blocked', 'active>closed', 'blocked>active', 'blocked>closed', 'closed>active']) THEN
           RETURN NEW;
         END IF;
         RAISE EXCEPTION 'La cuenta corriente no puede pasar de % a %', OLD."status", NEW."status"
           USING ERRCODE = '23514', CONSTRAINT = 'CHK_customer_account_transicion_de_estado';
       END $$;


--
-- Name: transicion_de_estado_cylinder(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.transicion_de_estado_cylinder() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       BEGIN
         IF OLD."state" IS NOT DISTINCT FROM NEW."state"
            OR current_setting('splg.bypass_transiciones', true) = 'on'
            OR (OLD."state"::text || '>' || NEW."state"::text) = ANY (ARRAY['dispatched>in_depot', 'dispatched>with_customer', 'empty_returned>in_depot', 'empty_returned>retired', 'filled>dispatched', 'filled>in_depot', 'in_depot>filled', 'in_depot>retired', 'with_customer>empty_returned']) THEN
           RETURN NEW;
         END IF;
         RAISE EXCEPTION 'El envase no puede pasar de % a %', OLD."state", NEW."state"
           USING ERRCODE = '23514', CONSTRAINT = 'CHK_cylinder_transicion_de_estado';
       END $$;


--
-- Name: transicion_de_estado_driver_liquidation(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.transicion_de_estado_driver_liquidation() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       BEGIN
         IF OLD."status" IS NOT DISTINCT FROM NEW."status"
            OR current_setting('splg.bypass_transiciones', true) = 'on'
            OR (OLD."status"::text || '>' || NEW."status"::text) = ANY (ARRAY['approved>paid', 'approved>voided', 'draft>approved', 'draft>voided', 'paid>approved']) THEN
           RETURN NEW;
         END IF;
         RAISE EXCEPTION 'La liquidación no puede pasar de % a %', OLD."status", NEW."status"
           USING ERRCODE = '23514', CONSTRAINT = 'CHK_driver_liquidation_transicion_de_estado';
       END $$;


--
-- Name: transicion_de_estado_driver_settlement(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.transicion_de_estado_driver_settlement() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       BEGIN
         IF OLD."status" IS NOT DISTINCT FROM NEW."status"
            OR current_setting('splg.bypass_transiciones', true) = 'on'
            OR (OLD."status"::text || '>' || NEW."status"::text) = ANY (ARRAY['open>submitted', 'submitted>approved', 'submitted>open']) THEN
           RETURN NEW;
         END IF;
         RAISE EXCEPTION 'La rendición no puede pasar de % a %', OLD."status", NEW."status"
           USING ERRCODE = '23514', CONSTRAINT = 'CHK_driver_settlement_transicion_de_estado';
       END $$;


--
-- Name: transicion_de_estado_order(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.transicion_de_estado_order() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       BEGIN
         IF OLD."status" IS NOT DISTINCT FROM NEW."status"
            OR current_setting('splg.bypass_transiciones', true) = 'on'
            OR (OLD."status"::text || '>' || NEW."status"::text) = ANY (ARRAY['accepted>cancelled', 'accepted>on_the_way', 'accepted>pending', 'on_the_way>cancelled', 'on_the_way>delivered', 'on_the_way>pending', 'pending>accepted', 'pending>cancelled', 'reserved>cancelled', 'reserved>pending']) THEN
           RETURN NEW;
         END IF;
         RAISE EXCEPTION 'El pedido no puede pasar de % a %', OLD."status", NEW."status"
           USING ERRCODE = '23514', CONSTRAINT = 'CHK_order_transicion_de_estado';
       END $$;


--
-- Name: transicion_de_estado_order_dispatch_offer(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.transicion_de_estado_order_dispatch_offer() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       BEGIN
         IF OLD."status" IS NOT DISTINCT FROM NEW."status"
            OR current_setting('splg.bypass_transiciones', true) = 'on'
            OR (OLD."status"::text || '>' || NEW."status"::text) = ANY (ARRAY['accepted>rejected', 'offered>accepted', 'offered>expired', 'offered>rejected', 'offered>superseded']) THEN
           RETURN NEW;
         END IF;
         RAISE EXCEPTION 'La oferta de despacho no puede pasar de % a %', OLD."status", NEW."status"
           USING ERRCODE = '23514', CONSTRAINT = 'CHK_order_dispatch_offer_transicion_de_estado';
       END $$;


--
-- Name: transicion_de_estado_purchase_order(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.transicion_de_estado_purchase_order() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       BEGIN
         IF OLD."status" IS NOT DISTINCT FROM NEW."status"
            OR current_setting('splg.bypass_transiciones', true) = 'on'
            OR (OLD."status"::text || '>' || NEW."status"::text) = ANY (ARRAY['draft>cancelled', 'draft>sent', 'partially_received>closed_short', 'partially_received>partially_received', 'partially_received>received', 'partially_received>sent', 'received>partially_received', 'received>sent', 'sent>cancelled', 'sent>partially_received', 'sent>received']) THEN
           RETURN NEW;
         END IF;
         RAISE EXCEPTION 'La orden de compra no puede pasar de % a %', OLD."status", NEW."status"
           USING ERRCODE = '23514', CONSTRAINT = 'CHK_purchase_order_transicion_de_estado';
       END $$;


--
-- Name: transicion_de_estado_truck_load(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.transicion_de_estado_truck_load() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       BEGIN
         IF OLD."status" IS NOT DISTINCT FROM NEW."status"
            OR current_setting('splg.bypass_transiciones', true) = 'on'
            OR (OLD."status"::text || '>' || NEW."status"::text) = ANY (ARRAY['loading>cancelled', 'loading>on_route', 'on_route>returned', 'returned>closed', 'returned>closed_with_difference']) THEN
           RETURN NEW;
         END IF;
         RAISE EXCEPTION 'La carga del camión no puede pasar de % a %', OLD."status", NEW."status"
           USING ERRCODE = '23514', CONSTRAINT = 'CHK_truck_load_transicion_de_estado';
       END $$;


--
-- Name: verificar_existencia_contra_libro(uuid, uuid, public.stock_condition_enum); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.verificar_existencia_contra_libro(p_ubicacion uuid, p_garrafa uuid, p_condicion public.stock_condition_enum) RETURNS void
    LANGUAGE plpgsql
    AS $$
       DECLARE v_saldo bigint; v_libro bigint;
       BEGIN
         IF p_ubicacion IS NULL THEN RETURN; END IF;
         SELECT coalesce(sum("quantity"), 0) INTO v_saldo FROM "stock_balance"
           WHERE "location_id" = p_ubicacion AND "gas_cylinder_id" = p_garrafa AND "condition" = p_condicion;
         SELECT coalesce((SELECT sum("quantity") FROM "stock_movement"
                           WHERE "to_location_id" = p_ubicacion AND "gas_cylinder_id" = p_garrafa AND "to_condition" = p_condicion), 0)
              - coalesce((SELECT sum("quantity") FROM "stock_movement"
                           WHERE "from_location_id" = p_ubicacion AND "gas_cylinder_id" = p_garrafa AND "from_condition" = p_condicion), 0)
           INTO v_libro;
         IF v_saldo <> v_libro THEN
           RAISE EXCEPTION 'La existencia (%) no coincide con la suma de los movimientos de stock (%)', v_saldo, v_libro
             USING ERRCODE = '23514', CONSTRAINT = 'CHK_stock_balance_saldo_contra_libro';
         END IF;
       END $$;


--
-- Name: verificar_existencia_del_movimiento(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.verificar_existencia_del_movimiento() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       BEGIN
         IF current_setting('splg.bypass_saldos', true) = 'on' THEN RETURN NULL; END IF;
         PERFORM verificar_existencia_contra_libro(NEW."to_location_id", NEW."gas_cylinder_id", NEW."to_condition");
         PERFORM verificar_existencia_contra_libro(NEW."from_location_id", NEW."gas_cylinder_id", NEW."from_condition");
         RETURN NULL;
       END $$;


--
-- Name: verificar_existencia_del_saldo(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.verificar_existencia_del_saldo() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       BEGIN
         IF current_setting('splg.bypass_saldos', true) = 'on' THEN RETURN NULL; END IF;
         PERFORM verificar_existencia_contra_libro(NEW."location_id", NEW."gas_cylinder_id", NEW."condition");
         RETURN NULL;
       END $$;


--
-- Name: verificar_imputacion_de_cuenta(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.verificar_imputacion_de_cuenta() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       DECLARE v_asiento uuid; v_importe numeric; v_aplicado numeric;
       BEGIN
         IF current_setting('splg.bypass_saldos', true) = 'on' THEN RETURN NULL; END IF;
         FOREACH v_asiento IN ARRAY ARRAY[NEW."debit_entry_id", NEW."credit_entry_id"] LOOP
           SELECT "amount" INTO v_importe FROM "customer_account_entry" WHERE "entry_id" = v_asiento;
           SELECT coalesce(sum("amount"), 0) INTO v_aplicado FROM "customer_account_allocation"
             WHERE "debit_entry_id" = v_asiento OR "credit_entry_id" = v_asiento;
           IF v_aplicado > v_importe THEN
             RAISE EXCEPTION 'Lo imputado (%) supera el importe del asiento (%)', v_aplicado, v_importe
               USING ERRCODE = '23514', CONSTRAINT = 'CHK_customer_account_allocation_tope';
           END IF;
         END LOOP;
         RETURN NULL;
       END $$;


--
-- Name: verificar_saldo_de_caja(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.verificar_saldo_de_caja() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       DECLARE v_saldo numeric; v_libro numeric;
       BEGIN
         IF current_setting('splg.bypass_saldos', true) = 'on' THEN RETURN NULL; END IF;
         SELECT "balance" INTO v_saldo FROM "cash_box" WHERE "cash_box_id" = NEW."cash_box_id";
         IF NOT FOUND THEN RETURN NULL; END IF;
         SELECT coalesce(sum(CASE "direction" WHEN 'in' THEN "amount" ELSE -"amount" END), 0) INTO v_libro
           FROM "cash_movement" WHERE "cash_box_id" = NEW."cash_box_id";
         IF v_saldo <> v_libro THEN
           RAISE EXCEPTION 'El saldo de la caja (%) no coincide con la suma de sus movimientos (%)', v_saldo, v_libro
             USING ERRCODE = '23514', CONSTRAINT = 'CHK_cash_box_saldo_contra_libro';
         END IF;
         RETURN NULL;
       END $$;


--
-- Name: verificar_saldo_de_cuenta(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.verificar_saldo_de_cuenta() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
       DECLARE v_saldo numeric; v_libro numeric;
       BEGIN
         IF current_setting('splg.bypass_saldos', true) = 'on' THEN RETURN NULL; END IF;
         SELECT "balance" INTO v_saldo FROM "customer_account" WHERE "account_id" = NEW."account_id";
         IF NOT FOUND THEN RETURN NULL; END IF;
         SELECT coalesce(sum(CASE WHEN "type" IN ('sale_charge', 'debit_note') THEN "amount" ELSE -"amount" END), 0) INTO v_libro
           FROM "customer_account_entry" WHERE "account_id" = NEW."account_id";
         IF v_saldo <> v_libro THEN
           RAISE EXCEPTION 'El saldo de la cuenta corriente (%) no coincide con la suma de sus asientos (%)', v_saldo, v_libro
             USING ERRCODE = '23514', CONSTRAINT = 'CHK_customer_account_saldo_contra_libro';
         END IF;
         RETURN NULL;
       END $$;


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
    photo_key character varying(512),
    fuel_type public.fuel_type_enum,
    tank_capacity_liters numeric(6,2),
    CONSTRAINT "CHK_car_patente" CHECK (((car_patent IS NULL) OR ((car_patent)::text ~ '^([A-Z]{3}[0-9]{3}|[A-Z]{2}[0-9]{3}[A-Z]{2})$'::text)))
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
    unit_price numeric(10,2) NOT NULL,
    CONSTRAINT "CHK_cart_item_cantidad" CHECK (((quantity >= 1) AND (quantity <= 999))),
    CONSTRAINT "CHK_cart_item_precio" CHECK ((unit_price >= (0)::numeric))
);


--
-- Name: cash_box; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cash_box (
    cash_box_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    name character varying(80) NOT NULL,
    kind public.cash_box_kind_enum NOT NULL,
    balance numeric(14,2) DEFAULT '0'::numeric NOT NULL,
    requires_session boolean DEFAULT false NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    "deletedAt" timestamp with time zone,
    CONSTRAINT "CHK_cash_box_efectivo_no_negativo" CHECK (((kind <> 'cash'::public.cash_box_kind_enum) OR (balance >= (0)::numeric)))
);


--
-- Name: cash_category; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cash_category (
    category_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    name character varying(80) NOT NULL,
    direction public.cash_category_direction_enum NOT NULL,
    system_code public.cash_category_system_code_enum,
    is_active boolean DEFAULT true NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: cash_movement; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cash_movement (
    movement_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    cash_box_id uuid NOT NULL,
    session_id uuid,
    direction public.cash_movement_direction_enum NOT NULL,
    amount numeric(12,2) NOT NULL,
    category_id uuid NOT NULL,
    method public.cash_movement_method_enum DEFAULT 'cash'::public.cash_movement_method_enum NOT NULL,
    occurred_at timestamp with time zone DEFAULT now() NOT NULL,
    description character varying(255) NOT NULL,
    reference_type public.cash_movement_reference_type_enum DEFAULT 'manual'::public.cash_movement_reference_type_enum NOT NULL,
    reference_id uuid,
    reverses_movement_id uuid,
    created_by_user_id uuid NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_cash_movement_importe" CHECK ((amount > (0)::numeric))
);


--
-- Name: cash_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cash_session (
    session_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    cash_box_id uuid NOT NULL,
    status public.cash_session_status_enum DEFAULT 'open'::public.cash_session_status_enum NOT NULL,
    opened_at timestamp with time zone DEFAULT now() NOT NULL,
    opened_by_user_id uuid NOT NULL,
    opening_amount numeric(14,2) NOT NULL,
    closed_at timestamp with time zone,
    closed_by_user_id uuid,
    expected_amount numeric(14,2),
    counted_amount numeric(14,2),
    difference numeric(14,2),
    notes text,
    CONSTRAINT "CHK_cash_session_cierre_completo" CHECK (((status <> 'closed'::public.cash_session_status_enum) OR ((closed_by_user_id IS NOT NULL) AND (counted_amount IS NOT NULL) AND (expected_amount IS NOT NULL) AND (difference = (counted_amount - expected_amount))))),
    CONSTRAINT "CHK_cash_session_cierre_fecha" CHECK (((status = 'closed'::public.cash_session_status_enum) = (closed_at IS NOT NULL))),
    CONSTRAINT "CHK_cash_session_montos" CHECK (((opening_amount >= (0)::numeric) AND ((counted_amount IS NULL) OR (counted_amount >= (0)::numeric)))),
    CONSTRAINT "CHK_cash_session_periodo" CHECK (((closed_at IS NULL) OR (closed_at >= opened_at)))
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
    photo_key character varying(512),
    CONSTRAINT "CHK_claims_largo_de_textos" CHECK (((char_length((reason)::text) <= 120) AND (char_length(description) <= 1000) AND (("resolutionNote" IS NULL) OR (char_length("resolutionNote") <= 1000)))),
    CONSTRAINT "CHK_claims_textos" CHECK (((btrim((reason)::text) <> ''::text) AND (btrim(description) <> ''::text)))
);


--
-- Name: commission_entry; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.commission_entry (
    entry_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    employee_id uuid NOT NULL,
    delivery_id uuid,
    type public.commission_entry_type_enum NOT NULL,
    amount numeric(12,2) NOT NULL,
    order_id uuid,
    rule_id uuid,
    rule_snapshot jsonb,
    liquidation_id uuid,
    reference_id uuid,
    description character varying(255) NOT NULL,
    occurred_at timestamp with time zone DEFAULT now() NOT NULL,
    created_by_user_id uuid,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_commission_entry_importe" CHECK ((amount <> (0)::numeric)),
    CONSTRAINT "CHK_commission_entry_signo" CHECK ((((type <> 'delivery_commission'::public.commission_entry_type_enum) OR (amount > (0)::numeric)) AND ((type <> 'settlement_shortage'::public.commission_entry_type_enum) OR (amount < (0)::numeric))))
);


--
-- Name: commission_rule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.commission_rule (
    rule_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    employee_id uuid,
    gas_cylinder_id uuid,
    basis public.commission_rule_basis_enum NOT NULL,
    value numeric(10,4) NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    is_active boolean DEFAULT true NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_commission_rule_porcentaje" CHECK (((basis <> 'percent_of_total'::public.commission_rule_basis_enum) OR (value <= (100)::numeric))),
    CONSTRAINT "CHK_commission_rule_valor" CHECK ((value >= (0)::numeric)),
    CONSTRAINT "CHK_commission_rule_vigencia" CHECK (((valid_to IS NULL) OR (valid_to >= valid_from)))
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
    CONSTRAINT "CHK_coverage_zone_surcharge" CHECK ((((surcharge_type = 'fixed'::public.coverage_zone_surcharge_type_enum) AND (surcharge_value >= (0)::numeric)) OR ((surcharge_type = 'percentage'::public.coverage_zone_surcharge_type_enum) AND (surcharge_value >= (0)::numeric) AND (surcharge_value <= (100)::numeric)))),
    CONSTRAINT "CHK_coverage_zone_vigencia" CHECK (((valid_until IS NULL) OR (valid_from IS NULL) OR (valid_until > valid_from)))
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
    next_repurchase_estimate_at timestamp with time zone,
    CONSTRAINT "CHK_customer_consumo" CHECK (((avg_monthly_consumption_kg IS NULL) OR (avg_monthly_consumption_kg > (0)::numeric)))
);


--
-- Name: customer_account; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer_account (
    account_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    customer_user_id uuid NOT NULL,
    business_name character varying(120) NOT NULL,
    tax_id character varying(11),
    tax_condition public.customer_account_tax_condition_enum NOT NULL,
    credit_limit numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    payment_terms_days integer DEFAULT 30 NOT NULL,
    status public.customer_account_status_enum DEFAULT 'active'::public.customer_account_status_enum NOT NULL,
    balance numeric(14,2) DEFAULT '0'::numeric NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    "deletedAt" timestamp with time zone,
    CONSTRAINT "CHK_customer_account_cerrada_sin_saldo" CHECK (((status <> 'closed'::public.customer_account_status_enum) OR (balance = (0)::numeric))),
    CONSTRAINT "CHK_customer_account_cuit" CHECK (((tax_id IS NULL) OR public.es_cuit_valido((tax_id)::text))),
    CONSTRAINT "CHK_customer_account_limite" CHECK ((credit_limit >= (0)::numeric)),
    CONSTRAINT "CHK_customer_account_plazo" CHECK ((payment_terms_days > 0)),
    CONSTRAINT "CHK_customer_account_plazo_maximo" CHECK ((payment_terms_days <= 365))
);


--
-- Name: customer_account_allocation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer_account_allocation (
    allocation_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    account_id uuid NOT NULL,
    debit_entry_id uuid NOT NULL,
    credit_entry_id uuid NOT NULL,
    amount numeric(12,2) NOT NULL,
    CONSTRAINT "CHK_customer_account_allocation_importe" CHECK ((amount > (0)::numeric))
);


--
-- Name: customer_account_entry; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customer_account_entry (
    entry_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    account_id uuid NOT NULL,
    type public.customer_account_entry_type_enum NOT NULL,
    amount numeric(12,2) NOT NULL,
    order_id uuid,
    due_date date,
    payment_method character varying(20),
    cash_movement_id uuid,
    collected_by_delivery_id uuid,
    description character varying(255),
    occurred_at timestamp with time zone DEFAULT now() NOT NULL,
    created_by_user_id uuid,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_customer_account_entry_importe" CHECK ((amount > (0)::numeric)),
    CONSTRAINT "CHK_customer_account_entry_vencimiento" CHECK (((due_date IS NULL) OR (due_date >= ((occurred_at AT TIME ZONE 'America/Argentina/Buenos_Aires'::text))::date)))
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
    expires_at timestamp with time zone,
    CONSTRAINT "CHK_cylinder_cliente_segun_estado" CHECK (((state = 'with_customer'::public.cylinder_state_enum) = (current_customer_id IS NOT NULL))),
    CONSTRAINT "CHK_cylinder_garantia" CHECK ((deposit >= (0)::numeric)),
    CONSTRAINT "CHK_cylinder_serial" CHECK ((btrim((serial)::text) <> ''::text)),
    CONSTRAINT "CHK_cylinder_vencimiento" CHECK (((expires_at IS NULL) OR (manufactured_at IS NULL) OR (expires_at >= manufactured_at)))
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
    notes text,
    CONSTRAINT "CHK_cylinder_inspection_proxima" CHECK (((result = 'rejected'::public.cylinder_inspection_result_enum) OR (next_due_at IS NOT NULL))),
    CONSTRAINT "CHK_cylinder_inspection_vencimiento" CHECK (((next_due_at IS NULL) OR (next_due_at > inspected_at)))
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
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_cylinder_movement_cambio" CHECK (((from_state IS NULL) OR ((from_state)::text <> (to_state)::text) OR (note IS NOT NULL)))
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
    balance numeric(12,2) DEFAULT 0 NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now(),
    "deletedAt" timestamp with time zone,
    location public.geometry(Point,4326),
    "isEnabled" boolean DEFAULT true NOT NULL,
    "isAvailable" boolean DEFAULT false NOT NULL,
    CONSTRAINT "CHK_delivery_calificacion" CHECK (((calification IS NULL) OR ((calification >= (0)::double precision) AND (calification <= (5)::double precision))))
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
    logo_key character varying(512),
    CONSTRAINT "CHK_distributor_cuit" CHECK (((tax_id IS NULL) OR ((tax_id)::text ~ '^[0-9]{11}$'::text))),
    CONSTRAINT "CHK_distributor_slug" CHECK (((slug)::text ~ '^[a-z0-9]+(-[a-z0-9]+)*$'::text))
);


--
-- Name: document_sequence; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_sequence (
    distributor_id uuid NOT NULL,
    doc_type character varying(40) NOT NULL,
    last_number integer DEFAULT 0 NOT NULL,
    CONSTRAINT "CHK_document_sequence_valores" CHECK (((last_number >= 0) AND ((doc_type)::text ~ '^[a-z][a-z0-9_]{0,39}$'::text)))
);


--
-- Name: driver_liquidation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.driver_liquidation (
    liquidation_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    number integer NOT NULL,
    employee_id uuid NOT NULL,
    period_from date NOT NULL,
    period_to date NOT NULL,
    gross numeric(12,2) NOT NULL,
    deductions numeric(12,2) NOT NULL,
    net numeric(12,2) NOT NULL,
    status public.driver_liquidation_status_enum DEFAULT 'draft'::public.driver_liquidation_status_enum NOT NULL,
    approved_at timestamp with time zone,
    approved_by_user_id uuid,
    paid_at timestamp with time zone,
    paid_by_user_id uuid,
    voided_at timestamp with time zone,
    cash_movement_id uuid,
    created_by_user_id uuid NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_driver_liquidation_anulada" CHECK (((status = 'voided'::public.driver_liquidation_status_enum) = (voided_at IS NOT NULL))),
    CONSTRAINT "CHK_driver_liquidation_aprobada" CHECK (((status <> ALL (ARRAY['approved'::public.driver_liquidation_status_enum, 'paid'::public.driver_liquidation_status_enum])) OR (approved_at IS NOT NULL))),
    CONSTRAINT "CHK_driver_liquidation_montos" CHECK (((gross >= (0)::numeric) AND (deductions >= (0)::numeric) AND (net = (gross - deductions)))),
    CONSTRAINT "CHK_driver_liquidation_pagada" CHECK (((status = 'paid'::public.driver_liquidation_status_enum) = (paid_at IS NOT NULL))),
    CONSTRAINT "CHK_driver_liquidation_periodo" CHECK ((period_from <= period_to))
);


--
-- Name: driver_settlement; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.driver_settlement (
    settlement_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    delivery_id uuid NOT NULL,
    number integer NOT NULL,
    truck_load_id uuid,
    business_date date NOT NULL,
    status public.driver_settlement_status_enum DEFAULT 'open'::public.driver_settlement_status_enum NOT NULL,
    expected_cash numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    declared_cash numeric(12,2),
    driver_expenses numeric(12,2) DEFAULT '0'::numeric NOT NULL,
    difference numeric(12,2),
    difference_resolution public.driver_settlement_difference_resolution_enum,
    destination_cash_box_id uuid,
    cash_movement_id uuid,
    submitted_at timestamp with time zone,
    submitted_by_user_id uuid,
    approved_at timestamp with time zone,
    approved_by_user_id uuid,
    notes text,
    overdue_alerted_at timestamp with time zone,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_driver_settlement_aprobada" CHECK (((status = 'approved'::public.driver_settlement_status_enum) = (approved_at IS NOT NULL))),
    CONSTRAINT "CHK_driver_settlement_diferencia" CHECK (((difference IS NULL) OR (difference = ((declared_cash + driver_expenses) - expected_cash)))),
    CONSTRAINT "CHK_driver_settlement_montos" CHECK (((expected_cash >= (0)::numeric) AND (driver_expenses >= (0)::numeric) AND ((declared_cash IS NULL) OR (declared_cash >= (0)::numeric)))),
    CONSTRAINT "CHK_driver_settlement_presentada" CHECK (((status = 'open'::public.driver_settlement_status_enum) OR ((submitted_at IS NOT NULL) AND (declared_cash IS NOT NULL))))
);


--
-- Name: driver_settlement_collection; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.driver_settlement_collection (
    collection_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    settlement_id uuid NOT NULL,
    entry_id uuid NOT NULL,
    amount numeric(12,2) NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_driver_settlement_collection_importe" CHECK ((amount > (0)::numeric))
);


--
-- Name: driver_settlement_expense; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.driver_settlement_expense (
    expense_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    settlement_id uuid NOT NULL,
    category_id uuid NOT NULL,
    amount numeric(12,2) NOT NULL,
    description character varying(255),
    CONSTRAINT "CHK_driver_settlement_expense_importe" CHECK ((amount > (0)::numeric))
);


--
-- Name: driver_settlement_order; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.driver_settlement_order (
    settlement_order_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    settlement_id uuid NOT NULL,
    order_id uuid NOT NULL,
    amount numeric(12,2) NOT NULL,
    payment_method character varying(20) NOT NULL,
    CONSTRAINT "CHK_driver_settlement_order_importe" CHECK ((amount >= (0)::numeric))
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
    CONSTRAINT "CHK_employee_cbu" CHECK (((bank_cbu IS NULL) OR ((bank_cbu)::text ~ '^[0-9]{22}$'::text))),
    CONSTRAINT "CHK_employee_cuil" CHECK (((cuil IS NULL) OR public.es_cuil_valido((cuil)::text))),
    CONSTRAINT "CHK_employee_email" CHECK (((personal_email IS NULL) OR ((personal_email)::text ~* '^[^@[:space:]]+@[^@[:space:]]+[.][^@[:space:]]+$'::text))),
    CONSTRAINT "CHK_employee_nacimiento" CHECK (((birth_date IS NULL) OR (birth_date < hire_date))),
    CONSTRAINT "CHK_employee_status_termination" CHECK (((status = 'terminated'::public.employee_status_enum) = (termination_date IS NOT NULL))),
    CONSTRAINT "CHK_employee_termination_date" CHECK (((termination_date IS NULL) OR (termination_date >= hire_date)))
);


--
-- Name: employee_attendance; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employee_attendance (
    attendance_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    employee_id uuid NOT NULL,
    work_date date NOT NULL,
    check_in_at timestamp with time zone NOT NULL,
    check_out_at timestamp with time zone,
    source public.employee_attendance_source_enum NOT NULL,
    recorded_by_user_id uuid,
    notes text,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_employee_attendance_period" CHECK (((check_out_at IS NULL) OR (check_out_at > check_in_at)))
);


--
-- Name: employee_leave; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.employee_leave (
    leave_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    employee_id uuid NOT NULL,
    type public.employee_leave_type_enum NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    days integer NOT NULL,
    status public.employee_leave_status_enum DEFAULT 'requested'::public.employee_leave_status_enum NOT NULL,
    reason text,
    rejection_reason text,
    requested_by_user_id uuid,
    decided_by_user_id uuid,
    decided_at timestamp with time zone,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_employee_leave_period" CHECK ((end_date >= start_date))
);


--
-- Name: fuel_load; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fuel_load (
    fuel_load_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    car_id uuid NOT NULL,
    employee_id uuid,
    loaded_at timestamp with time zone NOT NULL,
    fuel_type public.fuel_type_enum NOT NULL,
    liters numeric(10,2) NOT NULL,
    unit_price numeric(12,3) NOT NULL,
    total_amount numeric(12,2) NOT NULL,
    odometer_km integer NOT NULL,
    is_full_tank boolean DEFAULT true NOT NULL,
    station character varying(120),
    payment_method public.fuel_payment_method_enum NOT NULL,
    receipt_number character varying(40),
    anomaly boolean DEFAULT false NOT NULL,
    notes text,
    odometer_correction_note text,
    created_by_user_id uuid NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    "deletedAt" timestamp with time zone,
    cash_movement_id uuid,
    registered_by_driver boolean DEFAULT false NOT NULL,
    cash_payment_legacy boolean DEFAULT false NOT NULL,
    CONSTRAINT "CHK_fuel_load_liters" CHECK ((liters > (0)::numeric)),
    CONSTRAINT "CHK_fuel_load_odometro" CHECK ((odometer_km >= 0)),
    CONSTRAINT "CHK_fuel_load_precio" CHECK ((unit_price > (0)::numeric)),
    CONSTRAINT "CHK_fuel_load_total" CHECK ((total_amount >= (0)::numeric))
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
    average_unit_cost numeric(12,2),
    reservation_deficit integer DEFAULT 0 NOT NULL,
    CONSTRAINT "CHK_gas_cylinder_tipo" CHECK ((btrim((type)::text) <> ''::text)),
    CONSTRAINT "CHK_gas_cylinder_valores" CHECK (((price > (0)::numeric) AND (weight > (0)::numeric) AND (stock >= 0) AND (reservation_deficit >= 0) AND ((average_unit_cost IS NULL) OR (average_unit_cost >= (0)::numeric))))
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
    CONSTRAINT "CHK_promocion_descuento" CHECK (((discount_percentage > (0)::numeric) AND (discount_percentage <= (99)::numeric)))
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
    photo_key character varying(512),
    CONSTRAINT "CHK_incident_descripcion" CHECK ((btrim(description) <> ''::text)),
    CONSTRAINT "CHK_incident_largo_de_textos" CHECK (((char_length(description) <= 1000) AND ((resolution_note IS NULL) OR (char_length(resolution_note) <= 1000))))
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
    is_active boolean DEFAULT true NOT NULL,
    document_kind public.plan_document_kind_enum,
    applies_to_categories character varying[]
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
    notes text,
    valid_from timestamp with time zone,
    employee_id uuid,
    details jsonb,
    CONSTRAINT "CHK_maintenance_task_hecha_fecha" CHECK (((status <> 'done'::public.maintenance_task_status_enum) OR (performed_at IS NOT NULL))),
    CONSTRAINT "CHK_maintenance_task_un_sujeto" CHECK ((num_nonnulls(car_id, delivery_id, employee_id) = 1)),
    CONSTRAINT "CHK_maintenance_task_valores" CHECK (((COALESCE(cost, (0)::numeric) >= (0)::numeric) AND (COALESCE(due_km, 0) >= 0) AND (COALESCE(odometer_km, 0) >= 0)))
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
    payment_resolved_by uuid,
    express_surcharge_amount numeric(10,2) DEFAULT '0'::numeric NOT NULL,
    express_degraded_at timestamp with time zone,
    payment_surcharge_amount numeric(10,2) DEFAULT '0'::numeric NOT NULL,
    CONSTRAINT "CHK_order_aceptado_fecha" CHECK (((status <> ALL (ARRAY['accepted'::public.order_status_enum, 'on_the_way'::public.order_status_enum, 'delivered'::public.order_status_enum])) OR ("acceptedAt" IS NOT NULL))),
    CONSTRAINT "CHK_order_cancelado_motivo" CHECK (((status <> 'cancelled'::public.order_status_enum) OR (btrim(COALESCE("cancellationReason", ''::text)) <> ''::text))),
    CONSTRAINT "CHK_order_chofer_asignado" CHECK (((status <> ALL (ARRAY['accepted'::public.order_status_enum, 'on_the_way'::public.order_status_enum, 'delivered'::public.order_status_enum])) OR (delivery_id IS NOT NULL))),
    CONSTRAINT "CHK_order_en_camino_fecha" CHECK (((status <> ALL (ARRAY['on_the_way'::public.order_status_enum, 'delivered'::public.order_status_enum])) OR ("onTheWayAt" IS NOT NULL))),
    CONSTRAINT "CHK_order_entregado_fecha" CHECK (((status = 'delivered'::public.order_status_enum) = ("deliveredAt" IS NOT NULL))),
    CONSTRAINT "CHK_order_montos" CHECK ((("totalAmount" >= (0)::numeric) AND (subtotal_items >= (0)::numeric) AND (zone_surcharge_amount >= (0)::numeric) AND (express_surcharge_amount >= (0)::numeric) AND (payment_surcharge_amount >= (0)::numeric) AND (deposit_amount >= (0)::numeric))),
    CONSTRAINT "CHK_order_nota_de_impago_largo" CHECK (((payment_resolution_note IS NULL) OR ((char_length(payment_resolution_note) <= 500) AND (char_length(btrim(payment_resolution_note)) >= 10)))),
    CONSTRAINT "CHK_order_pago_coherente" CHECK (((("paymentMethod" = 'cash'::public.order_paymentmethod_enum) = ("paymentType" = 'cash'::public.order_paymenttype_enum)) AND (("paymentMethod" = 'account'::public.order_paymentmethod_enum) = ("paymentType" = 'account'::public.order_paymenttype_enum)))),
    CONSTRAINT "CHK_order_total_formula" CHECK (("totalAmount" = (((subtotal_items + zone_surcharge_amount) + payment_surcharge_amount) +
CASE
    WHEN (express_degraded_at IS NULL) THEN express_surcharge_amount
    ELSE (0)::numeric
END)))
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
    "offeredAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_order_dispatch_offer_vencimiento" CHECK (("expiresAt" > "offeredAt"))
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
    subtotal numeric(10,2) NOT NULL,
    CONSTRAINT "CHK_order_item_cantidad" CHECK ((quantity > 0)),
    CONSTRAINT "CHK_order_item_importes" CHECK ((("unitPrice" >= (0)::numeric) AND (subtotal >= (0)::numeric)))
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
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_payment_importe" CHECK ((amount > (0)::numeric))
);


--
-- Name: payment_refund; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.payment_refund (
    refund_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    payment_id uuid NOT NULL,
    order_id uuid NOT NULL,
    distributor_id uuid,
    kind public.payment_refund_kind_enum NOT NULL,
    amount numeric(10,2) NOT NULL,
    status public.payment_refund_status_enum DEFAULT 'pending'::public.payment_refund_status_enum NOT NULL,
    gateway_refund_id character varying(100),
    error_message text,
    attempts integer DEFAULT 0 NOT NULL,
    refunded_at timestamp with time zone,
    requested_by_user_id uuid,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    refunded_baseline numeric(10,2),
    CONSTRAINT "CHK_payment_refund_exito_fecha" CHECK (((status <> 'succeeded'::public.payment_refund_status_enum) OR (refunded_at IS NOT NULL))),
    CONSTRAINT "CHK_payment_refund_importe" CHECK ((amount > (0)::numeric)),
    CONSTRAINT "CHK_payment_refund_intentos" CHECK ((attempts >= 0))
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
    close_reason text,
    CONSTRAINT "CHK_purchase_order_cancelada" CHECK (((status <> 'cancelled'::public.purchase_order_status_enum) OR (cancel_reason IS NOT NULL))),
    CONSTRAINT "CHK_purchase_order_cerrada_corta" CHECK (((status <> 'closed_short'::public.purchase_order_status_enum) OR (close_reason IS NOT NULL))),
    CONSTRAINT "CHK_purchase_order_emitida" CHECK (((status = ANY (ARRAY['draft'::public.purchase_order_status_enum, 'cancelled'::public.purchase_order_status_enum])) OR (issued_at IS NOT NULL))),
    CONSTRAINT "CHK_purchase_order_fecha_esperada" CHECK (((expected_date IS NULL) OR (expected_date >= (("createdAt" AT TIME ZONE 'America/Argentina/Buenos_Aires'::text))::date))),
    CONSTRAINT "CHK_purchase_order_total" CHECK ((total_amount >= (0)::numeric))
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
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_purchase_receipt_anulacion_datos" CHECK (((status <> 'voided'::public.purchase_receipt_status_enum) OR ((void_reason IS NOT NULL) AND (voided_by_user_id IS NOT NULL)))),
    CONSTRAINT "CHK_purchase_receipt_anulada_fecha" CHECK (((status = 'voided'::public.purchase_receipt_status_enum) = (voided_at IS NOT NULL))),
    CONSTRAINT "CHK_purchase_receipt_total" CHECK ((total_amount >= (0)::numeric))
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
    previous_on_hand_at timestamp with time zone,
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
    hidden_by_user_id uuid,
    CONSTRAINT "CHK_rating_largo_de_textos" CHECK ((((comment IS NULL) OR (char_length(comment) <= 500)) AND ((hidden_reason IS NULL) OR (char_length(hidden_reason) <= 500)))),
    CONSTRAINT "CHK_rating_valores" CHECK ((((stars >= 1) AND (stars <= 5)) AND (from_user_id <> to_user_id) AND ((NOT hidden) OR (hidden_at IS NOT NULL))))
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
    sequence integer NOT NULL,
    CONSTRAINT "CHK_route_batch_stop_secuencia" CHECK ((sequence >= 1))
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
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_stock_adjustment_notas" CHECK ((btrim(notes) <> ''::text))
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
    CONSTRAINT "CHK_stock_movement_origen_destino_distintos" CHECK ((NOT ((from_location_id = to_location_id) AND (from_condition = to_condition)))),
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
    "deletedAt" timestamp with time zone,
    CONSTRAINT "CHK_supplier_cuit" CHECK (public.es_cuit_valido((cuit)::text))
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
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_time_slot_capacidad" CHECK ((capacity > 0)),
    CONSTRAINT "CHK_time_slot_horario" CHECK (("startTime" < "endTime"))
);


--
-- Name: tire; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tire (
    tire_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    serial_number character varying(60) NOT NULL,
    brand character varying(60) NOT NULL,
    size character varying(40) NOT NULL,
    cost numeric(12,2) NOT NULL,
    status public.tire_status_enum DEFAULT 'in_stock'::public.tire_status_enum NOT NULL,
    car_id uuid,
    "position" character varying(6),
    mounted_odometer_km integer,
    km_traveled integer DEFAULT 0 NOT NULL,
    retread_count integer DEFAULT 0 NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_tire_montaje" CHECK (((status = 'mounted'::public.tire_status_enum) = ((car_id IS NOT NULL) AND ("position" IS NOT NULL)))),
    CONSTRAINT "CHK_tire_valores" CHECK (((cost >= (0)::numeric) AND (km_traveled >= 0) AND (retread_count >= 0)))
);


--
-- Name: tire_event; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tire_event (
    event_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    tire_id uuid NOT NULL,
    distributor_id uuid NOT NULL,
    type public.tire_event_type_enum NOT NULL,
    car_id uuid,
    "position" character varying(6),
    odometer_km integer NOT NULL,
    created_by_user_id uuid NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: traffic_fine; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.traffic_fine (
    fine_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    car_id uuid NOT NULL,
    employee_id uuid,
    occurred_at timestamp with time zone NOT NULL,
    jurisdiction character varying(80) NOT NULL,
    act_number character varying(40) NOT NULL,
    infraction text NOT NULL,
    amount numeric(12,2) NOT NULL,
    voluntary_payment_amount numeric(12,2),
    due_date date,
    status public.traffic_fine_status_enum DEFAULT 'pending'::public.traffic_fine_status_enum NOT NULL,
    paid_at timestamp with time zone,
    paid_amount numeric(12,2),
    charged_to_employee boolean DEFAULT false NOT NULL,
    void_reason text,
    voided_at timestamp with time zone,
    alerted_at timestamp with time zone,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    cash_movement_id uuid,
    CONSTRAINT "CHK_traffic_fine_amount" CHECK ((amount > (0)::numeric)),
    CONSTRAINT "CHK_traffic_fine_anulada_fecha" CHECK (((status <> 'voided'::public.traffic_fine_status_enum) OR (voided_at IS NOT NULL))),
    CONSTRAINT "CHK_traffic_fine_importe_pagado" CHECK (((paid_amount IS NULL) OR (paid_amount > (0)::numeric))),
    CONSTRAINT "CHK_traffic_fine_pagada_datos" CHECK (((status <> 'paid'::public.traffic_fine_status_enum) OR ((paid_at IS NOT NULL) AND (paid_amount IS NOT NULL)))),
    CONSTRAINT "CHK_traffic_fine_pago_contra_importe" CHECK (((paid_amount IS NULL) OR (paid_amount <= amount))),
    CONSTRAINT "CHK_traffic_fine_pago_voluntario" CHECK (((voluntary_payment_amount IS NULL) OR ((voluntary_payment_amount > (0)::numeric) AND (voluntary_payment_amount <= amount))))
);


--
-- Name: truck_load; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.truck_load (
    load_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    number integer NOT NULL,
    car_id uuid NOT NULL,
    delivery_id uuid NOT NULL,
    helper_employee_id uuid,
    origin_location_id uuid NOT NULL,
    business_date date NOT NULL,
    status public.truck_load_status_enum DEFAULT 'loading'::public.truck_load_status_enum NOT NULL,
    opened_at timestamp with time zone DEFAULT now() NOT NULL,
    departed_at timestamp with time zone,
    returned_at timestamp with time zone,
    closed_at timestamp with time zone,
    opened_by_user_id uuid NOT NULL,
    closed_by_user_id uuid,
    difference_note text,
    cancel_reason text,
    notes text,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_truck_load_cancelada" CHECK (((status <> 'cancelled'::public.truck_load_status_enum) OR (cancel_reason IS NOT NULL))),
    CONSTRAINT "CHK_truck_load_cierre" CHECK (((status <> ALL (ARRAY['closed'::public.truck_load_status_enum, 'closed_with_difference'::public.truck_load_status_enum, 'cancelled'::public.truck_load_status_enum])) OR (closed_at IS NOT NULL))),
    CONSTRAINT "CHK_truck_load_regreso" CHECK (((status <> ALL (ARRAY['returned'::public.truck_load_status_enum, 'closed'::public.truck_load_status_enum, 'closed_with_difference'::public.truck_load_status_enum])) OR (returned_at IS NOT NULL))),
    CONSTRAINT "CHK_truck_load_salida" CHECK (((status = ANY (ARRAY['loading'::public.truck_load_status_enum, 'cancelled'::public.truck_load_status_enum])) OR (departed_at IS NOT NULL)))
);


--
-- Name: truck_load_item; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.truck_load_item (
    item_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    load_id uuid NOT NULL,
    gas_cylinder_id uuid NOT NULL,
    loaded_full integer DEFAULT 0 NOT NULL,
    reloaded_full integer DEFAULT 0 NOT NULL,
    loaded_empty integer DEFAULT 0 NOT NULL,
    declared_return_full integer,
    declared_return_empty integer,
    delivered_full integer,
    collected_empty integer,
    expected_full integer,
    expected_empty integer,
    difference_full integer,
    difference_empty integer,
    CONSTRAINT "CHK_truck_load_item_cargado" CHECK (((loaded_full >= 0) AND (reloaded_full >= 0) AND (loaded_empty >= 0))),
    CONSTRAINT "CHK_truck_load_item_declarado" CHECK ((((declared_return_full IS NULL) OR (declared_return_full >= 0)) AND ((declared_return_empty IS NULL) OR (declared_return_empty >= 0))))
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
    photo_key character varying(512),
    CONSTRAINT "CHK_user_email" CHECK (((email IS NULL) OR ((email)::text ~* '^[^@[:space:]]+@[^@[:space:]]+[.][^@[:space:]]+$'::text))),
    CONSTRAINT "CHK_user_telefono" CHECK (((phone_number IS NULL) OR ((phone_number)::text ~ '^[+][1-9][0-9]{7,14}$'::text)))
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
-- Name: vehicle_accident; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vehicle_accident (
    accident_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    distributor_id uuid NOT NULL,
    car_id uuid NOT NULL,
    employee_id uuid,
    occurred_at timestamp with time zone NOT NULL,
    location public.geometry(Point,4326),
    address text,
    description text NOT NULL,
    injuries boolean DEFAULT false NOT NULL,
    third_parties_involved boolean DEFAULT false NOT NULL,
    hazmat_release boolean DEFAULT false NOT NULL,
    police_report_number character varying(40),
    insurer_claim_number character varying(40),
    status public.vehicle_accident_status_enum DEFAULT 'reported'::public.vehicle_accident_status_enum NOT NULL,
    vehicle_unusable boolean DEFAULT false NOT NULL,
    repair_cost numeric(12,2),
    insurer_reimbursement numeric(12,2),
    deductible_amount numeric(12,2),
    closed_at timestamp with time zone,
    created_by_user_id uuid NOT NULL,
    "createdAt" timestamp with time zone DEFAULT now() NOT NULL,
    "updatedAt" timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "CHK_vehicle_accident_cerrado_fecha" CHECK (((status <> 'closed'::public.vehicle_accident_status_enum) OR (closed_at IS NOT NULL))),
    CONSTRAINT "CHK_vehicle_accident_montos" CHECK (((COALESCE(repair_cost, (0)::numeric) >= (0)::numeric) AND (COALESCE(insurer_reimbursement, (0)::numeric) >= (0)::numeric) AND (COALESCE(deductible_amount, (0)::numeric) >= (0)::numeric) AND ((insurer_reimbursement IS NULL) OR (repair_cost IS NULL) OR (insurer_reimbursement <= repair_cost))))
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
    note text,
    CONSTRAINT "CHK_vehicle_assignment_periodo" CHECK (((released_at IS NULL) OR (released_at >= assigned_at)))
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
    route_hours numeric(6,2) DEFAULT '0'::numeric NOT NULL,
    CONSTRAINT "CHK_vehicle_usage_log_valores" CHECK (((km >= (0)::numeric) AND (orders >= 0) AND (route_hours >= (0)::numeric)))
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
    "deletedAt" timestamp with time zone,
    CONSTRAINT "CHK_warehouse_codigo" CHECK (((code)::text ~ '^[A-Z0-9_-]{1,12}$'::text))
);


--
-- Name: commission_rule EXC_commission_rule_solapada; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_rule
    ADD CONSTRAINT "EXC_commission_rule_solapada" EXCLUDE USING gist (distributor_id WITH =, COALESCE(employee_id, '00000000-0000-0000-0000-000000000000'::uuid) WITH =, COALESCE(gas_cylinder_id, '00000000-0000-0000-0000-000000000000'::uuid) WITH =, daterange(valid_from, valid_to, '[]'::text) WITH &&) WHERE (is_active);


--
-- Name: driver_liquidation EXC_driver_liquidation_periodo_solapado; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_liquidation
    ADD CONSTRAINT "EXC_driver_liquidation_periodo_solapado" EXCLUDE USING gist (employee_id WITH =, daterange(period_from, period_to, '[]'::text) WITH &&) WHERE ((status <> 'voided'::public.driver_liquidation_status_enum));


--
-- Name: employee_attendance EXC_employee_attendance_solapada; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_attendance
    ADD CONSTRAINT "EXC_employee_attendance_solapada" EXCLUDE USING gist (employee_id WITH =, tstzrange(check_in_at, COALESCE(check_out_at, 'infinity'::timestamp with time zone)) WITH &&);


--
-- Name: time_slot EXC_time_slot_solapada; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.time_slot
    ADD CONSTRAINT "EXC_time_slot_solapada" EXCLUDE USING gist (distributor_id WITH =, tsrange(('2000-01-01 00:00:00'::timestamp without time zone + ("startTime")::interval), ('2000-01-01 00:00:00'::timestamp without time zone + ("endTime")::interval)) WITH &&) WHERE (("isActive" AND ("startTime" IS NOT NULL) AND ("endTime" IS NOT NULL)));


--
-- Name: vehicle_assignment EXC_vehicle_assignment_chofer_solapada; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_assignment
    ADD CONSTRAINT "EXC_vehicle_assignment_chofer_solapada" EXCLUDE USING gist (delivery_id WITH =, tstzrange(assigned_at, COALESCE(released_at, 'infinity'::timestamp with time zone)) WITH &&);


--
-- Name: vehicle_assignment EXC_vehicle_assignment_vehiculo_solapada; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_assignment
    ADD CONSTRAINT "EXC_vehicle_assignment_vehiculo_solapada" EXCLUDE USING gist (car_id WITH =, tstzrange(assigned_at, COALESCE(released_at, 'infinity'::timestamp with time zone)) WITH &&);


--
-- Name: vehicle_assignment PK_03cbc11f348efffa59570945343; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_assignment
    ADD CONSTRAINT "PK_03cbc11f348efffa59570945343" PRIMARY KEY (assignment_id);


--
-- Name: cash_session PK_0405f0f75e0ea603b67f56512a0; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_session
    ADD CONSTRAINT "PK_0405f0f75e0ea603b67f56512a0" PRIMARY KEY (session_id);


--
-- Name: traffic_fine PK_070a6dff8acb17a6bbfecad41df; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic_fine
    ADD CONSTRAINT "PK_070a6dff8acb17a6bbfecad41df" PRIMARY KEY (fine_id);


--
-- Name: admin PK_08603203f2c50664bda27b1ff89; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT "PK_08603203f2c50664bda27b1ff89" PRIMARY KEY (admin_id);


--
-- Name: driver_settlement_expense PK_08eefdada00e317b45b6010c36e; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement_expense
    ADD CONSTRAINT "PK_08eefdada00e317b45b6010c36e" PRIMARY KEY (expense_id);


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
-- Name: tire PK_1cd585e4893980c1fdc669df3da; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tire
    ADD CONSTRAINT "PK_1cd585e4893980c1fdc669df3da" PRIMARY KEY (tire_id);


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
-- Name: driver_settlement_order PK_32d328e79201459a738eb2f2071; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement_order
    ADD CONSTRAINT "PK_32d328e79201459a738eb2f2071" PRIMARY KEY (settlement_order_id);


--
-- Name: fuel_load PK_365d58e595b7370dd809570d41e; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fuel_load
    ADD CONSTRAINT "PK_365d58e595b7370dd809570d41e" PRIMARY KEY (fuel_load_id);


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
-- Name: truck_load PK_3dbdc80ba4676ee68d818791f34; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load
    ADD CONSTRAINT "PK_3dbdc80ba4676ee68d818791f34" PRIMARY KEY (load_id);


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
-- Name: customer_account_allocation PK_656ecedc3cc77c138bd4f5ed181; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account_allocation
    ADD CONSTRAINT "PK_656ecedc3cc77c138bd4f5ed181" PRIMARY KEY (allocation_id);


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
-- Name: driver_settlement PK_6fac21943a903481ccf2fbc72e3; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement
    ADD CONSTRAINT "PK_6fac21943a903481ccf2fbc72e3" PRIMARY KEY (settlement_id);


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
-- Name: employee_leave PK_84fc148f29a528aa770fb590a1f; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_leave
    ADD CONSTRAINT "PK_84fc148f29a528aa770fb590a1f" PRIMARY KEY (leave_id);


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
-- Name: tire_event PK_8f948fe5b4246a2a92915126dad; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tire_event
    ADD CONSTRAINT "PK_8f948fe5b4246a2a92915126dad" PRIMARY KEY (event_id);


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
-- Name: cash_category PK_9ed23398638cf60f931c58a6254; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_category
    ADD CONSTRAINT "PK_9ed23398638cf60f931c58a6254" PRIMARY KEY (category_id);


--
-- Name: delivery PK_9f4d2062bce95d9b75e00d145ee; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.delivery
    ADD CONSTRAINT "PK_9f4d2062bce95d9b75e00d145ee" PRIMARY KEY (delivery_id);


--
-- Name: driver_settlement_collection PK_9fb2ab779fdce604bd99c6e03d4; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement_collection
    ADD CONSTRAINT "PK_9fb2ab779fdce604bd99c6e03d4" PRIMARY KEY (collection_id);


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
-- Name: commission_entry PK_af74ef71d43b41c3a39141fda1c; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_entry
    ADD CONSTRAINT "PK_af74ef71d43b41c3a39141fda1c" PRIMARY KEY (entry_id);


--
-- Name: payment_refund PK_b2ceff76c7c89bdd2259d27a8a7; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_refund
    ADD CONSTRAINT "PK_b2ceff76c7c89bdd2259d27a8a7" PRIMARY KEY (refund_id);


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
-- Name: employee_attendance PK_ba49c1b4279ee383655a5065e06; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_attendance
    ADD CONSTRAINT "PK_ba49c1b4279ee383655a5065e06" PRIMARY KEY (attendance_id);


--
-- Name: truck_load_item PK_bad04888d48307d2e2cefb5e4ab; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load_item
    ADD CONSTRAINT "PK_bad04888d48307d2e2cefb5e4ab" PRIMARY KEY (item_id);


--
-- Name: cash_movement PK_c3fc21001d0a2ada9461504eeb8; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_movement
    ADD CONSTRAINT "PK_c3fc21001d0a2ada9461504eeb8" PRIMARY KEY (movement_id);


--
-- Name: vehicle_accident PK_c6448a95ffc706c4e8c25d007f1; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_accident
    ADD CONSTRAINT "PK_c6448a95ffc706c4e8c25d007f1" PRIMARY KEY (accident_id);


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
-- Name: customer_account PK_d1e5a9401cb7dcb5604168f96ea; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account
    ADD CONSTRAINT "PK_d1e5a9401cb7dcb5604168f96ea" PRIMARY KEY (account_id);


--
-- Name: cash_box PK_d48c98d81a07966df57824713cd; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_box
    ADD CONSTRAINT "PK_d48c98d81a07966df57824713cd" PRIMARY KEY (cash_box_id);


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
-- Name: customer_account_entry PK_e1c743cf21d5ab0b30d342404dc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account_entry
    ADD CONSTRAINT "PK_e1c743cf21d5ab0b30d342404dc" PRIMARY KEY (entry_id);


--
-- Name: commission_rule PK_e46763ead31c4f2fceeb5faefdd; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_rule
    ADD CONSTRAINT "PK_e46763ead31c4f2fceeb5faefdd" PRIMARY KEY (rule_id);


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
-- Name: driver_liquidation PK_efb13a8e9ee929dd7477906021c; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_liquidation
    ADD CONSTRAINT "PK_efb13a8e9ee929dd7477906021c" PRIMARY KEY (liquidation_id);


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
-- Name: car UQ_car_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.car
    ADD CONSTRAINT "UQ_car_id_distribuidora" UNIQUE (car_id, distributor_id);


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
-- Name: cash_box UQ_cash_box_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_box
    ADD CONSTRAINT "UQ_cash_box_id_distribuidora" UNIQUE (cash_box_id, distributor_id);


--
-- Name: cash_category UQ_cash_category_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_category
    ADD CONSTRAINT "UQ_cash_category_id_distribuidora" UNIQUE (category_id, distributor_id);


--
-- Name: cash_movement UQ_cash_movement_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_movement
    ADD CONSTRAINT "UQ_cash_movement_id_distribuidora" UNIQUE (movement_id, distributor_id);


--
-- Name: cash_session UQ_cash_session_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_session
    ADD CONSTRAINT "UQ_cash_session_id_distribuidora" UNIQUE (session_id, distributor_id);


--
-- Name: coverage_zone UQ_coverage_zone_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coverage_zone
    ADD CONSTRAINT "UQ_coverage_zone_id_distribuidora" UNIQUE (coverage_zone_id, distributor_id);


--
-- Name: customer_account UQ_customer_account_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account
    ADD CONSTRAINT "UQ_customer_account_id_distribuidora" UNIQUE (account_id, distributor_id);


--
-- Name: cylinder UQ_cylinder_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder
    ADD CONSTRAINT "UQ_cylinder_id_distribuidora" UNIQUE (cylinder_id, distributor_id);


--
-- Name: delivery UQ_delivery_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.delivery
    ADD CONSTRAINT "UQ_delivery_id_distribuidora" UNIQUE (delivery_id, distributor_id);


--
-- Name: driver_liquidation UQ_driver_liquidation_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_liquidation
    ADD CONSTRAINT "UQ_driver_liquidation_id_distribuidora" UNIQUE (liquidation_id, distributor_id);


--
-- Name: user UQ_e12875dfb3b1d92d7d7c5377e22; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "UQ_e12875dfb3b1d92d7d7c5377e22" UNIQUE (email);


--
-- Name: employee UQ_employee_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT "UQ_employee_id_distribuidora" UNIQUE (employee_id, distributor_id);


--
-- Name: gas_cylinder UQ_gas_cylinder_distribuidora_tipo; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.gas_cylinder
    ADD CONSTRAINT "UQ_gas_cylinder_distribuidora_tipo" UNIQUE (distributor_id, type);


--
-- Name: gas_cylinder UQ_gas_cylinder_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.gas_cylinder
    ADD CONSTRAINT "UQ_gas_cylinder_id_distribuidora" UNIQUE (gas_cylinder_id, distributor_id);


--
-- Name: module_config UQ_module_config_distributor_module; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.module_config
    ADD CONSTRAINT "UQ_module_config_distributor_module" UNIQUE (distributor_id, module);


--
-- Name: order UQ_order_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "UQ_order_id_distribuidora" UNIQUE (order_id, distributor_id);


--
-- Name: payment_refund UQ_payment_refund_payment_kind; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_refund
    ADD CONSTRAINT "UQ_payment_refund_payment_kind" UNIQUE (payment_id, kind);


--
-- Name: purchase_order UQ_purchase_order_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT "UQ_purchase_order_id_distribuidora" UNIQUE (purchase_order_id, distributor_id);


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
-- Name: stock_location UQ_stock_location_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_location
    ADD CONSTRAINT "UQ_stock_location_id_distribuidora" UNIQUE (location_id, distributor_id);


--
-- Name: stock_movement UQ_stock_movement_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement
    ADD CONSTRAINT "UQ_stock_movement_id_distribuidora" UNIQUE (movement_id, distributor_id);


--
-- Name: supplier UQ_supplier_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.supplier
    ADD CONSTRAINT "UQ_supplier_id_distribuidora" UNIQUE (supplier_id, distributor_id);


--
-- Name: time_slot UQ_time_slot_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.time_slot
    ADD CONSTRAINT "UQ_time_slot_id_distribuidora" UNIQUE (time_slot_id, distributor_id);


--
-- Name: truck_load UQ_truck_load_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load
    ADD CONSTRAINT "UQ_truck_load_id_distribuidora" UNIQUE (load_id, distributor_id);


--
-- Name: vehicle_usage_log UQ_vehicle_usage_log_car_day; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_usage_log
    ADD CONSTRAINT "UQ_vehicle_usage_log_car_day" UNIQUE (car_id, day);


--
-- Name: warehouse UQ_warehouse_id_distribuidora; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.warehouse
    ADD CONSTRAINT "UQ_warehouse_id_distribuidora" UNIQUE (warehouse_id, distributor_id);


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
-- Name: IDX_9649d0833082fad8f431ff1381; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_9649d0833082fad8f431ff1381" ON public.payment_refund USING btree (distributor_id);


--
-- Name: IDX_968ad11170db2741bb5c0c47bb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_968ad11170db2741bb5c0c47bb" ON public.cylinder_movement USING btree (distributor_id);


--
-- Name: IDX_990b829fdf06cb282d835a5d72; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_990b829fdf06cb282d835a5d72" ON public.gas_cylinder USING btree (distributor_id);


--
-- Name: IDX_9b1ba9fb797de22fc87b598f50; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_9b1ba9fb797de22fc87b598f50" ON public.payment_refund USING btree (payment_id);


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
-- Name: IDX_a2ae8bef86602c9f97be8e0b41; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_a2ae8bef86602c9f97be8e0b41" ON public.payment_refund USING btree (status);


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
-- Name: IDX_cash_box_distributor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_cash_box_distributor" ON public.cash_box USING btree (distributor_id);


--
-- Name: IDX_cash_category_distributor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_cash_category_distributor" ON public.cash_category USING btree (distributor_id);


--
-- Name: IDX_cash_movement_caja_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_cash_movement_caja_fecha" ON public.cash_movement USING btree (cash_box_id, occurred_at);


--
-- Name: IDX_cash_movement_distribuidora_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_cash_movement_distribuidora_fecha" ON public.cash_movement USING btree (distributor_id, occurred_at);


--
-- Name: IDX_cash_movement_referencia; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_cash_movement_referencia" ON public.cash_movement USING btree (reference_type, reference_id);


--
-- Name: IDX_cash_movement_sesion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_cash_movement_sesion" ON public.cash_movement USING btree (session_id);


--
-- Name: IDX_cash_session_caja_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_cash_session_caja_fecha" ON public.cash_session USING btree (cash_box_id, opened_at);


--
-- Name: IDX_cash_session_distributor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_cash_session_distributor" ON public.cash_session USING btree (distributor_id);


--
-- Name: IDX_cd7812c96209c5bdd48a6b858b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_cd7812c96209c5bdd48a6b858b" ON public."order" USING btree (customer_id);


--
-- Name: IDX_commission_entry_distributor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_commission_entry_distributor" ON public.commission_entry USING btree (distributor_id);


--
-- Name: IDX_commission_entry_empleado; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_commission_entry_empleado" ON public.commission_entry USING btree (employee_id, occurred_at);


--
-- Name: IDX_commission_entry_liquidacion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_commission_entry_liquidacion" ON public.commission_entry USING btree (liquidation_id);


--
-- Name: IDX_commission_rule_distribuidora; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_commission_rule_distribuidora" ON public.commission_rule USING btree (distributor_id, is_active);


--
-- Name: IDX_customer_account_allocation_credito; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_customer_account_allocation_credito" ON public.customer_account_allocation USING btree (credit_entry_id);


--
-- Name: IDX_customer_account_allocation_cuenta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_customer_account_allocation_cuenta" ON public.customer_account_allocation USING btree (account_id);


--
-- Name: IDX_customer_account_allocation_debito; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_customer_account_allocation_debito" ON public.customer_account_allocation USING btree (debit_entry_id);


--
-- Name: IDX_customer_account_distributor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_customer_account_distributor" ON public.customer_account USING btree (distributor_id);


--
-- Name: IDX_customer_account_entry_cuenta_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_customer_account_entry_cuenta_fecha" ON public.customer_account_entry USING btree (account_id, occurred_at);


--
-- Name: IDX_customer_account_entry_distributor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_customer_account_entry_distributor" ON public.customer_account_entry USING btree (distributor_id);


--
-- Name: IDX_d6bb53d55c3556b23295d5ac5a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_d6bb53d55c3556b23295d5ac5a" ON public.cylinder_recovery_case USING btree (distributor_id);


--
-- Name: IDX_ddf9b0a3d9abeee97fa77f0f20; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_ddf9b0a3d9abeee97fa77f0f20" ON public.payment_refund USING btree (order_id);


--
-- Name: IDX_df56039592a4bbbd3fa4a19f14; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_df56039592a4bbbd3fa4a19f14" ON public."order" USING btree (distributor_id);


--
-- Name: IDX_driver_liquidation_distributor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_driver_liquidation_distributor" ON public.driver_liquidation USING btree (distributor_id);


--
-- Name: IDX_driver_liquidation_empleado; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_driver_liquidation_empleado" ON public.driver_liquidation USING btree (employee_id, status);


--
-- Name: IDX_driver_settlement_chofer; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_driver_settlement_chofer" ON public.driver_settlement USING btree (delivery_id);


--
-- Name: IDX_driver_settlement_collection_rendicion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_driver_settlement_collection_rendicion" ON public.driver_settlement_collection USING btree (settlement_id);


--
-- Name: IDX_driver_settlement_estado; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_driver_settlement_estado" ON public.driver_settlement USING btree (distributor_id, status);


--
-- Name: IDX_driver_settlement_expense_rendicion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_driver_settlement_expense_rendicion" ON public.driver_settlement_expense USING btree (settlement_id);


--
-- Name: IDX_driver_settlement_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_driver_settlement_fecha" ON public.driver_settlement USING btree (distributor_id, business_date);


--
-- Name: IDX_driver_settlement_order_rendicion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_driver_settlement_order_rendicion" ON public.driver_settlement_order USING btree (settlement_id);


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
-- Name: IDX_employee_attendance_day; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_employee_attendance_day" ON public.employee_attendance USING btree (distributor_id, work_date);


--
-- Name: IDX_employee_attendance_employee; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_employee_attendance_employee" ON public.employee_attendance USING btree (employee_id, work_date);


--
-- Name: IDX_employee_leave_distributor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_employee_leave_distributor" ON public.employee_leave USING btree (distributor_id, status);


--
-- Name: IDX_employee_leave_employee; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_employee_leave_employee" ON public.employee_leave USING btree (employee_id, status, start_date, end_date);


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
-- Name: IDX_fuel_load_car_loaded_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_fuel_load_car_loaded_at" ON public.fuel_load USING btree (car_id, loaded_at);


--
-- Name: IDX_fuel_load_distributor_loaded_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_fuel_load_distributor_loaded_at" ON public.fuel_load USING btree (distributor_id, loaded_at);


--
-- Name: IDX_maintenance_task_employee; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_maintenance_task_employee" ON public.maintenance_task USING btree (employee_id);


--
-- Name: IDX_order_status_history_cancelacion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_order_status_history_cancelacion" ON public.order_status_history USING btree (order_id, changed_at) WHERE (to_status = 'cancelled'::public.order_status_enum);


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
-- Name: IDX_stock_movement_alta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_stock_movement_alta" ON public.stock_movement USING btree (distributor_id, "createdAt");


--
-- Name: IDX_stock_movement_destino; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_stock_movement_destino" ON public.stock_movement USING btree (to_location_id, gas_cylinder_id, to_condition);


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

CREATE INDEX "IDX_stock_movement_origen" ON public.stock_movement USING btree (from_location_id, gas_cylinder_id, from_condition);


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
-- Name: IDX_tire_event_tire; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_tire_event_tire" ON public.tire_event USING btree (tire_id, "createdAt");


--
-- Name: IDX_traffic_fine_car; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_traffic_fine_car" ON public.traffic_fine USING btree (car_id, occurred_at);


--
-- Name: IDX_traffic_fine_status_due; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_traffic_fine_status_due" ON public.traffic_fine USING btree (distributor_id, status, due_date);


--
-- Name: IDX_truck_load_camion; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_truck_load_camion" ON public.truck_load USING btree (car_id);


--
-- Name: IDX_truck_load_chofer; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_truck_load_chofer" ON public.truck_load USING btree (delivery_id);


--
-- Name: IDX_truck_load_estado; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_truck_load_estado" ON public.truck_load USING btree (distributor_id, status);


--
-- Name: IDX_truck_load_fecha; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_truck_load_fecha" ON public.truck_load USING btree (distributor_id, business_date);


--
-- Name: IDX_truck_load_item_garrafa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_truck_load_item_garrafa" ON public.truck_load_item USING btree (gas_cylinder_id);


--
-- Name: IDX_vehicle_accident_car; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_vehicle_accident_car" ON public.vehicle_accident USING btree (car_id, occurred_at);


--
-- Name: IDX_vehicle_accident_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_vehicle_accident_status" ON public.vehicle_accident USING btree (distributor_id, status);


--
-- Name: IDX_warehouse_distributor; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "IDX_warehouse_distributor" ON public.warehouse USING btree (distributor_id);


--
-- Name: UQ_admin_user; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_admin_user" ON public.admin USING btree (user_id);


--
-- Name: UQ_car_patente_distribuidora_vigente; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_car_patente_distribuidora_vigente" ON public.car USING btree (distributor_id, car_patent) WHERE ("deletedAt" IS NULL);


--
-- Name: UQ_cash_box_nombre_vigente; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_cash_box_nombre_vigente" ON public.cash_box USING btree (distributor_id, name) WHERE ("deletedAt" IS NULL);


--
-- Name: UQ_cash_category_nombre_activa; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_cash_category_nombre_activa" ON public.cash_category USING btree (distributor_id, direction, name) WHERE ((is_active = true) AND (system_code IS NULL));


--
-- Name: UQ_cash_category_sistema; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_cash_category_sistema" ON public.cash_category USING btree (distributor_id, system_code) WHERE (system_code IS NOT NULL);


--
-- Name: UQ_cash_movement_anula; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_cash_movement_anula" ON public.cash_movement USING btree (reverses_movement_id) WHERE (reverses_movement_id IS NOT NULL);


--
-- Name: UQ_cash_session_abierta; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_cash_session_abierta" ON public.cash_session USING btree (cash_box_id) WHERE (status = 'open'::public.cash_session_status_enum);


--
-- Name: UQ_commission_entry_faltante; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_commission_entry_faltante" ON public.commission_entry USING btree (reference_id) WHERE (type = 'settlement_shortage'::public.commission_entry_type_enum);


--
-- Name: UQ_commission_entry_pedido; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_commission_entry_pedido" ON public.commission_entry USING btree (order_id) WHERE (type = 'delivery_commission'::public.commission_entry_type_enum);


--
-- Name: UQ_coverage_zone_nombre_activa; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_coverage_zone_nombre_activa" ON public.coverage_zone USING btree (distributor_id, lower((name)::text)) WHERE ("isActive" AND ("deletedAt" IS NULL));


--
-- Name: UQ_coverage_zone_prioridad_activa; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_coverage_zone_prioridad_activa" ON public.coverage_zone USING btree (distributor_id, priority) WHERE ("isActive" AND ("deletedAt" IS NULL));


--
-- Name: UQ_customer_account_cliente_vigente; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_customer_account_cliente_vigente" ON public.customer_account USING btree (distributor_id, customer_user_id) WHERE ("deletedAt" IS NULL);


--
-- Name: UQ_customer_account_entry_cargo_pedido; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_customer_account_entry_cargo_pedido" ON public.customer_account_entry USING btree (order_id) WHERE (type = 'sale_charge'::public.customer_account_entry_type_enum);


--
-- Name: UQ_cylinder_serial_normalizado; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_cylinder_serial_normalizado" ON public.cylinder USING btree (distributor_id, upper(btrim((serial)::text)));


--
-- Name: UQ_driver_liquidation_numero; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_driver_liquidation_numero" ON public.driver_liquidation USING btree (distributor_id, number);


--
-- Name: UQ_driver_settlement_carga; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_driver_settlement_carga" ON public.driver_settlement USING btree (truck_load_id) WHERE (truck_load_id IS NOT NULL);


--
-- Name: UQ_driver_settlement_chofer_dia; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_driver_settlement_chofer_dia" ON public.driver_settlement USING btree (delivery_id, business_date);


--
-- Name: UQ_driver_settlement_collection_asiento; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_driver_settlement_collection_asiento" ON public.driver_settlement_collection USING btree (entry_id);


--
-- Name: UQ_driver_settlement_numero; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_driver_settlement_numero" ON public.driver_settlement USING btree (distributor_id, number);


--
-- Name: UQ_driver_settlement_order_pedido; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_driver_settlement_order_pedido" ON public.driver_settlement_order USING btree (order_id);


--
-- Name: UQ_employee_attendance_abierta; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_employee_attendance_abierta" ON public.employee_attendance USING btree (employee_id) WHERE (check_out_at IS NULL);


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
-- Name: UQ_gas_cylinder_tipo_normalizado; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_gas_cylinder_tipo_normalizado" ON public.gas_cylinder USING btree (distributor_id, lower(btrim((type)::text)));


--
-- Name: UQ_incident_cobro_impago; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_incident_cobro_impago" ON public.incident USING btree (order_id) WHERE ((type = 'unpaid_collection'::public.incident_type_enum) AND (status = ANY (ARRAY['open'::public.incident_status_enum, 'resolved'::public.incident_status_enum])));


--
-- Name: UQ_job_position_name_vigente; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_job_position_name_vigente" ON public.job_position USING btree (distributor_id, lower((name)::text)) WHERE ("deletedAt" IS NULL);


--
-- Name: UQ_order_dispatch_offer_aceptada; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_order_dispatch_offer_aceptada" ON public.order_dispatch_offer USING btree (order_id) WHERE (status = 'accepted'::public.order_dispatch_offer_status_enum);


--
-- Name: UQ_order_dispatch_offer_viva; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_order_dispatch_offer_viva" ON public.order_dispatch_offer USING btree (order_id, driver_id) WHERE (status = 'offered'::public.order_dispatch_offer_status_enum);


--
-- Name: UQ_order_item_pedido_producto; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_order_item_pedido_producto" ON public.order_item USING btree (order_id, gas_cylinder_id);


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
-- Name: UQ_route_batch_stop_secuencia; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_route_batch_stop_secuencia" ON public.route_batch_stop USING btree (batch_id, sequence);


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
-- Name: UQ_time_slot_nombre_activa; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_time_slot_nombre_activa" ON public.time_slot USING btree (distributor_id, lower((name)::text)) WHERE "isActive";


--
-- Name: UQ_tire_posicion_ocupada; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_tire_posicion_ocupada" ON public.tire USING btree (car_id, "position") WHERE (status = 'mounted'::public.tire_status_enum);


--
-- Name: UQ_tire_serial; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_tire_serial" ON public.tire USING btree (distributor_id, serial_number);


--
-- Name: UQ_traffic_fine_act; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_traffic_fine_act" ON public.traffic_fine USING btree (distributor_id, jurisdiction, act_number);


--
-- Name: UQ_truck_load_camion_abierta; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_truck_load_camion_abierta" ON public.truck_load USING btree (car_id) WHERE (status = ANY (ARRAY['loading'::public.truck_load_status_enum, 'on_route'::public.truck_load_status_enum, 'returned'::public.truck_load_status_enum]));


--
-- Name: UQ_truck_load_chofer_abierta; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_truck_load_chofer_abierta" ON public.truck_load USING btree (delivery_id) WHERE (status = ANY (ARRAY['loading'::public.truck_load_status_enum, 'on_route'::public.truck_load_status_enum, 'returned'::public.truck_load_status_enum]));


--
-- Name: UQ_truck_load_item_garrafa; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_truck_load_item_garrafa" ON public.truck_load_item USING btree (load_id, gas_cylinder_id);


--
-- Name: UQ_truck_load_numero; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_truck_load_numero" ON public.truck_load USING btree (distributor_id, number);


--
-- Name: UQ_user_address_principal; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_user_address_principal" ON public.user_address USING btree (user_id) WHERE ("isDefault" AND ("deletedAt" IS NULL));


--
-- Name: UQ_user_email_minusculas; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UQ_user_email_minusculas" ON public."user" USING btree (lower((email)::text));


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
-- Name: cash_box TRG_cash_box_saldo_contra_libro; Type: TRIGGER; Schema: public; Owner: -
--

CREATE CONSTRAINT TRIGGER "TRG_cash_box_saldo_contra_libro" AFTER INSERT OR UPDATE OF balance ON public.cash_box DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION public.verificar_saldo_de_caja();


--
-- Name: cash_movement TRG_cash_movement_saldo_contra_libro; Type: TRIGGER; Schema: public; Owner: -
--

CREATE CONSTRAINT TRIGGER "TRG_cash_movement_saldo_contra_libro" AFTER INSERT ON public.cash_movement DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION public.verificar_saldo_de_caja();


--
-- Name: claims TRG_claims_transicion_de_estado; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_claims_transicion_de_estado" BEFORE UPDATE OF status ON public.claims FOR EACH ROW EXECUTE FUNCTION public.transicion_de_estado_claims();


--
-- Name: customer_account_allocation TRG_customer_account_allocation_tope; Type: TRIGGER; Schema: public; Owner: -
--

CREATE CONSTRAINT TRIGGER "TRG_customer_account_allocation_tope" AFTER INSERT ON public.customer_account_allocation DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION public.verificar_imputacion_de_cuenta();


--
-- Name: customer_account_entry TRG_customer_account_entry_cobro_maximo; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_customer_account_entry_cobro_maximo" BEFORE INSERT ON public.customer_account_entry FOR EACH ROW WHEN ((new.type = 'payment'::public.customer_account_entry_type_enum)) EXECUTE FUNCTION public.cobro_de_cuenta_maximo();


--
-- Name: customer_account_entry TRG_customer_account_entry_saldo_contra_libro; Type: TRIGGER; Schema: public; Owner: -
--

CREATE CONSTRAINT TRIGGER "TRG_customer_account_entry_saldo_contra_libro" AFTER INSERT ON public.customer_account_entry DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION public.verificar_saldo_de_cuenta();


--
-- Name: customer_account TRG_customer_account_saldo_contra_libro; Type: TRIGGER; Schema: public; Owner: -
--

CREATE CONSTRAINT TRIGGER "TRG_customer_account_saldo_contra_libro" AFTER INSERT OR UPDATE OF balance ON public.customer_account DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION public.verificar_saldo_de_cuenta();


--
-- Name: customer_account TRG_customer_account_transicion_de_estado; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_customer_account_transicion_de_estado" BEFORE UPDATE OF status ON public.customer_account FOR EACH ROW EXECUTE FUNCTION public.transicion_de_estado_customer_account();


--
-- Name: cylinder TRG_cylinder_fabricacion_no_futura; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_cylinder_fabricacion_no_futura" BEFORE INSERT OR UPDATE OF manufactured_at ON public.cylinder FOR EACH ROW EXECUTE FUNCTION public.fabricacion_de_envase_no_futura();


--
-- Name: cylinder TRG_cylinder_transicion_de_estado; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_cylinder_transicion_de_estado" BEFORE UPDATE OF state ON public.cylinder FOR EACH ROW EXECUTE FUNCTION public.transicion_de_estado_cylinder();


--
-- Name: driver_liquidation TRG_driver_liquidation_transicion_de_estado; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_driver_liquidation_transicion_de_estado" BEFORE UPDATE OF status ON public.driver_liquidation FOR EACH ROW EXECUTE FUNCTION public.transicion_de_estado_driver_liquidation();


--
-- Name: driver_settlement TRG_driver_settlement_fecha_futura; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_driver_settlement_fecha_futura" BEFORE INSERT ON public.driver_settlement FOR EACH ROW EXECUTE FUNCTION public.rendicion_sin_fecha_futura();


--
-- Name: driver_settlement TRG_driver_settlement_transicion_de_estado; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_driver_settlement_transicion_de_estado" BEFORE UPDATE OF status ON public.driver_settlement FOR EACH ROW EXECUTE FUNCTION public.transicion_de_estado_driver_settlement();


--
-- Name: fuel_load TRG_fuel_load_odometro_monotono; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_fuel_load_odometro_monotono" BEFORE INSERT OR UPDATE OF odometer_km, loaded_at, car_id, "deletedAt" ON public.fuel_load FOR EACH ROW EXECUTE FUNCTION public.odometro_de_carga_monotono();


--
-- Name: maintenance_task TRG_maintenance_task_odometro_monotono; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_maintenance_task_odometro_monotono" BEFORE INSERT OR UPDATE OF odometer_km, performed_at, status, car_id ON public.maintenance_task FOR EACH ROW EXECUTE FUNCTION public.odometro_de_tarea_monotono();


--
-- Name: order_dispatch_offer TRG_order_dispatch_offer_transicion_de_estado; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_order_dispatch_offer_transicion_de_estado" BEFORE UPDATE OF status ON public.order_dispatch_offer FOR EACH ROW EXECUTE FUNCTION public.transicion_de_estado_order_dispatch_offer();


--
-- Name: order TRG_order_transicion_de_estado; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_order_transicion_de_estado" BEFORE UPDATE OF status ON public."order" FOR EACH ROW EXECUTE FUNCTION public.transicion_de_estado_order();


--
-- Name: payment TRG_payment_estado_no_retrocede; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_payment_estado_no_retrocede" BEFORE UPDATE OF status ON public.payment FOR EACH ROW EXECUTE FUNCTION public.payment_estado_no_retrocede();


--
-- Name: purchase_order TRG_purchase_order_transicion_de_estado; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_purchase_order_transicion_de_estado" BEFORE UPDATE OF status ON public.purchase_order FOR EACH ROW EXECUTE FUNCTION public.transicion_de_estado_purchase_order();


--
-- Name: stock_balance TRG_stock_balance_saldo_contra_libro; Type: TRIGGER; Schema: public; Owner: -
--

CREATE CONSTRAINT TRIGGER "TRG_stock_balance_saldo_contra_libro" AFTER INSERT OR UPDATE OF quantity ON public.stock_balance DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION public.verificar_existencia_del_saldo();


--
-- Name: stock_movement TRG_stock_movement_saldo_contra_libro; Type: TRIGGER; Schema: public; Owner: -
--

CREATE CONSTRAINT TRIGGER "TRG_stock_movement_saldo_contra_libro" AFTER INSERT ON public.stock_movement DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION public.verificar_existencia_del_movimiento();


--
-- Name: tire_event TRG_tire_event_odometro_monotono; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_tire_event_odometro_monotono" BEFORE INSERT ON public.tire_event FOR EACH ROW EXECUTE FUNCTION public.odometro_de_neumatico_monotono();


--
-- Name: truck_load TRG_truck_load_transicion_de_estado; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER "TRG_truck_load_transicion_de_estado" BEFORE UPDATE OF status ON public.truck_load FOR EACH ROW EXECUTE FUNCTION public.transicion_de_estado_truck_load();


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
-- Name: cash_movement cash_movement_solo_agregar; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER cash_movement_solo_agregar BEFORE DELETE OR UPDATE ON public.cash_movement FOR EACH ROW EXECUTE FUNCTION public.libro_de_solo_agregar();


--
-- Name: commission_entry commission_entry_solo_agregar; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER commission_entry_solo_agregar BEFORE DELETE OR UPDATE ON public.commission_entry FOR EACH ROW EXECUTE FUNCTION public.libro_de_solo_agregar();


--
-- Name: customer_account_entry customer_account_entry_solo_agregar; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER customer_account_entry_solo_agregar BEFORE DELETE OR UPDATE ON public.customer_account_entry FOR EACH ROW EXECUTE FUNCTION public.libro_de_solo_agregar();


--
-- Name: employee_leave employee_leave_no_overlap; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER employee_leave_no_overlap BEFORE INSERT OR UPDATE ON public.employee_leave FOR EACH ROW EXECUTE FUNCTION public.employee_leave_no_overlap();


--
-- Name: stock_movement stock_movement_inmutable; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER stock_movement_inmutable BEFORE DELETE OR UPDATE ON public.stock_movement FOR EACH ROW EXECUTE FUNCTION public.stock_movement_inmutable();


--
-- Name: driver_settlement_order FK_00b78dc2e95eff06336c982de3c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement_order
    ADD CONSTRAINT "FK_00b78dc2e95eff06336c982de3c" FOREIGN KEY (settlement_id) REFERENCES public.driver_settlement(settlement_id) ON DELETE CASCADE;


--
-- Name: driver_settlement FK_034a404a6b3c046410baaccd6bf; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement
    ADD CONSTRAINT "FK_034a404a6b3c046410baaccd6bf" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: customer_account_allocation FK_040f1307a22c0877436239c49ea; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account_allocation
    ADD CONSTRAINT "FK_040f1307a22c0877436239c49ea" FOREIGN KEY (debit_entry_id) REFERENCES public.customer_account_entry(entry_id) ON DELETE RESTRICT;


--
-- Name: customer_account FK_05d48d2b9438d97c70797088f72; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account
    ADD CONSTRAINT "FK_05d48d2b9438d97c70797088f72" FOREIGN KEY (customer_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
-- Name: commission_entry FK_0b03f8315648bdfda67d1f3f4fa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_entry
    ADD CONSTRAINT "FK_0b03f8315648bdfda67d1f3f4fa" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE RESTRICT;


--
-- Name: tire_event FK_0be6bc39d234517b95e758d916f; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tire_event
    ADD CONSTRAINT "FK_0be6bc39d234517b95e758d916f" FOREIGN KEY (tire_id) REFERENCES public.tire(tire_id) ON DELETE CASCADE;


--
-- Name: maintenance_task FK_0c10df10892879498bf6037f951; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_task
    ADD CONSTRAINT "FK_0c10df10892879498bf6037f951" FOREIGN KEY (delivery_id) REFERENCES public.delivery(delivery_id) ON DELETE CASCADE;


--
-- Name: driver_liquidation FK_0c2c60d341a621185c48d35e975; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_liquidation
    ADD CONSTRAINT "FK_0c2c60d341a621185c48d35e975" FOREIGN KEY (created_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: employee_leave FK_0c529fe51d5cdcf84876085d637; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_leave
    ADD CONSTRAINT "FK_0c529fe51d5cdcf84876085d637" FOREIGN KEY (decided_by_user_id) REFERENCES public."user"(user_id) ON DELETE SET NULL;


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
-- Name: driver_settlement_order FK_1022fc8018671046aefdab2f8fd; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement_order
    ADD CONSTRAINT "FK_1022fc8018671046aefdab2f8fd" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE RESTRICT;


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
-- Name: customer_account_entry FK_1401ec5da7e64330b406b3fbfa9; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account_entry
    ADD CONSTRAINT "FK_1401ec5da7e64330b406b3fbfa9" FOREIGN KEY (collected_by_delivery_id) REFERENCES public.delivery(delivery_id) ON DELETE RESTRICT;


--
-- Name: cash_category FK_1528db3a4ea037a767795b0d9c9; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_category
    ADD CONSTRAINT "FK_1528db3a4ea037a767795b0d9c9" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: customer_account_allocation FK_15d961bae7cbf44cda5649a10a6; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account_allocation
    ADD CONSTRAINT "FK_15d961bae7cbf44cda5649a10a6" FOREIGN KEY (credit_entry_id) REFERENCES public.customer_account_entry(entry_id) ON DELETE RESTRICT;


--
-- Name: driver_settlement FK_1751ff46c2e373bb36f760c3607; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement
    ADD CONSTRAINT "FK_1751ff46c2e373bb36f760c3607" FOREIGN KEY (truck_load_id) REFERENCES public.truck_load(load_id) ON DELETE RESTRICT;


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
-- Name: tire FK_1aacb8a04f755929167e6f8117d; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tire
    ADD CONSTRAINT "FK_1aacb8a04f755929167e6f8117d" FOREIGN KEY (car_id) REFERENCES public.car(car_id) ON DELETE SET NULL;


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
    ADD CONSTRAINT "FK_1ca7d5228cf9dc589b60243933c" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE RESTRICT;


--
-- Name: cylinder_inspection FK_1cbfd2007890911e8b42d207d4b; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_inspection
    ADD CONSTRAINT "FK_1cbfd2007890911e8b42d207d4b" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: vehicle_accident FK_1e015d25e77f2e6f5174cb1036c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_accident
    ADD CONSTRAINT "FK_1e015d25e77f2e6f5174cb1036c" FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE SET NULL;


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
-- Name: vehicle_accident FK_2000ad7aae034d1996f07d9efda; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_accident
    ADD CONSTRAINT "FK_2000ad7aae034d1996f07d9efda" FOREIGN KEY (created_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
-- Name: customer_account_entry FK_24670e6df94198c58ad163ecce4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account_entry
    ADD CONSTRAINT "FK_24670e6df94198c58ad163ecce4" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE RESTRICT;


--
-- Name: maintenance_window_proposal FK_24b20b6fcfe92abf85bc56c9072; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_window_proposal
    ADD CONSTRAINT "FK_24b20b6fcfe92abf85bc56c9072" FOREIGN KEY (delivery_id) REFERENCES public.delivery(delivery_id) ON DELETE CASCADE;


--
-- Name: cash_session FK_24c1c29632e21025336adc2d2c1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_session
    ADD CONSTRAINT "FK_24c1c29632e21025336adc2d2c1" FOREIGN KEY (opened_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: maintenance_task FK_296b62bd1680483d20f2652e62f; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_task
    ADD CONSTRAINT "FK_296b62bd1680483d20f2652e62f" FOREIGN KEY (plan_id) REFERENCES public.maintenance_plan(plan_id) ON DELETE RESTRICT;


--
-- Name: user_address FK_29d6df815a78e4c8291d3cf5e53; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_address
    ADD CONSTRAINT "FK_29d6df815a78e4c8291d3cf5e53" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
-- Name: employee_attendance FK_2f436573780c5731f76c5833944; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_attendance
    ADD CONSTRAINT "FK_2f436573780c5731f76c5833944" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: stock_adjustment_item FK_2fa4ce3625472a3239024cc8312; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_adjustment_item
    ADD CONSTRAINT "FK_2fa4ce3625472a3239024cc8312" FOREIGN KEY (adjustment_id) REFERENCES public.stock_adjustment(adjustment_id) ON DELETE CASCADE;


--
-- Name: cash_movement FK_309ab225b94de04ab0ee244d6a9; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_movement
    ADD CONSTRAINT "FK_309ab225b94de04ab0ee244d6a9" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: truck_load FK_30e302bc956545af9282a1c43c4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load
    ADD CONSTRAINT "FK_30e302bc956545af9282a1c43c4" FOREIGN KEY (helper_employee_id) REFERENCES public.employee(employee_id) ON DELETE RESTRICT;


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
-- Name: driver_settlement FK_353df4e2e3c3e8ffca5e83f1ede; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement
    ADD CONSTRAINT "FK_353df4e2e3c3e8ffca5e83f1ede" FOREIGN KEY (approved_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: traffic_fine FK_367a6b8c0709f0a75bb2102ed37; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic_fine
    ADD CONSTRAINT "FK_367a6b8c0709f0a75bb2102ed37" FOREIGN KEY (car_id) REFERENCES public.car(car_id) ON DELETE CASCADE;


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
-- Name: customer_account_entry FK_39f5f1bf029ec0921d6c9d81795; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account_entry
    ADD CONSTRAINT "FK_39f5f1bf029ec0921d6c9d81795" FOREIGN KEY (cash_movement_id) REFERENCES public.cash_movement(movement_id) ON DELETE RESTRICT;


--
-- Name: truck_load FK_3b6b13c2d3f23575097fca51f2b; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load
    ADD CONSTRAINT "FK_3b6b13c2d3f23575097fca51f2b" FOREIGN KEY (opened_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: commission_entry FK_3c627d2c84dbd71130d917eb276; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_entry
    ADD CONSTRAINT "FK_3c627d2c84dbd71130d917eb276" FOREIGN KEY (delivery_id) REFERENCES public.delivery(delivery_id) ON DELETE RESTRICT;


--
-- Name: commission_entry FK_3cdb19a54a48a911ecedbc38841; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_entry
    ADD CONSTRAINT "FK_3cdb19a54a48a911ecedbc38841" FOREIGN KEY (rule_id) REFERENCES public.commission_rule(rule_id) ON DELETE SET NULL;


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
-- Name: customer_account_entry FK_3f917672bdb3f9fa953b197a1d6; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account_entry
    ADD CONSTRAINT "FK_3f917672bdb3f9fa953b197a1d6" FOREIGN KEY (account_id) REFERENCES public.customer_account(account_id) ON DELETE RESTRICT;


--
-- Name: stock_balance FK_425c43cce61e9a14028ec1115d1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_balance
    ADD CONSTRAINT "FK_425c43cce61e9a14028ec1115d1" FOREIGN KEY (gas_cylinder_id) REFERENCES public.gas_cylinder(gas_cylinder_id) ON DELETE RESTRICT;


--
-- Name: truck_load_item FK_440db97a6d338b1392d613087c6; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load_item
    ADD CONSTRAINT "FK_440db97a6d338b1392d613087c6" FOREIGN KEY (load_id) REFERENCES public.truck_load(load_id) ON DELETE CASCADE;


--
-- Name: customer_account_entry FK_461301da4afa2be775baa570c22; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account_entry
    ADD CONSTRAINT "FK_461301da4afa2be775baa570c22" FOREIGN KEY (created_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
    ADD CONSTRAINT "FK_4c82c1fe16612f55a925ec87741" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE RESTRICT;


--
-- Name: truck_load FK_4d54b2fe75eceaccd133cd852c8; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load
    ADD CONSTRAINT "FK_4d54b2fe75eceaccd133cd852c8" FOREIGN KEY (closed_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: tire FK_4d9a885cbe45d32a05b0083b906; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tire
    ADD CONSTRAINT "FK_4d9a885cbe45d32a05b0083b906" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: driver_settlement FK_4e7b4890ff3e759f07c7c215501; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement
    ADD CONSTRAINT "FK_4e7b4890ff3e759f07c7c215501" FOREIGN KEY (destination_cash_box_id) REFERENCES public.cash_box(cash_box_id) ON DELETE RESTRICT;


--
-- Name: employee_attendance FK_4ea40b73b24bf50777c9601f180; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_attendance
    ADD CONSTRAINT "FK_4ea40b73b24bf50777c9601f180" FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE RESTRICT;


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
-- Name: customer_account FK_564bc79a7c5208b8a2e451f33ee; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account
    ADD CONSTRAINT "FK_564bc79a7c5208b8a2e451f33ee" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: cash_session FK_566ccda1abee03369e83fbdac52; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_session
    ADD CONSTRAINT "FK_566ccda1abee03369e83fbdac52" FOREIGN KEY (cash_box_id) REFERENCES public.cash_box(cash_box_id) ON DELETE RESTRICT;


--
-- Name: driver_liquidation FK_573612e2fab26969026ec1af128; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_liquidation
    ADD CONSTRAINT "FK_573612e2fab26969026ec1af128" FOREIGN KEY (paid_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
-- Name: truck_load FK_587a7d9c99ceae48a3642c8d4bb; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load
    ADD CONSTRAINT "FK_587a7d9c99ceae48a3642c8d4bb" FOREIGN KEY (car_id) REFERENCES public.car(car_id) ON DELETE RESTRICT;


--
-- Name: driver_settlement_collection FK_5a1110f63b59aadf68c65085ee0; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement_collection
    ADD CONSTRAINT "FK_5a1110f63b59aadf68c65085ee0" FOREIGN KEY (entry_id) REFERENCES public.customer_account_entry(entry_id) ON DELETE RESTRICT;


--
-- Name: customer FK_5d1f609371a285123294fddcf3a; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT "FK_5d1f609371a285123294fddcf3a" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: traffic_fine FK_5d3ee796a650efff7dc859091cf; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic_fine
    ADD CONSTRAINT "FK_5d3ee796a650efff7dc859091cf" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: driver_liquidation FK_5ed664156f365d251740f9643f6; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_liquidation
    ADD CONSTRAINT "FK_5ed664156f365d251740f9643f6" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: traffic_fine FK_61447819bfe7d42839be95fb820; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic_fine
    ADD CONSTRAINT "FK_61447819bfe7d42839be95fb820" FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE SET NULL;


--
-- Name: audit_log FK_617015cb20b8887ecb699504a84; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_log
    ADD CONSTRAINT "FK_617015cb20b8887ecb699504a84" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE SET NULL;


--
-- Name: customer_account_allocation FK_61ea8a58fa0af69e8d60b92da68; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account_allocation
    ADD CONSTRAINT "FK_61ea8a58fa0af69e8d60b92da68" FOREIGN KEY (account_id) REFERENCES public.customer_account(account_id) ON DELETE RESTRICT;


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
-- Name: driver_liquidation FK_74adb440c22c7f7036811c76599; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_liquidation
    ADD CONSTRAINT "FK_74adb440c22c7f7036811c76599" FOREIGN KEY (approved_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: driver_settlement FK_75d32540838e7084b7c0eb113e0; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement
    ADD CONSTRAINT "FK_75d32540838e7084b7c0eb113e0" FOREIGN KEY (cash_movement_id) REFERENCES public.cash_movement(movement_id) ON DELETE RESTRICT;


--
-- Name: fuel_load FK_76c156efd52997ef49bfd8a9b9f; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fuel_load
    ADD CONSTRAINT "FK_76c156efd52997ef49bfd8a9b9f" FOREIGN KEY (car_id) REFERENCES public.car(car_id) ON DELETE CASCADE;


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
-- Name: commission_rule FK_7b250de6da53a02d3a91d255a68; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_rule
    ADD CONSTRAINT "FK_7b250de6da53a02d3a91d255a68" FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE RESTRICT;


--
-- Name: tire_event FK_7b5154eec31cbcbdb3b14456b21; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tire_event
    ADD CONSTRAINT "FK_7b5154eec31cbcbdb3b14456b21" FOREIGN KEY (car_id) REFERENCES public.car(car_id) ON DELETE SET NULL;


--
-- Name: maintenance_plan FK_7ee5533ee6d3b24f7d74a2c61ce; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_plan
    ADD CONSTRAINT "FK_7ee5533ee6d3b24f7d74a2c61ce" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: driver_settlement_expense FK_81dfc131cc2b6c5d5aa5b4a854f; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement_expense
    ADD CONSTRAINT "FK_81dfc131cc2b6c5d5aa5b4a854f" FOREIGN KEY (settlement_id) REFERENCES public.driver_settlement(settlement_id) ON DELETE CASCADE;


--
-- Name: order_dispatch_offer FK_830f3888d1424414675f1c184d9; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_dispatch_offer
    ADD CONSTRAINT "FK_830f3888d1424414675f1c184d9" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: maintenance_task FK_8358c952b2c0b0dab8df7965f83; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.maintenance_task
    ADD CONSTRAINT "FK_8358c952b2c0b0dab8df7965f83" FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE CASCADE;


--
-- Name: vehicle_accident FK_83c35413f94f6c3a1c8c05ad4f1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_accident
    ADD CONSTRAINT "FK_83c35413f94f6c3a1c8c05ad4f1" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: driver_settlement FK_841e7f13d74799b8be10aab1fbf; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement
    ADD CONSTRAINT "FK_841e7f13d74799b8be10aab1fbf" FOREIGN KEY (delivery_id) REFERENCES public.delivery(delivery_id) ON DELETE RESTRICT;


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
    ADD CONSTRAINT "FK_8a89ba6c226022354d0d8b4ada0" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE RESTRICT;


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
-- Name: commission_rule FK_8c9d53a2fe9227838bf1790976a; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_rule
    ADD CONSTRAINT "FK_8c9d53a2fe9227838bf1790976a" FOREIGN KEY (gas_cylinder_id) REFERENCES public.gas_cylinder(gas_cylinder_id) ON DELETE RESTRICT;


--
-- Name: vehicle_usage_log FK_8d4be9c7008fc808b4900a83a5d; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_usage_log
    ADD CONSTRAINT "FK_8d4be9c7008fc808b4900a83a5d" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: cash_movement FK_8e5c5ff29d543ee1e3a3d26a4a7; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_movement
    ADD CONSTRAINT "FK_8e5c5ff29d543ee1e3a3d26a4a7" FOREIGN KEY (reverses_movement_id) REFERENCES public.cash_movement(movement_id) ON DELETE RESTRICT;


--
-- Name: order_item FK_8ea8fa760695e81b4624345fc72; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_item
    ADD CONSTRAINT "FK_8ea8fa760695e81b4624345fc72" FOREIGN KEY (gas_cylinder_id) REFERENCES public.gas_cylinder(gas_cylinder_id);


--
-- Name: cash_session FK_8fd04897962bec0681603f29421; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_session
    ADD CONSTRAINT "FK_8fd04897962bec0681603f29421" FOREIGN KEY (closed_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
-- Name: commission_rule FK_93f6151205640d2f5a157024b35; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_rule
    ADD CONSTRAINT "FK_93f6151205640d2f5a157024b35" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


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
-- Name: payment_refund FK_9649d0833082fad8f431ff1381f; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_refund
    ADD CONSTRAINT "FK_9649d0833082fad8f431ff1381f" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


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
-- Name: vehicle_accident FK_99b58b33529b87aebd788f77686; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_accident
    ADD CONSTRAINT "FK_99b58b33529b87aebd788f77686" FOREIGN KEY (car_id) REFERENCES public.car(car_id) ON DELETE CASCADE;


--
-- Name: payment_refund FK_9b1ba9fb797de22fc87b598f509; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_refund
    ADD CONSTRAINT "FK_9b1ba9fb797de22fc87b598f509" FOREIGN KEY (payment_id) REFERENCES public.payment(payment_id) ON DELETE RESTRICT;


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
-- Name: commission_entry FK_a0c3335a8b5af840c818b5334a0; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_entry
    ADD CONSTRAINT "FK_a0c3335a8b5af840c818b5334a0" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


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
    ADD CONSTRAINT "FK_a28028ba709cd7e5053a86857b4" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: delivery FK_a3b8af1ce2f6e143d416d83080a; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.delivery
    ADD CONSTRAINT "FK_a3b8af1ce2f6e143d416d83080a" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
-- Name: commission_entry FK_a53df91c9e50ec2b0ebd364ad9a; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_entry
    ADD CONSTRAINT "FK_a53df91c9e50ec2b0ebd364ad9a" FOREIGN KEY (created_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
-- Name: fuel_load FK_a70b641640176492d8d0634b818; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fuel_load
    ADD CONSTRAINT "FK_a70b641640176492d8d0634b818" FOREIGN KEY (created_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: employee_leave FK_a7720c43add56423460fa1a2aaa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_leave
    ADD CONSTRAINT "FK_a7720c43add56423460fa1a2aaa" FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE RESTRICT;


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
-- Name: cash_movement FK_a9b982c8aec7c799a146f449e25; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_movement
    ADD CONSTRAINT "FK_a9b982c8aec7c799a146f449e25" FOREIGN KEY (cash_box_id) REFERENCES public.cash_box(cash_box_id) ON DELETE RESTRICT;


--
-- Name: truck_load_item FK_aab2bf3823dbe43254226112845; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load_item
    ADD CONSTRAINT "FK_aab2bf3823dbe43254226112845" FOREIGN KEY (gas_cylinder_id) REFERENCES public.gas_cylinder(gas_cylinder_id) ON DELETE RESTRICT;


--
-- Name: claims FK_af79ab775a51930eb21951a3c95; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims
    ADD CONSTRAINT "FK_af79ab775a51930eb21951a3c95" FOREIGN KEY (customer_id) REFERENCES public."user"(user_id);


--
-- Name: truck_load FK_b075736a27f0d8accf03d6412a9; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load
    ADD CONSTRAINT "FK_b075736a27f0d8accf03d6412a9" FOREIGN KEY (delivery_id) REFERENCES public.delivery(delivery_id) ON DELETE RESTRICT;


--
-- Name: cash_movement FK_b1f34c53c367143701b9164785e; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_movement
    ADD CONSTRAINT "FK_b1f34c53c367143701b9164785e" FOREIGN KEY (category_id) REFERENCES public.cash_category(category_id) ON DELETE RESTRICT;


--
-- Name: purchase_receipt_item FK_b391d5552738cae006c0b9bf801; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt_item
    ADD CONSTRAINT "FK_b391d5552738cae006c0b9bf801" FOREIGN KEY (receipt_id) REFERENCES public.purchase_receipt(receipt_id) ON DELETE CASCADE;


--
-- Name: truck_load FK_b446f9041a2b069fabf41a1ee5e; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load
    ADD CONSTRAINT "FK_b446f9041a2b069fabf41a1ee5e" FOREIGN KEY (origin_location_id) REFERENCES public.stock_location(location_id) ON DELETE RESTRICT;


--
-- Name: rating FK_b46b63fc1ddf2135e1ed37069a9; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT "FK_b46b63fc1ddf2135e1ed37069a9" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id);


--
-- Name: cash_movement FK_b4ddcca770fe0f7b5b7c8131d25; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_movement
    ADD CONSTRAINT "FK_b4ddcca770fe0f7b5b7c8131d25" FOREIGN KEY (created_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


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
-- Name: commission_entry FK_b7d839b89e77ecff89abda761e5; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_entry
    ADD CONSTRAINT "FK_b7d839b89e77ecff89abda761e5" FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE RESTRICT;


--
-- Name: employee_leave FK_b8923c061b86827456de74e7ea8; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_leave
    ADD CONSTRAINT "FK_b8923c061b86827456de74e7ea8" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: module_config FK_ba2e1f43e70ba77c13d6844ee84; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.module_config
    ADD CONSTRAINT "FK_ba2e1f43e70ba77c13d6844ee84" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: rating FK_beb6f44b22a7f1ed7cad984a2e1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT "FK_beb6f44b22a7f1ed7cad984a2e1" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE RESTRICT;


--
-- Name: purchase_order FK_c00afbc3e2836ac46be7c45ca78; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT "FK_c00afbc3e2836ac46be7c45ca78" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: truck_load FK_c023820beebd76607bbe400ba17; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load
    ADD CONSTRAINT "FK_c023820beebd76607bbe400ba17" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


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
-- Name: tire_event FK_c88fcd0fe7dc9f9228db77cfb6f; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tire_event
    ADD CONSTRAINT "FK_c88fcd0fe7dc9f9228db77cfb6f" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: car FK_c8d34198d86de9e96aae03b8990; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.car
    ADD CONSTRAINT "FK_c8d34198d86de9e96aae03b8990" FOREIGN KEY (user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: purchase_receipt FK_c92afda2aff490f63e02ea303bb; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt
    ADD CONSTRAINT "FK_c92afda2aff490f63e02ea303bb" FOREIGN KEY (received_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: cash_movement FK_cash_movement_cash_box_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_movement
    ADD CONSTRAINT "FK_cash_movement_cash_box_distribuidora" FOREIGN KEY (cash_box_id, distributor_id) REFERENCES public.cash_box(cash_box_id, distributor_id);


--
-- Name: cash_movement FK_cash_movement_category_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_movement
    ADD CONSTRAINT "FK_cash_movement_category_distribuidora" FOREIGN KEY (category_id, distributor_id) REFERENCES public.cash_category(category_id, distributor_id);


--
-- Name: cash_movement FK_cash_movement_reverses_movement_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_movement
    ADD CONSTRAINT "FK_cash_movement_reverses_movement_distribuidora" FOREIGN KEY (reverses_movement_id, distributor_id) REFERENCES public.cash_movement(movement_id, distributor_id);


--
-- Name: cash_movement FK_cash_movement_session_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_movement
    ADD CONSTRAINT "FK_cash_movement_session_distribuidora" FOREIGN KEY (session_id, distributor_id) REFERENCES public.cash_session(session_id, distributor_id);


--
-- Name: cash_session FK_cash_session_cash_box_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_session
    ADD CONSTRAINT "FK_cash_session_cash_box_distribuidora" FOREIGN KEY (cash_box_id, distributor_id) REFERENCES public.cash_box(cash_box_id, distributor_id);


--
-- Name: cash_session FK_cba986fb1ad57b98770e517d9b8; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_session
    ADD CONSTRAINT "FK_cba986fb1ad57b98770e517d9b8" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


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
-- Name: cash_box FK_cf2a6266f8dc0f2d942fe88aa6e; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_box
    ADD CONSTRAINT "FK_cf2a6266f8dc0f2d942fe88aa6e" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: claims FK_claims_order_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.claims
    ADD CONSTRAINT "FK_claims_order_distribuidora" FOREIGN KEY (order_id, distributor_id) REFERENCES public."order"(order_id, distributor_id);


--
-- Name: commission_entry FK_commission_entry_delivery_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_entry
    ADD CONSTRAINT "FK_commission_entry_delivery_distribuidora" FOREIGN KEY (delivery_id, distributor_id) REFERENCES public.delivery(delivery_id, distributor_id);


--
-- Name: commission_entry FK_commission_entry_employee_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_entry
    ADD CONSTRAINT "FK_commission_entry_employee_distribuidora" FOREIGN KEY (employee_id, distributor_id) REFERENCES public.employee(employee_id, distributor_id);


--
-- Name: commission_entry FK_commission_entry_liquidation_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_entry
    ADD CONSTRAINT "FK_commission_entry_liquidation_distribuidora" FOREIGN KEY (liquidation_id, distributor_id) REFERENCES public.driver_liquidation(liquidation_id, distributor_id);


--
-- Name: commission_entry FK_commission_entry_order_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_entry
    ADD CONSTRAINT "FK_commission_entry_order_distribuidora" FOREIGN KEY (order_id, distributor_id) REFERENCES public."order"(order_id, distributor_id);


--
-- Name: customer_account_entry FK_customer_account_entry_account_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account_entry
    ADD CONSTRAINT "FK_customer_account_entry_account_distribuidora" FOREIGN KEY (account_id, distributor_id) REFERENCES public.customer_account(account_id, distributor_id);


--
-- Name: customer_account_entry FK_customer_account_entry_cash_movement_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account_entry
    ADD CONSTRAINT "FK_customer_account_entry_cash_movement_distribuidora" FOREIGN KEY (cash_movement_id, distributor_id) REFERENCES public.cash_movement(movement_id, distributor_id);


--
-- Name: customer_account_entry FK_customer_account_entry_collected_by_delivery_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account_entry
    ADD CONSTRAINT "FK_customer_account_entry_collected_by_delivery_distribuidora" FOREIGN KEY (collected_by_delivery_id, distributor_id) REFERENCES public.delivery(delivery_id, distributor_id);


--
-- Name: customer_account_entry FK_customer_account_entry_order_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account_entry
    ADD CONSTRAINT "FK_customer_account_entry_order_distribuidora" FOREIGN KEY (order_id, distributor_id) REFERENCES public."order"(order_id, distributor_id);


--
-- Name: cylinder FK_cylinder_current_order_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder
    ADD CONSTRAINT "FK_cylinder_current_order_distribuidora" FOREIGN KEY (current_order_id, distributor_id) REFERENCES public."order"(order_id, distributor_id);


--
-- Name: cylinder FK_cylinder_gas_cylinder_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder
    ADD CONSTRAINT "FK_cylinder_gas_cylinder_distribuidora" FOREIGN KEY (gas_cylinder_id, distributor_id) REFERENCES public.gas_cylinder(gas_cylinder_id, distributor_id);


--
-- Name: cylinder_inspection FK_cylinder_inspection_cylinder_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_inspection
    ADD CONSTRAINT "FK_cylinder_inspection_cylinder_distribuidora" FOREIGN KEY (cylinder_id, distributor_id) REFERENCES public.cylinder(cylinder_id, distributor_id);


--
-- Name: cylinder_movement FK_cylinder_movement_cylinder_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_movement
    ADD CONSTRAINT "FK_cylinder_movement_cylinder_distribuidora" FOREIGN KEY (cylinder_id, distributor_id) REFERENCES public.cylinder(cylinder_id, distributor_id);


--
-- Name: cylinder_movement FK_cylinder_movement_order_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cylinder_movement
    ADD CONSTRAINT "FK_cylinder_movement_order_distribuidora" FOREIGN KEY (order_id, distributor_id) REFERENCES public."order"(order_id, distributor_id);


--
-- Name: fuel_load FK_d083e0be3bb71d18990f4d76153; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fuel_load
    ADD CONSTRAINT "FK_d083e0be3bb71d18990f4d76153" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: audit FK_d214d146099cc53049201a1efd5; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit
    ADD CONSTRAINT "FK_d214d146099cc53049201a1efd5" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE SET NULL;


--
-- Name: employee_leave FK_d417e890ac4cb96aaa6da2fb239; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_leave
    ADD CONSTRAINT "FK_d417e890ac4cb96aaa6da2fb239" FOREIGN KEY (requested_by_user_id) REFERENCES public."user"(user_id) ON DELETE SET NULL;


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
-- Name: cash_movement FK_d704d3ac4a86b13e238da3d4083; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cash_movement
    ADD CONSTRAINT "FK_d704d3ac4a86b13e238da3d4083" FOREIGN KEY (session_id) REFERENCES public.cash_session(session_id) ON DELETE RESTRICT;


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
-- Name: customer_account_entry FK_d9a03fad3dae8ac9c53de957b96; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customer_account_entry
    ADD CONSTRAINT "FK_d9a03fad3dae8ac9c53de957b96" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: tire_event FK_d9e58b451d933032d487f8b08e5; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tire_event
    ADD CONSTRAINT "FK_d9e58b451d933032d487f8b08e5" FOREIGN KEY (created_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: driver_settlement FK_dce1f0f1e826575bf49d6a5776f; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement
    ADD CONSTRAINT "FK_dce1f0f1e826575bf49d6a5776f" FOREIGN KEY (submitted_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: payment_refund FK_ddf9b0a3d9abeee97fa77f0f204; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_refund
    ADD CONSTRAINT "FK_ddf9b0a3d9abeee97fa77f0f204" FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE RESTRICT;


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
-- Name: driver_liquidation FK_driver_liquidation_cash_movement_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_liquidation
    ADD CONSTRAINT "FK_driver_liquidation_cash_movement_distribuidora" FOREIGN KEY (cash_movement_id, distributor_id) REFERENCES public.cash_movement(movement_id, distributor_id);


--
-- Name: driver_liquidation FK_driver_liquidation_employee_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_liquidation
    ADD CONSTRAINT "FK_driver_liquidation_employee_distribuidora" FOREIGN KEY (employee_id, distributor_id) REFERENCES public.employee(employee_id, distributor_id);


--
-- Name: driver_settlement FK_driver_settlement_cash_movement_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement
    ADD CONSTRAINT "FK_driver_settlement_cash_movement_distribuidora" FOREIGN KEY (cash_movement_id, distributor_id) REFERENCES public.cash_movement(movement_id, distributor_id);


--
-- Name: driver_settlement FK_driver_settlement_delivery_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement
    ADD CONSTRAINT "FK_driver_settlement_delivery_distribuidora" FOREIGN KEY (delivery_id, distributor_id) REFERENCES public.delivery(delivery_id, distributor_id);


--
-- Name: driver_settlement FK_driver_settlement_destination_cash_box_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement
    ADD CONSTRAINT "FK_driver_settlement_destination_cash_box_distribuidora" FOREIGN KEY (destination_cash_box_id, distributor_id) REFERENCES public.cash_box(cash_box_id, distributor_id);


--
-- Name: driver_settlement FK_driver_settlement_truck_load_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement
    ADD CONSTRAINT "FK_driver_settlement_truck_load_distribuidora" FOREIGN KEY (truck_load_id, distributor_id) REFERENCES public.truck_load(load_id, distributor_id);


--
-- Name: driver_settlement_expense FK_e1279555100a50a59f7d6225db7; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement_expense
    ADD CONSTRAINT "FK_e1279555100a50a59f7d6225db7" FOREIGN KEY (category_id) REFERENCES public.cash_category(category_id) ON DELETE RESTRICT;


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
-- Name: employee_attendance FK_e8e6684056188b645f01dc2f24e; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.employee_attendance
    ADD CONSTRAINT "FK_e8e6684056188b645f01dc2f24e" FOREIGN KEY (recorded_by_user_id) REFERENCES public."user"(user_id) ON DELETE SET NULL;


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
-- Name: fuel_load FK_ee48925b2fcea12a694e512681c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fuel_load
    ADD CONSTRAINT "FK_ee48925b2fcea12a694e512681c" FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE SET NULL;


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
-- Name: driver_liquidation FK_f87255c83855b6e635e95862da8; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_liquidation
    ADD CONSTRAINT "FK_f87255c83855b6e635e95862da8" FOREIGN KEY (employee_id) REFERENCES public.employee(employee_id) ON DELETE RESTRICT;


--
-- Name: driver_liquidation FK_f897f43191611d24ac38cb9f3da; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_liquidation
    ADD CONSTRAINT "FK_f897f43191611d24ac38cb9f3da" FOREIGN KEY (cash_movement_id) REFERENCES public.cash_movement(movement_id) ON DELETE RESTRICT;


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
-- Name: commission_entry FK_feba91de77750347b3623fcf849; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.commission_entry
    ADD CONSTRAINT "FK_feba91de77750347b3623fcf849" FOREIGN KEY (liquidation_id) REFERENCES public.driver_liquidation(liquidation_id) ON DELETE RESTRICT;


--
-- Name: driver_settlement_collection FK_ffffe9c244ec6bc721223a622a6; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.driver_settlement_collection
    ADD CONSTRAINT "FK_ffffe9c244ec6bc721223a622a6" FOREIGN KEY (settlement_id) REFERENCES public.driver_settlement(settlement_id) ON DELETE CASCADE;


--
-- Name: fuel_load FK_fuel_load_cash_movement; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fuel_load
    ADD CONSTRAINT "FK_fuel_load_cash_movement" FOREIGN KEY (cash_movement_id) REFERENCES public.cash_movement(movement_id) ON DELETE RESTRICT;


--
-- Name: fuel_load FK_fuel_load_cash_movement_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fuel_load
    ADD CONSTRAINT "FK_fuel_load_cash_movement_distribuidora" FOREIGN KEY (cash_movement_id, distributor_id) REFERENCES public.cash_movement(movement_id, distributor_id);


--
-- Name: incident FK_incident_order_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.incident
    ADD CONSTRAINT "FK_incident_order_distribuidora" FOREIGN KEY (order_id, distributor_id) REFERENCES public."order"(order_id, distributor_id);


--
-- Name: order FK_order_coverage_zone_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_order_coverage_zone_distribuidora" FOREIGN KEY (coverage_zone_id, distributor_id) REFERENCES public.coverage_zone(coverage_zone_id, distributor_id);


--
-- Name: order FK_order_delivery_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_order_delivery_distribuidora" FOREIGN KEY (delivery_id, distributor_id) REFERENCES public.delivery(delivery_id, distributor_id);


--
-- Name: order_dispatch_offer FK_order_dispatch_offer_order_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_dispatch_offer
    ADD CONSTRAINT "FK_order_dispatch_offer_order_distribuidora" FOREIGN KEY (order_id, distributor_id) REFERENCES public."order"(order_id, distributor_id);


--
-- Name: order FK_order_payment_confirmed_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_order_payment_confirmed_by" FOREIGN KEY (payment_confirmed_by) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: order FK_order_payment_resolved_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_order_payment_resolved_by" FOREIGN KEY (payment_resolved_by) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: order FK_order_time_slot_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_order_time_slot_distribuidora" FOREIGN KEY (time_slot_id, distributor_id) REFERENCES public.time_slot(time_slot_id, distributor_id);


--
-- Name: order FK_order_vehicle_car; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_order_vehicle_car" FOREIGN KEY (vehicle_car_id) REFERENCES public.car(car_id) ON DELETE SET NULL;


--
-- Name: order FK_order_vehicle_car_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."order"
    ADD CONSTRAINT "FK_order_vehicle_car_distribuidora" FOREIGN KEY (vehicle_car_id, distributor_id) REFERENCES public.car(car_id, distributor_id);


--
-- Name: payment_refund FK_payment_refund_requested_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_refund
    ADD CONSTRAINT "FK_payment_refund_requested_by" FOREIGN KEY (requested_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: purchase_order FK_purchase_order_destination_warehouse_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT "FK_purchase_order_destination_warehouse_distribuidora" FOREIGN KEY (destination_warehouse_id, distributor_id) REFERENCES public.warehouse(warehouse_id, distributor_id);


--
-- Name: purchase_order FK_purchase_order_supplier_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_order
    ADD CONSTRAINT "FK_purchase_order_supplier_distribuidora" FOREIGN KEY (supplier_id, distributor_id) REFERENCES public.supplier(supplier_id, distributor_id);


--
-- Name: purchase_receipt FK_purchase_receipt_cash_movement; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt
    ADD CONSTRAINT "FK_purchase_receipt_cash_movement" FOREIGN KEY (cash_movement_id) REFERENCES public.cash_movement(movement_id) ON DELETE RESTRICT;


--
-- Name: purchase_receipt FK_purchase_receipt_cash_movement_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt
    ADD CONSTRAINT "FK_purchase_receipt_cash_movement_distribuidora" FOREIGN KEY (cash_movement_id, distributor_id) REFERENCES public.cash_movement(movement_id, distributor_id);


--
-- Name: purchase_receipt FK_purchase_receipt_purchase_order_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt
    ADD CONSTRAINT "FK_purchase_receipt_purchase_order_distribuidora" FOREIGN KEY (purchase_order_id, distributor_id) REFERENCES public.purchase_order(purchase_order_id, distributor_id);


--
-- Name: purchase_receipt FK_purchase_receipt_supplier_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt
    ADD CONSTRAINT "FK_purchase_receipt_supplier_distribuidora" FOREIGN KEY (supplier_id, distributor_id) REFERENCES public.supplier(supplier_id, distributor_id);


--
-- Name: purchase_receipt FK_purchase_receipt_voided_by; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt
    ADD CONSTRAINT "FK_purchase_receipt_voided_by" FOREIGN KEY (voided_by_user_id) REFERENCES public."user"(user_id) ON DELETE RESTRICT;


--
-- Name: purchase_receipt FK_purchase_receipt_warehouse_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchase_receipt
    ADD CONSTRAINT "FK_purchase_receipt_warehouse_distribuidora" FOREIGN KEY (warehouse_id, distributor_id) REFERENCES public.warehouse(warehouse_id, distributor_id);


--
-- Name: rating FK_rating_order_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT "FK_rating_order_distribuidora" FOREIGN KEY (order_id, distributor_id) REFERENCES public."order"(order_id, distributor_id);


--
-- Name: stock_adjustment FK_stock_adjustment_location_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_adjustment
    ADD CONSTRAINT "FK_stock_adjustment_location_distribuidora" FOREIGN KEY (location_id, distributor_id) REFERENCES public.stock_location(location_id, distributor_id);


--
-- Name: stock_balance FK_stock_balance_gas_cylinder_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_balance
    ADD CONSTRAINT "FK_stock_balance_gas_cylinder_distribuidora" FOREIGN KEY (gas_cylinder_id, distributor_id) REFERENCES public.gas_cylinder(gas_cylinder_id, distributor_id);


--
-- Name: stock_balance FK_stock_balance_location_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_balance
    ADD CONSTRAINT "FK_stock_balance_location_distribuidora" FOREIGN KEY (location_id, distributor_id) REFERENCES public.stock_location(location_id, distributor_id);


--
-- Name: stock_location FK_stock_location_car_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_location
    ADD CONSTRAINT "FK_stock_location_car_distribuidora" FOREIGN KEY (car_id, distributor_id) REFERENCES public.car(car_id, distributor_id);


--
-- Name: stock_location FK_stock_location_warehouse_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_location
    ADD CONSTRAINT "FK_stock_location_warehouse_distribuidora" FOREIGN KEY (warehouse_id, distributor_id) REFERENCES public.warehouse(warehouse_id, distributor_id);


--
-- Name: stock_movement FK_stock_movement_from_location_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement
    ADD CONSTRAINT "FK_stock_movement_from_location_distribuidora" FOREIGN KEY (from_location_id, distributor_id) REFERENCES public.stock_location(location_id, distributor_id);


--
-- Name: stock_movement FK_stock_movement_gas_cylinder_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement
    ADD CONSTRAINT "FK_stock_movement_gas_cylinder_distribuidora" FOREIGN KEY (gas_cylinder_id, distributor_id) REFERENCES public.gas_cylinder(gas_cylinder_id, distributor_id);


--
-- Name: stock_movement FK_stock_movement_reversed_movement_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement
    ADD CONSTRAINT "FK_stock_movement_reversed_movement_distribuidora" FOREIGN KEY (reversed_movement_id, distributor_id) REFERENCES public.stock_movement(movement_id, distributor_id);


--
-- Name: stock_movement FK_stock_movement_to_location_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_movement
    ADD CONSTRAINT "FK_stock_movement_to_location_distribuidora" FOREIGN KEY (to_location_id, distributor_id) REFERENCES public.stock_location(location_id, distributor_id);


--
-- Name: stock_reconciliation_alert FK_stock_reconciliation_alert_distributor; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_reconciliation_alert
    ADD CONSTRAINT "FK_stock_reconciliation_alert_distributor" FOREIGN KEY (distributor_id) REFERENCES public.distributor(distributor_id) ON DELETE CASCADE;


--
-- Name: stock_threshold FK_stock_threshold_gas_cylinder_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_threshold
    ADD CONSTRAINT "FK_stock_threshold_gas_cylinder_distribuidora" FOREIGN KEY (gas_cylinder_id, distributor_id) REFERENCES public.gas_cylinder(gas_cylinder_id, distributor_id);


--
-- Name: stock_threshold FK_stock_threshold_warehouse_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock_threshold
    ADD CONSTRAINT "FK_stock_threshold_warehouse_distribuidora" FOREIGN KEY (warehouse_id, distributor_id) REFERENCES public.warehouse(warehouse_id, distributor_id);


--
-- Name: traffic_fine FK_traffic_fine_cash_movement; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic_fine
    ADD CONSTRAINT "FK_traffic_fine_cash_movement" FOREIGN KEY (cash_movement_id) REFERENCES public.cash_movement(movement_id) ON DELETE RESTRICT;


--
-- Name: traffic_fine FK_traffic_fine_cash_movement_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic_fine
    ADD CONSTRAINT "FK_traffic_fine_cash_movement_distribuidora" FOREIGN KEY (cash_movement_id, distributor_id) REFERENCES public.cash_movement(movement_id, distributor_id);


--
-- Name: truck_load FK_truck_load_car_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load
    ADD CONSTRAINT "FK_truck_load_car_distribuidora" FOREIGN KEY (car_id, distributor_id) REFERENCES public.car(car_id, distributor_id);


--
-- Name: truck_load FK_truck_load_delivery_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load
    ADD CONSTRAINT "FK_truck_load_delivery_distribuidora" FOREIGN KEY (delivery_id, distributor_id) REFERENCES public.delivery(delivery_id, distributor_id);


--
-- Name: truck_load FK_truck_load_helper_employee_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load
    ADD CONSTRAINT "FK_truck_load_helper_employee_distribuidora" FOREIGN KEY (helper_employee_id, distributor_id) REFERENCES public.employee(employee_id, distributor_id);


--
-- Name: truck_load FK_truck_load_origin_location_distribuidora; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.truck_load
    ADD CONSTRAINT "FK_truck_load_origin_location_distribuidora" FOREIGN KEY (origin_location_id, distributor_id) REFERENCES public.stock_location(location_id, distributor_id);


--
-- PostgreSQL database dump complete
--

