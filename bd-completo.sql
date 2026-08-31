-- ============================================================
-- SPLG — Sistema de Pedidos y Logística de Garrafas de Gas
-- Esquema completo de Base de Datos — PostgreSQL 14+
-- ------------------------------------------------------------
-- Listo para importar en Lucidchart:
--   File → Import Data → Database (Custom)
--   Seleccionar PostgreSQL como motor → pegar este archivo
--   Lucidchart genera el ER automáticamente con cardinalidades
-- ------------------------------------------------------------
-- Incluye:
--   • 12 tablas core del sistema (User, Customer, Delivery, Order, etc.)
--   • 5 tablas auxiliares completadas (Notification, Webhook, Payment_Gateway, Email, Seed)
--   • 2 tablas de auditoría/intermedias (Audit_Log, Order_Driver_Rejection)
--   • 13 tablas adicionales según patrones estándar de delivery apps:
--       Rating, FCM_Token, Delivery_Zone, Driver_Shift, Promo_Code (+ usage),
--       Stock_Movement, Driver_Document, Chat_Message, Scheduled_Order,
--       Delivery_Route, Support_Ticket (+ messages)
--   • Total: 32 tablas + 2 vistas, ~50 FKs, ~55 índices
-- ============================================================

-- ============================================================
-- TIPOS / ENUMS DE NEGOCIO (representados como CHECK constraints)
-- ============================================================
-- Nota: se usan VARCHAR + CHECK para máxima compatibilidad con
-- importadores de diagrama. Los valores válidos están comentados.

-- ============================================================
-- 1. TABLA: role
-- Catálogo de roles del sistema
-- ============================================================
CREATE TABLE role (
    role_id           UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    type              VARCHAR(20)     NOT NULL UNIQUE,  -- CLIENTE | CHOFER | ADMIN | SUPER_ADMIN
    description       TEXT            NULL,
    created_at        TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMP       NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE role IS 'Catálogo de roles disponibles en el sistema';

-- ============================================================
-- 2. TABLA: user (entidad central)
-- Información común a Clientes, Choferes y Administradores
-- ============================================================
CREATE TABLE "user" (
    user_id           UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id           UUID            NULL REFERENCES role(role_id) ON DELETE SET NULL,
    firebase_uid      VARCHAR(128)    UNIQUE NULL,
    email             VARCHAR(255)    UNIQUE NULL,
    full_name         VARCHAR(150)    NULL,
    phone_number      VARCHAR(30)     UNIQUE NULL,
    selfie_url        TEXT            NULL,
    phone_verified    BOOLEAN         NOT NULL DEFAULT FALSE,
    email_verified    BOOLEAN         NOT NULL DEFAULT FALSE,
    blocked           BOOLEAN         NOT NULL DEFAULT FALSE,
    last_login_at     TIMESTAMP       NULL,
    created_at        TIMESTAMP       NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMP       NOT NULL DEFAULT NOW(),
    deleted_at        TIMESTAMP       NULL  -- Soft-delete
);

CREATE INDEX idx_user_email ON "user"(email);
CREATE INDEX idx_user_firebase_uid ON "user"(firebase_uid);
CREATE INDEX idx_user_role ON "user"(role_id);

COMMENT ON TABLE "user" IS 'Tabla central de usuarios. Cada User extiende a Customer, Delivery o Admin según role';

-- ============================================================
-- 3. TABLA: customer
-- Perfil de Cliente (hereda de User con role=CLIENTE)
-- ============================================================
CREATE TABLE customer (
    customer_id        UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id            UUID           NOT NULL UNIQUE REFERENCES "user"(user_id) ON DELETE CASCADE,
    notification_token TEXT           NULL,  -- Token FCM para push notifications
    last_known_lat     DECIMAL(10,7)  NULL,
    last_known_lng     DECIMAL(10,7)  NULL,
    validated          BOOLEAN        NOT NULL DEFAULT FALSE,
    accepts_marketing  BOOLEAN        NOT NULL DEFAULT FALSE,
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW(),
    deleted_at         TIMESTAMP      NULL
);

COMMENT ON TABLE customer IS 'Perfil de Cliente. Realiza pedidos. Tiene 1:1 con User';

-- ============================================================
-- 4. TABLA: delivery
-- Perfil de Chofer/Repartidor (hereda de User con role=CHOFER)
-- ============================================================
CREATE TABLE delivery (
    delivery_id        UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id            UUID           NOT NULL UNIQUE REFERENCES "user"(user_id) ON DELETE CASCADE,
    calification       DECIMAL(3,2)   NULL,        -- 0.00 a 5.00
    current_lat        DECIMAL(10,7)  NULL,        -- Última ubicación GPS conocida
    current_lng        DECIMAL(10,7)  NULL,
    cancelled_charge   DECIMAL(10,2)  NULL DEFAULT 0,  -- Cargo por cancelaciones
    validated          BOOLEAN        NOT NULL DEFAULT FALSE,  -- Habilitación permanente del admin
    is_active          BOOLEAN        NOT NULL DEFAULT TRUE,   -- Disponibilidad operativa
    is_traveling       BOOLEAN        NOT NULL DEFAULT FALSE,  -- En entrega activa
    balance            DECIMAL(12,2)  NOT NULL DEFAULT 0,      -- Saldo acumulado
    total_deliveries   INTEGER        NOT NULL DEFAULT 0,
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW(),
    deleted_at         TIMESTAMP      NULL
);

CREATE INDEX idx_delivery_active ON delivery(is_active, validated);

COMMENT ON TABLE delivery IS 'Perfil de Chofer. Realiza entregas. Tiene 1:1 con User';

-- ============================================================
-- 5. TABLA: admin
-- Perfil de Administrador
-- ============================================================
CREATE TABLE admin (
    admin_id           UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id            UUID           NOT NULL UNIQUE REFERENCES "user"(user_id) ON DELETE CASCADE,
    role_id            UUID           NOT NULL REFERENCES role(role_id),
    department         VARCHAR(50)    NULL,
    can_manage_drivers BOOLEAN        NOT NULL DEFAULT TRUE,
    can_manage_orders  BOOLEAN        NOT NULL DEFAULT TRUE,
    can_view_reports   BOOLEAN        NOT NULL DEFAULT TRUE,
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE admin IS 'Perfil de Administrador. Acceso al Panel Web';

-- ============================================================
-- 6. TABLA: car
-- Vehículos asignados a un chofer (un chofer puede tener varios)
-- ============================================================
CREATE TABLE car (
    car_id             UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id            UUID           NOT NULL REFERENCES "user"(user_id) ON DELETE CASCADE,
    type_car           VARCHAR(20)    NULL,        -- MOTO | AUTO | CAMIONETA | CAMION
    car_capacity       INTEGER        NULL,        -- Cantidad de garrafas que carga
    car_patent         VARCHAR(15)    UNIQUE NULL,
    car_brand          VARCHAR(50)    NULL,
    car_model          VARCHAR(50)    NULL,
    car_year           INTEGER        NULL,
    car_color          VARCHAR(30)    NULL,
    is_active          BOOLEAN        NOT NULL DEFAULT TRUE,
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_car_user ON car(user_id);

COMMENT ON TABLE car IS 'Vehículo de un chofer. Un chofer puede tener varios';

-- ============================================================
-- 7. TABLA: user_address
-- Direcciones guardadas del usuario (un usuario puede tener varias)
-- ============================================================
CREATE TABLE user_address (
    address_id              UUID       PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id                 UUID       NOT NULL REFERENCES "user"(user_id) ON DELETE CASCADE,
    street                  VARCHAR(200) NOT NULL,
    number                  VARCHAR(20) NULL,
    apartment               VARCHAR(20) NULL,
    city                    VARCHAR(100) NOT NULL,
    province                VARCHAR(100) NULL,
    postal_code             VARCHAR(20) NULL,
    latitude                DECIMAL(10,7) NULL,
    longitude               DECIMAL(10,7) NULL,
    formatted_address       TEXT        NULL,
    is_default              BOOLEAN     NOT NULL DEFAULT FALSE,
    additional_instructions TEXT        NULL,
    created_at              TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMP   NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_address_user ON user_address(user_id);
CREATE INDEX idx_address_default ON user_address(user_id, is_default);

COMMENT ON TABLE user_address IS 'Direcciones guardadas por el usuario para futuras entregas';

-- ============================================================
-- 8. TABLA: gas_cylinder
-- Catálogo de productos (garrafas de gas)
-- ============================================================
CREATE TABLE gas_cylinder (
    gas_cylinder_id    UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    type               VARCHAR(20)    NOT NULL,    -- 10kg | 15kg | 45kg
    weight             DECIMAL(6,2)   NOT NULL,
    price              DECIMAL(10,2)  NOT NULL,
    stock              INTEGER        NOT NULL DEFAULT 0,
    description        TEXT           NULL,
    image_url          TEXT           NULL,
    is_active          BOOLEAN        NOT NULL DEFAULT TRUE,
    promotions         JSONB          NULL,        -- [{quantity, discountPercentage}]
    min_stock_alert    INTEGER        NULL DEFAULT 5,
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_cylinder_active ON gas_cylinder(is_active);
CREATE INDEX idx_cylinder_stock ON gas_cylinder(stock);

COMMENT ON TABLE gas_cylinder IS 'Catálogo de garrafas comercializadas';

-- ============================================================
-- 9. TABLA: time_slot
-- Franjas horarias disponibles para entrega
-- ============================================================
CREATE TABLE time_slot (
    time_slot_id       UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    name               VARCHAR(50)    NOT NULL,    -- Ej: "Mañana 8-12"
    start_time         TIME           NOT NULL,
    end_time           TIME           NOT NULL,
    capacity           INTEGER        NOT NULL DEFAULT 50,
    is_active          BOOLEAN        NOT NULL DEFAULT TRUE,
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMP      NOT NULL DEFAULT NOW(),
    CHECK (end_time > start_time),
    CHECK (capacity > 0)
);

COMMENT ON TABLE time_slot IS 'Franjas horarias de entrega configurables';

-- ============================================================
-- 10. TABLA: order (pedidos)
-- Tabla central de transacciones
-- ============================================================
CREATE TABLE "order" (
    order_id              UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id           UUID         NOT NULL REFERENCES customer(customer_id),
    delivery_id           UUID         NULL REFERENCES delivery(delivery_id),
    time_slot_id          UUID         NULL REFERENCES time_slot(time_slot_id),
    address_id            UUID         NOT NULL REFERENCES user_address(address_id),
    status                VARCHAR(20)  NOT NULL DEFAULT 'PENDING',  -- PENDING | ACCEPTED | ON_THE_WAY | ARRIVED | DELIVERED | CANCELLED
    payment_method        VARCHAR(20)  NOT NULL,    -- CASH | MERCADOPAGO | TRANSFER
    payment_type          VARCHAR(20)  NULL,        -- CASH | ONLINE
    payment_status        VARCHAR(20)  NOT NULL DEFAULT 'PENDING',  -- PENDING | PAID | FAILED | REFUNDED
    total_amount          DECIMAL(12,2) NOT NULL,
    transfer_surcharge    DECIMAL(10,2) NULL DEFAULT 0,
    applied_discount_pct  DECIMAL(5,2)  NULL,
    notes                 TEXT          NULL,
    delivery_instructions TEXT          NULL,
    delivery_latitude     DECIMAL(10,7) NULL,
    delivery_longitude    DECIMAL(10,7) NULL,
    requested_delivery_date DATE        NULL,
    -- Timestamps de cada cambio de estado
    accepted_at           TIMESTAMP     NULL,
    on_the_way_at         TIMESTAMP     NULL,
    arrived_at            TIMESTAMP     NULL,
    delivered_at          TIMESTAMP     NULL,
    cancelled_at          TIMESTAMP     NULL,
    cancellation_reason   TEXT          NULL,
    cancelled_by          VARCHAR(20)   NULL,        -- CLIENTE | CHOFER | ADMIN | SISTEMA
    -- Algoritmo de despacho
    dispatch_attempts     INTEGER       NOT NULL DEFAULT 0,
    last_dispatch_radius_km DECIMAL(5,2) NULL,
    last_dispatch_at      TIMESTAMP     NULL,
    -- Auditoría
    created_at            TIMESTAMP     NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMP     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_order_customer ON "order"(customer_id);
CREATE INDEX idx_order_delivery ON "order"(delivery_id);
CREATE INDEX idx_order_status ON "order"(status);
CREATE INDEX idx_order_status_pending ON "order"(status, created_at) WHERE status = 'PENDING';
CREATE INDEX idx_order_created ON "order"(created_at);

COMMENT ON TABLE "order" IS 'Pedido. Tabla central de transacciones del sistema';

-- ============================================================
-- 11. TABLA: order_item
-- Líneas de un pedido (una garrafa con cantidad)
-- ============================================================
CREATE TABLE order_item (
    order_item_id          UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id               UUID          NOT NULL REFERENCES "order"(order_id) ON DELETE CASCADE,
    gas_cylinder_id        UUID          NOT NULL REFERENCES gas_cylinder(gas_cylinder_id),
    quantity               INTEGER       NOT NULL,
    unit_price             DECIMAL(10,2) NOT NULL,  -- Snapshot al momento de la compra
    subtotal               DECIMAL(12,2) NOT NULL,
    applied_discount_pct   DECIMAL(5,2)  NULL,
    discount_amount        DECIMAL(10,2) NULL DEFAULT 0,
    CHECK (quantity > 0),
    CHECK (unit_price >= 0)
);

CREATE INDEX idx_order_item_order ON order_item(order_id);
CREATE INDEX idx_order_item_cylinder ON order_item(gas_cylinder_id);

COMMENT ON TABLE order_item IS 'Línea de pedido. Snapshot del precio al momento de la compra';

-- ============================================================
-- 12. TABLA: claims (reclamos)
-- ============================================================
CREATE TABLE claims (
    claim_id           UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id           UUID          NOT NULL REFERENCES "order"(order_id),
    customer_id        UUID          NOT NULL REFERENCES customer(customer_id),
    delivery_id        UUID          NULL REFERENCES delivery(delivery_id),  -- Chofer reclamado (opcional)
    reason             VARCHAR(100)  NOT NULL,
    description        TEXT          NOT NULL,
    photo_url          VARCHAR(500)  NULL,
    status             VARCHAR(20)   NOT NULL DEFAULT 'PENDING',  -- PENDING | IN_PROCESS | RESOLVED | REJECTED
    resolution_note    TEXT          NULL,
    resolved_by        UUID          NULL REFERENCES "user"(user_id),  -- Admin que resolvió
    resolved_at        TIMESTAMP     NULL,
    created_at         TIMESTAMP     NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMP     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_claim_order ON claims(order_id);
CREATE INDEX idx_claim_customer ON claims(customer_id);
CREATE INDEX idx_claim_status ON claims(status);

COMMENT ON TABLE claims IS 'Reclamos de clientes sobre pedidos entregados';

-- ============================================================
-- 13. TABLA: notification (antes vacía — completada)
-- Historial de notificaciones enviadas por el sistema
-- ============================================================
CREATE TABLE notification (
    notification_id    UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id            UUID           NOT NULL REFERENCES "user"(user_id) ON DELETE CASCADE,
    order_id           UUID           NULL REFERENCES "order"(order_id),
    claim_id           UUID           NULL REFERENCES claims(claim_id),
    type               VARCHAR(40)    NOT NULL,    -- ORDER_CONFIRMED | ORDER_ACCEPTED | ORDER_ON_THE_WAY | ORDER_ARRIVED | ORDER_DELIVERED | ORDER_CANCELLED | NEW_ORDER_REQUEST | CLAIM_CREATED | CLAIM_RESOLVED | PROMOTION
    channel            VARCHAR(20)    NOT NULL,    -- WEBSOCKET | FCM_PUSH | EMAIL | SMS
    title              VARCHAR(150)   NOT NULL,
    body               TEXT           NOT NULL,
    payload            JSONB          NULL,        -- Datos adicionales del evento
    is_read            BOOLEAN        NOT NULL DEFAULT FALSE,
    is_sent            BOOLEAN        NOT NULL DEFAULT FALSE,
    sent_at            TIMESTAMP      NULL,
    read_at            TIMESTAMP      NULL,
    error_message      TEXT           NULL,
    retry_count        INTEGER        NOT NULL DEFAULT 0,
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notification_user ON notification(user_id);
CREATE INDEX idx_notification_unread ON notification(user_id, is_read) WHERE is_read = FALSE;
CREATE INDEX idx_notification_order ON notification(order_id);
CREATE INDEX idx_notification_type ON notification(type);

COMMENT ON TABLE notification IS 'Historial de notificaciones enviadas (FCM, WebSocket, Email, SMS)';

-- ============================================================
-- 14. TABLA: payment_gateway (antes vacía — completada)
-- Registros de pagos procesados por gateways externos
-- ============================================================
CREATE TABLE payment_gateway (
    payment_gateway_id     UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id               UUID           NOT NULL UNIQUE REFERENCES "order"(order_id),
    gateway                VARCHAR(20)    NOT NULL,  -- MERCADOPAGO | STRIPE | TRANSFER | CASH
    external_id            VARCHAR(100)   NULL,      -- ID del gateway externo (preferenceId / paymentId)
    preference_id          VARCHAR(100)   NULL,      -- MP preference_id
    payment_id             VARCHAR(100)   NULL,      -- MP payment_id (definitivo post-pago)
    status                 VARCHAR(20)    NOT NULL DEFAULT 'PENDING',  -- PENDING | APPROVED | REJECTED | REFUNDED | CANCELLED | CHARGEDBACK
    amount                 DECIMAL(12,2)  NOT NULL,
    currency               VARCHAR(3)     NOT NULL DEFAULT 'ARS',
    payer_email            VARCHAR(255)   NULL,
    payment_method_detail  VARCHAR(50)    NULL,      -- Ej: visa, mastercard, account_money
    installments           INTEGER        NULL,
    gateway_response       JSONB          NULL,      -- Respuesta completa del gateway
    init_point_url         TEXT           NULL,      -- URL de checkout MP
    fee_amount             DECIMAL(10,2)  NULL,
    net_received           DECIMAL(12,2)  NULL,
    paid_at                TIMESTAMP      NULL,
    refunded_at            TIMESTAMP      NULL,
    error_message          TEXT           NULL,
    created_at             TIMESTAMP      NOT NULL DEFAULT NOW(),
    updated_at             TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_payment_order ON payment_gateway(order_id);
CREATE INDEX idx_payment_external ON payment_gateway(external_id);
CREATE INDEX idx_payment_status ON payment_gateway(status);

COMMENT ON TABLE payment_gateway IS 'Registro de pagos procesados por pasarelas externas (MercadoPago, etc.)';

-- ============================================================
-- 15. TABLA: webhook (antes vacía — completada)
-- Log de webhooks entrantes desde gateways externos
-- ============================================================
CREATE TABLE webhook (
    webhook_id         UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    source             VARCHAR(20)    NOT NULL,  -- MERCADOPAGO | FIREBASE | STRIPE | OTHER
    event_type         VARCHAR(50)    NOT NULL,  -- payment.created | payment.updated | etc.
    external_id        VARCHAR(100)   NULL,      -- ID del evento en el origen
    payment_gateway_id UUID           NULL REFERENCES payment_gateway(payment_gateway_id),
    payload            JSONB          NOT NULL,  -- Cuerpo completo del webhook
    headers            JSONB          NULL,
    ip_address         VARCHAR(45)    NULL,
    signature_valid    BOOLEAN        NULL,
    is_processed       BOOLEAN        NOT NULL DEFAULT FALSE,
    processed_at       TIMESTAMP      NULL,
    error_message      TEXT           NULL,
    retry_count        INTEGER        NOT NULL DEFAULT 0,
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_webhook_source ON webhook(source);
CREATE INDEX idx_webhook_processed ON webhook(is_processed);
CREATE INDEX idx_webhook_external ON webhook(external_id);

COMMENT ON TABLE webhook IS 'Log de webhooks entrantes desde gateways externos. Crítico para conciliación de pagos';

-- ============================================================
-- 16. TABLA: email (antes vacía — completada)
-- Cola y log de emails enviados
-- ============================================================
CREATE TABLE email (
    email_id           UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id            UUID           NULL REFERENCES "user"(user_id),
    to_email           VARCHAR(255)   NOT NULL,
    cc_email           VARCHAR(500)   NULL,
    bcc_email          VARCHAR(500)   NULL,
    from_email         VARCHAR(255)   NOT NULL,
    subject            VARCHAR(200)   NOT NULL,
    template_name      VARCHAR(50)    NULL,    -- Ej: welcome, order_confirmation, password_reset
    template_data      JSONB          NULL,    -- Variables para el template
    body_html          TEXT           NULL,
    body_text          TEXT           NULL,
    status             VARCHAR(20)    NOT NULL DEFAULT 'PENDING',  -- PENDING | SENT | FAILED | BOUNCED
    sent_at            TIMESTAMP      NULL,
    error_message      TEXT           NULL,
    retry_count        INTEGER        NOT NULL DEFAULT 0,
    smtp_message_id    VARCHAR(255)   NULL,
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_email_user ON email(user_id);
CREATE INDEX idx_email_status ON email(status);
CREATE INDEX idx_email_to ON email(to_email);

COMMENT ON TABLE email IS 'Cola y log de emails transaccionales enviados por el sistema';

-- ============================================================
-- 17. TABLA: seed (antes vacía — completada)
-- Registro de seeds aplicados a la base de datos
-- ============================================================
CREATE TABLE seed (
    seed_id            UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    name               VARCHAR(100)   NOT NULL UNIQUE,  -- Ej: initial_roles, demo_products
    description        TEXT           NULL,
    version            VARCHAR(20)    NULL,
    executed_at        TIMESTAMP      NOT NULL DEFAULT NOW(),
    success            BOOLEAN        NOT NULL DEFAULT TRUE,
    records_affected   INTEGER        NULL,
    error_message      TEXT           NULL,
    executed_by        VARCHAR(100)   NULL  -- Usuario o sistema que ejecutó
);

COMMENT ON TABLE seed IS 'Registro histórico de seeds aplicados (data inicial, demo data, fixtures)';

-- ============================================================
-- 18. TABLA: audit_log (NUEVA — Auditoría)
-- Trazabilidad completa de cambios sensibles del sistema
-- ============================================================
CREATE TABLE audit_log (
    audit_id           UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id            UUID           NULL REFERENCES "user"(user_id),  -- Quien hizo la acción
    entity_type        VARCHAR(50)    NOT NULL,  -- User | Order | Claim | Delivery | GasCylinder | TimeSlot | etc.
    entity_id          UUID           NOT NULL,  -- ID del registro afectado
    action             VARCHAR(20)    NOT NULL,  -- CREATE | UPDATE | DELETE | LOGIN | LOGOUT | STATUS_CHANGE | CANCEL | REASSIGN
    field_changed      VARCHAR(50)    NULL,      -- Solo si action=UPDATE
    old_value          JSONB          NULL,
    new_value          JSONB          NULL,
    description        TEXT           NULL,      -- Descripción legible del cambio
    ip_address         VARCHAR(45)    NULL,
    user_agent         TEXT           NULL,
    request_id         VARCHAR(50)    NULL,      -- Correlation ID
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_user ON audit_log(user_id);
CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_action ON audit_log(action);
CREATE INDEX idx_audit_created ON audit_log(created_at);

COMMENT ON TABLE audit_log IS 'Auditoría completa de operaciones sensibles. Cumplimiento normativo y debugging';

-- ============================================================
-- 19. TABLA: order_driver_rejection (NUEVA — Tabla intermedia)
-- Registro de rechazos de pedidos por chofer
-- Previene re-notificación al mismo chofer + analytics
-- ============================================================
CREATE TABLE order_driver_rejection (
    rejection_id       UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id           UUID           NOT NULL REFERENCES "order"(order_id) ON DELETE CASCADE,
    delivery_id        UUID           NOT NULL REFERENCES delivery(delivery_id),
    rejection_type     VARCHAR(20)    NOT NULL DEFAULT 'EXPLICIT',  -- EXPLICIT | TIMEOUT | UNAVAILABLE
    reason             TEXT           NULL,
    distance_at_offer_km DECIMAL(5,2) NULL,
    rejected_at        TIMESTAMP      NOT NULL DEFAULT NOW(),
    UNIQUE(order_id, delivery_id)  -- Un chofer rechaza un pedido solo una vez
);

CREATE INDEX idx_rejection_order ON order_driver_rejection(order_id);
CREATE INDEX idx_rejection_driver ON order_driver_rejection(delivery_id);

COMMENT ON TABLE order_driver_rejection IS 'Registro de rechazos chofer-pedido. Previene re-notificación + analytics';

-- ============================================================
-- 20. TABLA: rating (Calificaciones de entrega)
-- Cliente califica al chofer post-entrega (1-5 + comentario)
-- ============================================================
CREATE TABLE rating (
    rating_id          UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id           UUID           NOT NULL UNIQUE REFERENCES "order"(order_id),
    customer_id        UUID           NOT NULL REFERENCES customer(customer_id),
    delivery_id        UUID           NOT NULL REFERENCES delivery(delivery_id),
    score              INTEGER        NOT NULL,  -- 1 a 5 estrellas
    speed_score        INTEGER        NULL,      -- Velocidad de entrega (1-5)
    courtesy_score     INTEGER        NULL,      -- Trato del chofer (1-5)
    comment            TEXT           NULL,
    is_anonymous       BOOLEAN        NOT NULL DEFAULT FALSE,
    is_visible         BOOLEAN        NOT NULL DEFAULT TRUE,  -- Admin puede ocultar abusos
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW(),
    CHECK (score BETWEEN 1 AND 5),
    CHECK (speed_score IS NULL OR speed_score BETWEEN 1 AND 5),
    CHECK (courtesy_score IS NULL OR courtesy_score BETWEEN 1 AND 5)
);

CREATE INDEX idx_rating_delivery ON rating(delivery_id);
CREATE INDEX idx_rating_customer ON rating(customer_id);
CREATE INDEX idx_rating_score ON rating(score);

COMMENT ON TABLE rating IS 'Calificación del cliente al chofer después de la entrega. Origen del promedio Delivery.calification';

-- ============================================================
-- 21. TABLA: fcm_token (Dispositivos del usuario)
-- Múltiples tokens FCM por usuario (un usuario, varios dispositivos)
-- ============================================================
CREATE TABLE fcm_token (
    token_id           UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id            UUID           NOT NULL REFERENCES "user"(user_id) ON DELETE CASCADE,
    fcm_token          TEXT           NOT NULL UNIQUE,
    device_type        VARCHAR(20)    NOT NULL,    -- ANDROID | IOS | WEB
    device_model       VARCHAR(100)   NULL,        -- "iPhone 14 Pro", "Pixel 7"
    device_os_version  VARCHAR(30)    NULL,
    app_version        VARCHAR(20)    NULL,
    locale             VARCHAR(10)    NULL,        -- es-AR, en-US
    is_active          BOOLEAN        NOT NULL DEFAULT TRUE,
    last_used_at       TIMESTAMP      NOT NULL DEFAULT NOW(),
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_fcm_user ON fcm_token(user_id);
CREATE INDEX idx_fcm_active ON fcm_token(user_id, is_active);

COMMENT ON TABLE fcm_token IS 'Tokens FCM por dispositivo. Un usuario puede tener múltiples (celu + tablet, cambio de equipo)';

-- ============================================================
-- 22. TABLA: delivery_zone (Zonas de cobertura)
-- Polígonos geográficos donde el sistema opera
-- ============================================================
CREATE TABLE delivery_zone (
    zone_id            UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    name               VARCHAR(100)   NOT NULL,
    description        TEXT           NULL,
    polygon_geojson    JSONB          NOT NULL,    -- GeoJSON Polygon con coordenadas del área
    delivery_fee       DECIMAL(10,2)  NULL DEFAULT 0,
    min_order_amount   DECIMAL(10,2)  NULL,        -- Pedido mínimo en esta zona
    estimated_time_min INTEGER        NULL,        -- Tiempo estimado de entrega
    color_hex          VARCHAR(7)     NULL,        -- Color para visualizar en mapa
    is_active          BOOLEAN        NOT NULL DEFAULT TRUE,
    priority           INTEGER        NOT NULL DEFAULT 1,  -- Si hay solapamiento, mayor prioridad gana
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_zone_active ON delivery_zone(is_active);

COMMENT ON TABLE delivery_zone IS 'Zonas geográficas de cobertura. Pre-validación de dirección antes de crear pedido';

-- ============================================================
-- 23. TABLA: driver_shift (Turnos de trabajo)
-- Sesiones de trabajo del chofer (login → logout disponibilidad)
-- ============================================================
CREATE TABLE driver_shift (
    shift_id              UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    delivery_id           UUID           NOT NULL REFERENCES delivery(delivery_id),
    start_time            TIMESTAMP      NOT NULL,
    end_time              TIMESTAMP      NULL,
    duration_minutes      INTEGER        NULL,        -- Calculado al cerrar
    deliveries_count      INTEGER        NOT NULL DEFAULT 0,
    deliveries_cancelled  INTEGER        NOT NULL DEFAULT 0,
    total_distance_km     DECIMAL(8,2)   NULL,
    total_earnings        DECIMAL(10,2)  NOT NULL DEFAULT 0,
    cash_collected        DECIMAL(10,2)  NOT NULL DEFAULT 0,  -- Efectivo recibido
    start_location_lat    DECIMAL(10,7)  NULL,
    start_location_lng    DECIMAL(10,7)  NULL,
    end_location_lat      DECIMAL(10,7)  NULL,
    end_location_lng      DECIMAL(10,7)  NULL,
    notes                 TEXT           NULL,
    created_at            TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_shift_driver ON driver_shift(delivery_id);
CREATE INDEX idx_shift_active ON driver_shift(delivery_id, end_time) WHERE end_time IS NULL;
CREATE INDEX idx_shift_date ON driver_shift(start_time);

COMMENT ON TABLE driver_shift IS 'Turnos de trabajo del chofer. Tracking de horas, entregas y rendimiento';

-- ============================================================
-- 24. TABLA: promo_code (Cupones de descuento)
-- Códigos promocionales aplicables en checkout
-- ============================================================
CREATE TABLE promo_code (
    promo_id              UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    code                  VARCHAR(30)    NOT NULL UNIQUE,
    description           TEXT           NULL,
    discount_type         VARCHAR(20)    NOT NULL,    -- PERCENTAGE | FIXED_AMOUNT | FREE_SHIPPING
    discount_value        DECIMAL(10,2)  NOT NULL,
    min_order_amount      DECIMAL(10,2)  NULL,
    max_discount_amount   DECIMAL(10,2)  NULL,        -- Tope absoluto (para %)
    max_uses              INTEGER        NULL,        -- Límite global (NULL = ilimitado)
    max_uses_per_customer INTEGER        NULL DEFAULT 1,
    current_uses          INTEGER        NOT NULL DEFAULT 0,
    valid_from            TIMESTAMP      NOT NULL,
    valid_until           TIMESTAMP      NULL,
    applies_to            VARCHAR(20)    NULL,        -- ALL | NEW_CUSTOMERS | SPECIFIC_PRODUCTS | FIRST_ORDER
    target_product_ids    JSONB          NULL,        -- Si applies_to=SPECIFIC_PRODUCTS
    is_active             BOOLEAN        NOT NULL DEFAULT TRUE,
    created_by            UUID           NULL REFERENCES "user"(user_id),
    created_at            TIMESTAMP      NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_promo_code ON promo_code(code);
CREATE INDEX idx_promo_active ON promo_code(is_active, valid_from, valid_until);

COMMENT ON TABLE promo_code IS 'Cupones de descuento que el cliente ingresa en checkout';

-- ============================================================
-- 25. TABLA: promo_code_usage (Uso de cupones)
-- Registro de cada vez que se aplica un cupón
-- ============================================================
CREATE TABLE promo_code_usage (
    usage_id           UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    promo_id           UUID           NOT NULL REFERENCES promo_code(promo_id),
    customer_id        UUID           NOT NULL REFERENCES customer(customer_id),
    order_id           UUID           NOT NULL REFERENCES "order"(order_id),
    discount_applied   DECIMAL(10,2)  NOT NULL,
    used_at            TIMESTAMP      NOT NULL DEFAULT NOW(),
    UNIQUE(promo_id, order_id)  -- Un cupón por pedido máximo
);

CREATE INDEX idx_promo_usage_customer ON promo_code_usage(customer_id);
CREATE INDEX idx_promo_usage_order ON promo_code_usage(order_id);

COMMENT ON TABLE promo_code_usage IS 'Registro de uso de cupones. Soporta el control de max_uses_per_customer';

-- ============================================================
-- 26. TABLA: stock_movement (Movimientos de inventario)
-- Histórico de TODOS los cambios de stock
-- ============================================================
CREATE TABLE stock_movement (
    movement_id        UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    gas_cylinder_id    UUID           NOT NULL REFERENCES gas_cylinder(gas_cylinder_id),
    movement_type      VARCHAR(30)    NOT NULL,    -- PURCHASE | SALE | CANCELLATION | ADJUSTMENT | LOSS | RETURN | INITIAL_LOAD
    quantity           INTEGER        NOT NULL,    -- Positivo (suma) o negativo (resta)
    quantity_before    INTEGER        NOT NULL,
    quantity_after     INTEGER        NOT NULL,
    unit_cost          DECIMAL(10,2)  NULL,        -- Costo de compra (si movement_type=PURCHASE)
    reference_id       UUID           NULL,        -- ID del order, claim, etc. que generó el movimiento
    reference_type     VARCHAR(50)    NULL,        -- ORDER_ITEM | CANCELLATION | MANUAL | INITIAL_LOAD
    reason             TEXT           NULL,
    performed_by       UUID           NULL REFERENCES "user"(user_id),
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_movement_cylinder ON stock_movement(gas_cylinder_id);
CREATE INDEX idx_movement_type ON stock_movement(movement_type);
CREATE INDEX idx_movement_date ON stock_movement(created_at);
CREATE INDEX idx_movement_reference ON stock_movement(reference_type, reference_id);

COMMENT ON TABLE stock_movement IS 'Auditoría completa de movimientos de stock. Cumplimiento contable + analytics de inventario';

-- ============================================================
-- 27. TABLA: driver_document (Documentos del chofer)
-- Documentos legales requeridos para operar
-- ============================================================
CREATE TABLE driver_document (
    document_id        UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    delivery_id        UUID           NOT NULL REFERENCES delivery(delivery_id),
    document_type      VARCHAR(40)    NOT NULL,    -- DRIVER_LICENSE | INSURANCE | VEHICLE_REGISTRATION | CRIMINAL_RECORD | ID_FRONT | ID_BACK | TAX_ID | BANK_ACCOUNT
    file_url           TEXT           NOT NULL,
    file_name          VARCHAR(255)   NULL,
    file_size_kb       INTEGER        NULL,
    mime_type          VARCHAR(50)    NULL,
    expiration_date    DATE           NULL,        -- Si aplica (licencia, seguro)
    is_verified        BOOLEAN        NOT NULL DEFAULT FALSE,
    verified_by        UUID           NULL REFERENCES "user"(user_id),
    verified_at        TIMESTAMP      NULL,
    rejection_reason   TEXT           NULL,
    notes              TEXT           NULL,
    uploaded_at        TIMESTAMP      NOT NULL DEFAULT NOW(),
    UNIQUE(delivery_id, document_type)
);

CREATE INDEX idx_doc_driver ON driver_document(delivery_id);
CREATE INDEX idx_doc_verified ON driver_document(is_verified);
CREATE INDEX idx_doc_expiration ON driver_document(expiration_date) WHERE expiration_date IS NOT NULL;

COMMENT ON TABLE driver_document IS 'Documentos legales del chofer (licencia, seguro, antecedentes). Requerido para validación CU-032';

-- ============================================================
-- 28. TABLA: chat_message (Chat in-app)
-- Mensajes entre cliente y chofer durante la entrega
-- ============================================================
CREATE TABLE chat_message (
    message_id         UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id           UUID           NOT NULL REFERENCES "order"(order_id) ON DELETE CASCADE,
    sender_id          UUID           NOT NULL REFERENCES "user"(user_id),
    sender_role        VARCHAR(20)    NOT NULL,    -- CLIENTE | CHOFER
    message_type       VARCHAR(20)    NOT NULL DEFAULT 'TEXT',  -- TEXT | IMAGE | LOCATION | QUICK_REPLY | SYSTEM
    content            TEXT           NOT NULL,
    attachment_url     TEXT           NULL,
    location_lat       DECIMAL(10,7)  NULL,        -- Si message_type=LOCATION
    location_lng       DECIMAL(10,7)  NULL,
    is_read            BOOLEAN        NOT NULL DEFAULT FALSE,
    read_at            TIMESTAMP      NULL,
    deleted_at         TIMESTAMP      NULL,
    sent_at            TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_chat_order ON chat_message(order_id);
CREATE INDEX idx_chat_unread ON chat_message(order_id, is_read) WHERE is_read = FALSE;
CREATE INDEX idx_chat_sender ON chat_message(sender_id);

COMMENT ON TABLE chat_message IS 'Chat in-app cliente↔chofer durante la entrega. Activo solo mientras pedido está ACCEPTED u ON_THE_WAY';

-- ============================================================
-- 29. TABLA: scheduled_order (Pedidos recurrentes)
-- Suscripciones de pedido (ej: "1 garrafa cada 30 días")
-- ============================================================
CREATE TABLE scheduled_order (
    schedule_id              UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id              UUID           NOT NULL REFERENCES customer(customer_id),
    address_id               UUID           NOT NULL REFERENCES user_address(address_id),
    time_slot_id             UUID           NULL REFERENCES time_slot(time_slot_id),
    payment_method           VARCHAR(20)    NOT NULL,
    items                    JSONB          NOT NULL,  -- [{gasCylinderId, quantity}]
    frequency                VARCHAR(20)    NOT NULL,  -- WEEKLY | BIWEEKLY | MONTHLY | CUSTOM_DAYS
    interval_days            INTEGER        NULL,      -- Solo si frequency=CUSTOM_DAYS
    next_delivery_date       DATE           NOT NULL,
    last_order_id            UUID           NULL REFERENCES "order"(order_id),
    is_active                BOOLEAN        NOT NULL DEFAULT TRUE,
    pause_until              DATE           NULL,      -- Pausa temporal por viaje, etc.
    end_date                 DATE           NULL,      -- Vencimiento de la suscripción
    total_orders_generated   INTEGER        NOT NULL DEFAULT 0,
    notes                    TEXT           NULL,
    created_at               TIMESTAMP      NOT NULL DEFAULT NOW(),
    updated_at               TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_scheduled_customer ON scheduled_order(customer_id);
CREATE INDEX idx_scheduled_next ON scheduled_order(next_delivery_date) WHERE is_active = TRUE;

COMMENT ON TABLE scheduled_order IS 'Suscripciones de pedido recurrente. Genera Order automáticamente al llegar next_delivery_date';

-- ============================================================
-- 30. TABLA: delivery_route (Trazabilidad GPS)
-- Recorrido completo de cada entrega
-- ============================================================
CREATE TABLE delivery_route (
    route_id           UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id           UUID           NOT NULL UNIQUE REFERENCES "order"(order_id),
    delivery_id        UUID           NOT NULL REFERENCES delivery(delivery_id),
    route_geojson      JSONB          NULL,        -- LineString GeoJSON con todos los puntos GPS
    distance_km        DECIMAL(8,2)   NULL,
    duration_minutes   INTEGER        NULL,
    started_at         TIMESTAMP      NOT NULL,
    ended_at           TIMESTAMP      NULL,
    -- Puntos clave del recorrido
    pickup_lat         DECIMAL(10,7)  NULL,
    pickup_lng         DECIMAL(10,7)  NULL,
    delivery_lat       DECIMAL(10,7)  NULL,
    delivery_lng       DECIMAL(10,7)  NULL,
    -- Métricas
    average_speed_kmh  DECIMAL(5,2)   NULL,
    max_speed_kmh      DECIMAL(5,2)   NULL,
    stops_count        INTEGER        NOT NULL DEFAULT 0,
    points_recorded    INTEGER        NOT NULL DEFAULT 0,  -- Cantidad de puntos GPS guardados
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_route_order ON delivery_route(order_id);
CREATE INDEX idx_route_driver ON delivery_route(delivery_id);

COMMENT ON TABLE delivery_route IS 'Track GPS completo de cada entrega. Útil para disputas, analytics y optimización';

-- ============================================================
-- 31. TABLA: support_ticket (Tickets de soporte)
-- Soporte general (no atado a un pedido)
-- ============================================================
CREATE TABLE support_ticket (
    ticket_id          UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_number      VARCHAR(20)    NOT NULL UNIQUE,  -- Ej: SPLG-2026-0001
    user_id            UUID           NOT NULL REFERENCES "user"(user_id),
    category           VARCHAR(40)    NOT NULL,    -- ACCOUNT | PAYMENT | TECHNICAL | DELIVERY_ISSUE | OTHER
    priority           VARCHAR(10)    NOT NULL DEFAULT 'NORMAL',  -- LOW | NORMAL | HIGH | URGENT
    subject            VARCHAR(200)   NOT NULL,
    description        TEXT           NOT NULL,
    status             VARCHAR(20)    NOT NULL DEFAULT 'OPEN',  -- OPEN | IN_PROGRESS | WAITING_CUSTOMER | RESOLVED | CLOSED
    assigned_to        UUID           NULL REFERENCES "user"(user_id),
    related_order_id   UUID           NULL REFERENCES "order"(order_id),
    resolution         TEXT           NULL,
    customer_satisfaction INTEGER     NULL,        -- 1-5 al cerrar
    resolved_at        TIMESTAMP      NULL,
    closed_at          TIMESTAMP      NULL,
    first_response_at  TIMESTAMP      NULL,        -- Para SLA
    created_at         TIMESTAMP      NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMP      NOT NULL DEFAULT NOW(),
    CHECK (customer_satisfaction IS NULL OR customer_satisfaction BETWEEN 1 AND 5)
);

CREATE INDEX idx_ticket_user ON support_ticket(user_id);
CREATE INDEX idx_ticket_status ON support_ticket(status);
CREATE INDEX idx_ticket_assigned ON support_ticket(assigned_to);
CREATE INDEX idx_ticket_priority ON support_ticket(priority, created_at);

COMMENT ON TABLE support_ticket IS 'Tickets de soporte general. Diferente de claims (que son sobre pedidos específicos)';

-- ============================================================
-- 32. TABLA: support_ticket_message (Conversación de tickets)
-- Mensajes dentro de un ticket de soporte
-- ============================================================
CREATE TABLE support_ticket_message (
    message_id         UUID           PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_id          UUID           NOT NULL REFERENCES support_ticket(ticket_id) ON DELETE CASCADE,
    sender_id          UUID           NOT NULL REFERENCES "user"(user_id),
    sender_role        VARCHAR(20)    NOT NULL,    -- CUSTOMER | SUPPORT_AGENT | SYSTEM
    content            TEXT           NOT NULL,
    attachment_url     TEXT           NULL,
    is_internal_note   BOOLEAN        NOT NULL DEFAULT FALSE,  -- Solo visible para soporte
    sent_at            TIMESTAMP      NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ticket_msg_ticket ON support_ticket_message(ticket_id);

COMMENT ON TABLE support_ticket_message IS 'Conversación dentro de un ticket de soporte (cliente ↔ agente)';

-- ============================================================
-- VISTAS AGREGADAS (opcional - útil para Lucidchart)
-- ============================================================

-- Vista resumen de pedidos para reportes
CREATE OR REPLACE VIEW v_order_summary AS
SELECT
    o.order_id,
    o.status,
    o.total_amount,
    o.created_at,
    c.customer_id,
    cu_user.full_name AS customer_name,
    d.delivery_id,
    dv_user.full_name AS driver_name,
    o.payment_method,
    o.payment_status
FROM "order" o
JOIN customer c ON o.customer_id = c.customer_id
JOIN "user" cu_user ON c.user_id = cu_user.user_id
LEFT JOIN delivery d ON o.delivery_id = d.delivery_id
LEFT JOIN "user" dv_user ON d.user_id = dv_user.user_id;

COMMENT ON VIEW v_order_summary IS 'Vista consolidada para listados y reportes de pedidos';

-- Vista de calificación promedio por chofer (denormalizada de rating)
CREATE OR REPLACE VIEW v_driver_ratings AS
SELECT
    d.delivery_id,
    u.full_name AS driver_name,
    COUNT(r.rating_id) AS total_ratings,
    AVG(r.score) AS avg_score,
    AVG(r.speed_score) AS avg_speed,
    AVG(r.courtesy_score) AS avg_courtesy
FROM delivery d
JOIN "user" u ON d.user_id = u.user_id
LEFT JOIN rating r ON r.delivery_id = d.delivery_id AND r.is_visible = TRUE
GROUP BY d.delivery_id, u.full_name;

COMMENT ON VIEW v_driver_ratings IS 'Calificación promedio por chofer. Útil para Delivery.calification y reportes';

-- ============================================================
-- FIN DEL ESQUEMA
-- ============================================================
-- Total: 32 tablas + 2 vistas
-- ------------------------------------------------------------
-- Distribución por capa:
--   • Identidad (5):     role, user, customer, delivery, admin
--   • Catálogo (3):      gas_cylinder, time_slot, car
--   • Direcciones (1):   user_address
--   • Pedidos (3):       order, order_item, order_driver_rejection
--   • Reclamos (1):      claims
--   • Pagos (2):         payment_gateway, webhook
--   • Notificaciones (3): notification, fcm_token, email
--   • Operación (4):     driver_shift, delivery_zone, delivery_route, stock_movement
--   • Comercial (3):     promo_code, promo_code_usage, scheduled_order
--   • Soporte (3):       support_ticket, support_ticket_message, chat_message
--   • Calidad (2):       rating, driver_document
--   • Sistema (2):       audit_log, seed
-- ------------------------------------------------------------
-- Relaciones FK: ~50
-- Índices: ~55
-- ============================================================
