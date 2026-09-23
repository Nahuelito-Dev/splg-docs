# Firmas Reales del Backend (splg-app-backend)

Documento de extracción técnica de firmas reales, dependencias de constructor, handlers de eventos y relaciones de entidades TypeORM para el diagrama de clases UML de diseño.

Fecha de extracción: 2026-09-09
Fuente de lectura: `splg-app-backend/src`

---

## 1. Clases de Servicio, Gateways y Casos de Uso

### 1. OrderService
- **Ubicación:** `src/order/order.service.ts:26`
- **Dependencias / Atributos inyectados por constructor:**
  - `private readonly orderRepository: Repository<Order>` (`@InjectRepository(Order)`)
  - `private readonly deliveryRepository: Repository<Delivery>` (`@InjectRepository(Delivery)`)
  - `private readonly dispatch: RealtimeDispatchPort`
  - `private readonly orders: OrderRepositoryPort`
  - `private readonly createOrderUseCase: CreateOrderUseCase`
  - `private readonly updateOrderStatusUseCase: UpdateOrderStatusUseCase`
  - `private readonly cancelOrderUseCase: CancelOrderUseCase`
  - `private readonly confirmDeliveryUseCase: ConfirmDeliveryUseCase`
  - `private readonly dispatchOrchestrator: DispatchOrchestratorService`
- **Métodos Públicos:**
  - `rejectOffer(orderId: string, driverId: string): (sin anotar)`
  - `create(createOrderDto: CreateOrderDto, distributorId?: string | null): (sin anotar)`
  - `findAll(paginationDto: PaginationDto, distributorId?: string | null): (sin anotar)`
  - `findOne(id: string): (sin anotar)`
  - `getOne(id: string, distributorId?: string | null, customerUserId?: string | null): Promise<OrderResponseDto>`
  - `findAvailableOrders(paginationDto: PaginationDto, distributorId?: string | null): (sin anotar)`
  - `findByCustomer(customerId: string, paginationDto: PaginationDto, distributorId?: string | null): (sin anotar)`
  - `findByDelivery(deliveryId: string, paginationDto: PaginationDto, distributorId?: string | null): (sin anotar)`
  - `updateStatus(id: string, status: OrderStatus, deliveryId?: string): (sin anotar)`
  - `getDeliveryCode(orderId: string, userId: string, role: RoleType): (sin anotar)`
  - `confirmDelivery(orderId: string, code: string, userId: string, role: RoleType): (sin anotar)`
  - `assignDelivery(orderId: string, deliveryId: string): (sin anotar)`
  - `updateLocation(id: string, lat: string, lng: string): (sin anotar)`
  - `getOrderStats(distributorId?: string | null): (sin anotar)`
  - `cancelOrder(orderId: string, userId: string, role: 'customer' | 'driver' | 'admin' | 'superadmin', reason?: string): (sin anotar)`
  - `notifyDriverArrived(orderId: string): (sin anotar)`
  - `getSalesChartData(distributorId?: string | null): (sin anotar)`

---

### 2. DispatchService
- **Ubicación:** `src/order/dispatch.service.ts:19`
- **Dependencias / Atributos inyectados por constructor:**
  - `private readonly orderService: OrderService`
  - `private readonly redisService: RedisService`
  - `private readonly orchestrator: DispatchOrchestratorService`
- **Métodos Públicos:**
  - `tick(): (sin anotar)` [Decorador: `@Cron('*/15 * * * * *')`]

---

### 3. DispatchOrchestratorService
- **Ubicación:** `src/order/application/dispatch-orchestrator.service.ts:23`
- **Dependencias / Atributos inyectados por constructor:**
  - `private readonly dispatch: RealtimeDispatchPort`
  - `private readonly orders: OrderRepositoryPort`
  - `private readonly offers: DispatchOfferRepositoryPort`
  - `private readonly deliveryRepository: Repository<Delivery>` (`@InjectRepository(Delivery)`)
  - `private readonly notifications: NotificationsService`
- **Métodos Públicos:**
  - `offerToNextDriver(order: Order): Promise<string | null>`
  - `handleExpiredOffers(): Promise<void>`
  - `ensureOffered(order: Order): Promise<void>`
  - `onDriverAccepted(orderId: string, driverId: string): Promise<void>`
  - `onDriverRejected(order: Order, driverId: string): Promise<void>`

---

### 4. RedisService (Métodos de Geolocalización y Ubicación de Choferes)
- **Ubicación:** `src/redis/redis.service.ts:13`
- **Dependencias / Atributos inyectados por constructor:**
  - `private readonly configService: ConfigService`
- **Métodos Públicos (Filtrados por Geolocalización / Ubicación Choferes):**
  - `setDriverActiveOrder(driverUserId: string, data: { orderId: string; customerId: string }, ttlSec = 3 * 60 * 60): Promise<void>`
  - `getDriverActiveOrder(driverUserId: string): Promise<{ orderId: string; customerId: string } | null>`
  - `clearDriverActiveOrder(driverUserId: string): Promise<void>`
  - `updateDriverLocation(driverId: string, lat: number, lng: number): (sin anotar)`
  - `getNearbyDrivers(lat: number, lng: number, radiusKm: number = 5): Promise<string[]>`
  - `removeDriver(driverId: string): (sin anotar)`

---

### 5. DriversGateway
- **Ubicación:** `src/gateways/drivers.gateway.ts:23`
- **Decorador de clase:** `@WebSocketGateway({ cors: { origin: '*' }, namespace: 'drivers' })`
- **Interfaces implementadas:** `OnGatewayConnection, OnGatewayDisconnect`
- **Propiedades de clase:**
  - `@WebSocketServer() server: Server`
  - `private readonly logger = new Logger('DriversGateway')`
- **Dependencias / Atributos inyectados por constructor:**
  - `private readonly redisService: RedisService`
  - `private readonly authService: AuthService`
  - `private readonly customersGateway: CustomersGateway`
  - `private readonly adminGateway: AdminGateway`
- **Métodos Públicos y Handlers @SubscribeMessage:**
  - `handleConnection(client: Socket): (sin anotar)`
    - *Comportamiento/Emisión:* Autenticación por token de handshake/authorization; desconecta con `client.disconnect()` si es inválido.
  - `handleDisconnect(client: Socket): (sin anotar)`
    - *Comportamiento/Emisión:* Remueve al chofer del radar GEO llamando a `redisService.removeDriver(id)`.
  - `@SubscribeMessage('driver:join')`
    `handleDriverJoin(@MessageBody() data: { driverId: string }, @ConnectedSocket() client: Socket): (sin anotar)`
    - *Unión a sala:* `client.join('driver_${data.driverId}')`
    - *Eventos emitidos:* `client.emit('server:ack', { message: 'Conectado al despacho' })`
  - `@SubscribeMessage('driver:update-location')`
    `handleDriverLocation(@MessageBody() data: { userId: string; lat: number; lng: number }, @ConnectedSocket() client: Socket): (sin anotar)`
    - *Actualiza ubicación:* Llama a `redisService.updateDriverLocation(data.userId, data.lat, data.lng)`.
    - *Eventos emitidos (si tiene orden activa en Redis):*
      - `this.customersGateway.notifyCustomer(active.customerId, 'order:driver-location', payload)` (emite `'order:driver-location'` a sala del cliente)
      - `this.adminGateway.notifyAdmins('order:driver-location', payload)` (emite `'order:driver-location'` al namespace admin)
  - `notifyNewOrder(driverId: string, orderPayload: any): (sin anotar)`
    - *Eventos emitidos:* `this.server.to('driver_${driverId}').emit('server:new-order-request', orderPayload)`
  - `notifyOrderCancelled(driverId: string, payload: any): (sin anotar)`
    - *Eventos emitidos:* `this.server.to('driver_${driverId}').emit('order:cancelled', payload)`

---

### 6. CustomersGateway
- **Ubicación:** `src/gateways/customers.gateway.ts:20`
- **Decorador de clase:** `@WebSocketGateway({ cors: { origin: '*' }, namespace: 'customers' })`
- **Interfaces implementadas:** `OnGatewayConnection, OnGatewayDisconnect`
- **Propiedades de clase:**
  - `@WebSocketServer() server: Server`
  - `private readonly logger = new Logger('CustomersGateway')`
- **Dependencias / Atributos inyectados por constructor:**
  - `private readonly authService: AuthService`
- **Métodos Públicos y Handlers @SubscribeMessage:**
  - `handleConnection(client: Socket): (sin anotar)`
    - *Comportamiento/Emisión:* Autentica token handshake y asigna `(client as any).user`; si no hay token llama `client.disconnect()`.
  - `handleDisconnect(client: Socket): (sin anotar)`
    - *Comportamiento/Emisión:* Hook de desconexión.
  - `@SubscribeMessage('customer:join')`
    `handleCustomerJoin(@MessageBody() data: { customerId: string }, @ConnectedSocket() client: Socket): (sin anotar)`
    - *Unión a sala:* `client.join('customer_${data.customerId}')`
    - *Eventos emitidos:* `client.emit('server:ack', { message: 'Conectado a actualizaciones de pedidos' })`
  - `notifyCustomer(customerId: string, event: string, payload: any): (sin anotar)`
    - *Eventos emitidos:* `this.server.to('customer_${customerId}').emit(event, payload)`

---

### 7. CreateOrderUseCase
- **Ubicación:** `src/order/application/create-order.use-case.ts:60`
- **Dependencias / Atributos inyectados por constructor:**
  - `private readonly dataSource: DataSource`
  - `private readonly userRepository: Repository<User>` (`@InjectRepository(User)`)
  - `private readonly userAddressRepository: Repository<UserAddress>` (`@InjectRepository(UserAddress)`)
  - `private readonly orderItemRepository: Repository<OrderItem>` (`@InjectRepository(OrderItem)`)
  - `private readonly orderRepository: Repository<Order>` (`@InjectRepository(Order)`)
  - `private readonly pricing: OrderPricingService`
  - `private readonly stock: StockReservationService`
  - `private readonly dispatchOrchestrator: DispatchOrchestratorService`
  - `private readonly notificationService: NotificationPort`
  - `private readonly orders: OrderRepositoryPort`
  - `private readonly realtime: RealtimeDispatchPort`
  - `private readonly paymentsService: PaymentsService`
  - `private readonly distributorService: DistributorService`
  - `private readonly timeSlotService: TimeSlotService`
  - `private readonly coverageZoneService: CoverageZoneService`
- **Métodos Públicos:**
  - `execute(createOrderDto: CreateOrderDto, distributorId?: string | null): Promise<CreateOrderResult>`

---

### 8. UpdateOrderStatusUseCase
- **Ubicación:** `src/order/application/update-order-status.use-case.ts:45`
- **Dependencias / Atributos inyectados por constructor:**
  - `private readonly userRepository: Repository<User>` (`@InjectRepository(User)`)
  - `private readonly deliveryRepository: Repository<Delivery>` (`@InjectRepository(Delivery)`)
  - `private readonly dispatch: RealtimeDispatchPort`
  - `private readonly notificationService: NotificationPort`
  - `private readonly orders: OrderRepositoryPort`
  - `private readonly dispatchOrchestrator: DispatchOrchestratorService`
  - `private readonly cylinderLifecycle: CylinderLifecyclePort`
- **Métodos Públicos:**
  - `execute(id: string, status: OrderStatus, deliveryId?: string): Promise<Order>`

---

### 9. ConfirmDeliveryUseCase
- **Ubicación:** `src/order/application/confirm-delivery.use-case.ts:29`
- **Dependencias / Atributos inyectados por constructor:**
  - `private readonly orders: OrderRepositoryPort`
  - `private readonly updateOrderStatusUseCase: UpdateOrderStatusUseCase`
- **Métodos Públicos:**
  - `execute(orderId: string, code: string, userId: string, role: RoleType): Promise<Order>`

---

### 10. CancelOrderUseCase
- **Ubicación:** `src/order/application/cancel-order.use-case.ts:30`
- **Estado:** EXISTE
- **Dependencias / Atributos inyectados por constructor:**
  - `private readonly dataSource: DataSource`
  - `private readonly stock: StockReservationService`
  - `private readonly dispatch: RealtimeDispatchPort`
  - `private readonly orders: OrderRepositoryPort`
- **Métodos Públicos:**
  - `execute(orderId: string, userId: string, role: CancelActor, reason?: string): Promise<Order>`

---

## 2. Entidades TypeORM

### 1. Order
- **Ubicación:** `src/order/entities/order.entity.ts:58`
- **Tabla:** `@Entity('order')`
- **Propiedades:**
  - `order_id: string` — PK UUID (`@PrimaryGeneratedColumn('uuid', { name: 'order_id' })`)
  - `distributor?: Distributor` — Relación ManyToOne (opcional en TS, nullable: false en BD)
  - `distributor_id?: string` — UUID (opcional en TS, `@Column({ type: 'uuid', nullable: false })`)
  - `customer: User` — Relación ManyToOne (no nullable)
  - `customer_id: string` — UUID (`@Column({ type: 'uuid' })`)
  - `delivery: Delivery` — Relación ManyToOne (nullable: true)
  - `timeSlot: TimeSlot` — Relación ManyToOne (nullable: true)
  - `time_slot_id: string` — UUID (`@Column({ nullable: true })`)
  - `scheduled_date?: string | null` — Date (`@Column({ type: 'date', nullable: true })`)
  - `deposit_amount: number` — Decimal (`@Column({ type: 'decimal', precision: 10, scale: 2, default: 0 })`)
  - `deposit_paid: boolean` — Boolean (`@Column({ type: 'boolean', default: false })`)
  - `delivery_id: string | null` — UUID (`@Column({ nullable: true })`)
  - `address: UserAddress` — Relación ManyToOne (no nullable)
  - `address_id: string` — UUID (`@Column({ type: 'uuid' })`)
  - `status: OrderStatus` — Enum OrderStatus (`@Column({ type: 'enum', enum: OrderStatus, default: OrderStatus.PENDING })`)
  - `paymentMethod: PaymentMethod` — Enum PaymentMethod (`@Column({ type: 'enum', enum: PaymentMethod })`)
  - `paymentType: PaymentType` — Enum PaymentType (`@Column({ type: 'enum', enum: PaymentType, default: PaymentType.CASH })`)
  - `paymentStatus: PaymentStatus` — Enum PaymentStatus (`@Column({ type: 'enum', enum: PaymentStatus, default: PaymentStatus.PENDING })`)
  - `totalAmount: number` — Decimal (`@Column({ type: 'decimal', precision: 10, scale: 2 })`)
  - `notes: string` — Text (`@Column({ type: 'text', nullable: true })`)
  - `deliveryInstructions: string` — Text (`@Column({ type: 'text', nullable: true })`)
  - `deliveryLatitude: string` — Varchar(50) (`@Column({ type: 'varchar', length: 50, nullable: true })`)
  - `deliveryLongitude: string` — Varchar(50) (`@Column({ type: 'varchar', length: 50, nullable: true })`)
  - `acceptedAt: Date | null` — Timestamp (`@Column({ type: 'timestamp', nullable: true })`)
  - `onTheWayAt: Date | null` — Timestamp (`@Column({ type: 'timestamp', nullable: true })`)
  - `deliveredAt: Date | null` — Timestamp (`@Column({ type: 'timestamp', nullable: true })`)
  - `createdAt: Date` — Timestamptz (`@CreateDateColumn({ type: 'timestamptz' })`)
  - `updatedAt: Date` — Timestamptz (`@UpdateDateColumn({ type: 'timestamptz' })`)
  - `items: OrderItem[]` — Relación OneToMany
  - `cancellationReason: string | null` — Text (`@Column({ type: 'text', nullable: true })`)
  - `gatewayPaymentId: string | null` — Varchar(100) (`@Column({ type: 'varchar', length: 100, nullable: true })`)
  - `deliveryCode: string | null` — Varchar(12) (`@Column({ type: 'varchar', length: 12, nullable: true })`)
- **Relaciones TypeORM (Total: 6):**
  1. `@ManyToOne(() => Distributor, { nullable: false })`
     `@JoinColumn({ name: 'distributor_id' })`
     `distributor?: Distributor;`
     - **Entidad destino:** `Distributor`
     - **Dirección:** `Order` es dueña de la FK (`distributor_id`).
  2. `@ManyToOne(() => User, (user) => user.customer, { onDelete: 'RESTRICT' })`
     `@JoinColumn({ name: 'customer_id' })`
     `customer: User;`
     - **Entidad destino:** `User`
     - **Dirección:** `Order` es dueña de la FK (`customer_id`).
  3. `@ManyToOne(() => Delivery, { nullable: true })`
     `@JoinColumn({ name: 'delivery_id' })`
     `delivery: Delivery;`
     - **Entidad destino:** `Delivery`
     - **Dirección:** `Order` es dueña de la FK (`delivery_id`).
  4. `@ManyToOne(() => TimeSlot, { nullable: true })`
     `@JoinColumn({ name: 'time_slot_id' })`
     `timeSlot: TimeSlot;`
     - **Entidad destino:** `TimeSlot`
     - **Dirección:** `Order` es dueña de la FK (`time_slot_id`).
  5. `@ManyToOne(() => UserAddress)`
     `@JoinColumn({ name: 'address_id' })`
     `address: UserAddress;`
     - **Entidad destino:** `UserAddress`
     - **Dirección:** `Order` es dueña de la FK (`address_id`).
  6. `@OneToMany(() => OrderItem, (item) => item.order, { cascade: true })`
     `items: OrderItem[];`
     - **Entidad destino:** `OrderItem`
     - **Dirección:** Lado inverso (la FK `order_id` reside en `OrderItem`).

---

### 2. OrderItem
- **Ubicación:** `src/order/entities/order-item.entity.ts:14`
- **Tabla:** `@Entity('order_item')`
- **Propiedades:**
  - `order_item_id: string` — PK UUID (`@PrimaryGeneratedColumn('uuid', { name: 'order_item_id' })`)
  - `order: Order` — Relación ManyToOne (no nullable)
  - `order_id: string` — UUID (`@Column({ type: 'uuid' })`)
  - `gasCylinder: GasCylinder` — Relación ManyToOne (no nullable)
  - `gas_cylinder_id: string` — UUID (`@Column({ type: 'uuid' })`)
  - `quantity: number` — Int (`@Column({ type: 'int' })`)
  - `unitPrice: number` — Decimal (`@Column({ type: 'decimal', precision: 10, scale: 2 })`)
  - `subtotal: number` — Decimal (`@Column({ type: 'decimal', precision: 10, scale: 2 })`)
- **Relaciones TypeORM (Total: 2):**
  1. `@ManyToOne(() => Order, (order) => order.items, { onDelete: 'CASCADE' })`
     `@JoinColumn({ name: 'order_id' })`
     `order: Order;`
     - **Entidad destino:** `Order`
     - **Dirección:** `OrderItem` es dueña de la FK (`order_id`); lado inverso es `Order.items`.
  2. `@ManyToOne(() => GasCylinder)`
     `@JoinColumn({ name: 'gas_cylinder_id' })`
     `gasCylinder: GasCylinder;`
     - **Entidad destino:** `GasCylinder`
     - **Dirección:** `OrderItem` es dueña de la FK (`gas_cylinder_id`).

---

### 3. GasCylinder
- **Ubicación:** `src/gascylinder/entities/gascylinder.entity.ts:16`
- **Tabla:** `@Entity('gas_cylinder')`
- **Propiedades:**
  - `gas_cylinder_id: string` — PK UUID (`@PrimaryGeneratedColumn('uuid', { name: 'gas_cylinder_id' })`)
  - `distributor?: Distributor` — Relación ManyToOne (opcional en TS, nullable: false en BD)
  - `distributor_id?: string` — UUID (`@Column({ type: 'uuid', nullable: false })`)
  - `type: string` — Varchar(50) (`@Column({ type: 'varchar', length: 50 })`) (ej. '10kg', '15kg', '45kg')
  - `weight: number` — Decimal (`@Column({ type: 'decimal', precision: 10, scale: 2 })`)
  - `price: number` — Decimal (`@Column({ type: 'decimal', precision: 10, scale: 2 })`)
  - `stock: number` — Int (`@Column({ type: 'int', default: 0 })`)
  - `description: string` — Text (`@Column({ type: 'text', nullable: true })`)
  - `isActive: boolean` — Boolean (`@Column({ type: 'boolean', default: true })`)
  - `promotions: { quantity: number; discountPercentage: number }[]` — Jsonb (`@Column({ type: 'jsonb', nullable: true })`)
  - `createdAt: Date` — Timestamptz (`@CreateDateColumn({ type: 'timestamptz' })`)
  - `updatedAt: Date` — Timestamptz (`@UpdateDateColumn({ type: 'timestamptz' })`)
- **Relaciones TypeORM (Total: 1):**
  1. `@ManyToOne(() => Distributor, { nullable: false })`
     `@JoinColumn({ name: 'distributor_id' })`
     `distributor?: Distributor;`
     - **Entidad destino:** `Distributor`
     - **Dirección:** `GasCylinder` es dueña de la FK (`distributor_id`).

---

### 4. Delivery
- **Ubicación:** `src/delivery/entities/delivery.entity.ts:16`
- **Tabla:** `@Entity('delivery')`
- **Propiedades:**
  - `delivery_id: string` — PK UUID (`@PrimaryGeneratedColumn('uuid', { name: 'delivery_id' })`)
  - `distributor?: Distributor` — Relación ManyToOne (opcional en TS, nullable: false en BD)
  - `distributor_id?: string` — UUID (`@Column({ type: 'uuid', nullable: false })`)
  - `user: User` — Relación OneToOne (no nullable)
  - `user_id: string` — UUID (`@Column({ type: 'uuid' })`)
  - `calification?: number` — Double precision (`@Column({ type: 'double precision', nullable: true })`)
  - `latLng?: string` — Text (`@Column({ type: 'text', nullable: true })`)
  - `actual_location?: string` — Text (`@Column({ type: 'text', nullable: true })`)
  - `cancelledCharge?: number` — Real (`@Column({ type: 'real', nullable: true })`)
  - `validated: boolean` — Boolean (`@Column({ type: 'boolean', default: false })`)
  - `isActive: boolean` — Boolean (`@Column({ type: 'boolean', default: true })`)
  - `notification_token?: string` — Text (`@Column({ type: 'text', nullable: true })`)
  - `isTraveling?: string` — Text (`@Column({ type: 'text', nullable: true })`)
  - `balance: number` — Double precision (`@Column({ type: 'double precision', default: 0 })`)
  - `createdAt?: Date` — Timestamptz (`@CreateDateColumn({ type: 'timestamptz', nullable: true })`)
  - `deletedAt?: Date` — Timestamptz (`@DeleteDateColumn({ type: 'timestamptz', nullable: true })`)
- **Relaciones TypeORM (Total: 2):**
  1. `@ManyToOne(() => Distributor, { nullable: false })`
     `@JoinColumn({ name: 'distributor_id' })`
     `distributor?: Distributor;`
     - **Entidad destino:** `Distributor`
     - **Dirección:** `Delivery` es dueña de la FK (`distributor_id`).
  2. `@OneToOne(() => User, (user) => user.delivery, { onDelete: 'CASCADE' })`
     `@JoinColumn({ name: 'user_id' })`
     `user: User;`
     - **Entidad destino:** `User`
     - **Dirección:** `Delivery` es dueña de la FK (`user_id`); lado inverso es `User.delivery`.

---

### 5. Claim
- **Ubicación:** `src/claims/entities/claim.entity.ts:22`
- **Tabla:** `@Entity('claims')`
- **Propiedades:**
  - `claim_id: string` — PK UUID (`@PrimaryGeneratedColumn('uuid')`)
  - `distributor?: Distributor` — Relación ManyToOne (opcional en TS, nullable: false en BD)
  - `distributor_id?: string` — UUID (`@Column({ type: 'uuid', nullable: false })`)
  - `order: Order` — Relación ManyToOne (no nullable)
  - `order_id: string` — String (`@Column()`)
  - `customer: User` — Relación ManyToOne (no nullable)
  - `customer_id: string` — String (`@Column()`)
  - `reason: string` — String (`@Column()`)
  - `description: string` — Text (`@Column('text')`)
  - `photoUrl: string` — String (`@Column({ nullable: true })`)
  - `status: ClaimStatus` — Enum ClaimStatus (`@Column({ type: 'enum', enum: ClaimStatus, default: ClaimStatus.PENDING })`)
  - `resolutionNote: string` — Text (`@Column({ type: 'text', nullable: true })`)
  - `createdAt: Date` — Date (`@CreateDateColumn()`)
- **Relaciones TypeORM (Total: 3):**
  1. `@ManyToOne(() => Distributor, { nullable: false })`
     `@JoinColumn({ name: 'distributor_id' })`
     `distributor?: Distributor;`
     - **Entidad destino:** `Distributor`
     - **Dirección:** `Claim` es dueña de la FK (`distributor_id`).
  2. `@ManyToOne(() => Order)`
     `@JoinColumn({ name: 'order_id' })`
     `order: Order;`
     - **Entidad destino:** `Order`
     - **Dirección:** `Claim` es dueña de la FK (`order_id`).
  3. `@ManyToOne(() => User)`
     `@JoinColumn({ name: 'customer_id' })`
     `customer: User;`
     - **Entidad destino:** `User`
     - **Dirección:** `Claim` es dueña de la FK (`customer_id`).

---

### 6. Customer
- **Ubicación:** `src/customer/entities/customer.entity.ts:13`
- **Tabla:** `@Entity('customer')`
- **Propiedades:**
  - `customer_id: string` — PK UUID (`@PrimaryGeneratedColumn('uuid', { name: 'customer_id' })`)
  - `user: User` — Relación OneToOne (no nullable)
  - `user_id: string` — UUID (`@Column({ type: 'uuid' })`)
  - `notification_token?: string` — Text (`@Column({ type: 'text', nullable: true })`)
  - `lat_lang?: string` — Text (`@Column({ type: 'text', nullable: true })`)
  - `validated?: string` — Text (`@Column({ type: 'text', nullable: true })`)
  - `createdAt?: Date` — Timestamptz (`@CreateDateColumn({ type: 'timestamptz', nullable: true })`)
  - `deletedAt?: Date` — Timestamptz (`@DeleteDateColumn({ type: 'timestamptz', nullable: true })`)
- **Relaciones TypeORM (Total: 1):**
  1. `@OneToOne(() => User, (user) => user.customer, { onDelete: 'CASCADE' })`
     `@JoinColumn({ name: 'user_id' })`
     `user: User;`
     - **Entidad destino:** `User`
     - **Dirección:** `Customer` es dueña de la FK (`user_id`); lado inverso es `User.customer`.

---

### 7. User
- **Ubicación:** `src/users/entities/user.entity.ts:20`
- **Tabla:** `@Entity('user')`
- **Propiedades:**
  - `user_id: string` — PK UUID (`@PrimaryGeneratedColumn('uuid', { name: 'user_id' })`)
  - `role?: Role` — Relación ManyToOne (nullable: true)
  - `role_id?: string` — UUID (`@Column({ type: 'uuid', nullable: true })`)
  - `firebase_uid?: string` — Varchar (`@Column({ type: 'varchar', nullable: true })`)
  - `full_name?: string` — Varchar (`@Column({ type: 'varchar', nullable: true })`)
  - `selfie?: string` — Varchar (`@Column({ type: 'varchar', nullable: true })`)
  - `email?: string` — Varchar (`@Column({ type: 'varchar', unique: true, nullable: true })`)
  - `phone_number?: string` — Varchar (`@Column({ type: 'varchar', unique: true, nullable: true })`)
  - `phone_verified: boolean` — Boolean (`@Column({ type: 'boolean', default: false })`)
  - `email_verified: boolean` — Boolean (`@Column({ type: 'boolean', default: false })`)
  - `blocked: boolean` — Boolean (`@Column({ type: 'boolean', default: false })`)
  - `createdAt: Date` — Timestamptz (`@CreateDateColumn({ type: 'timestamptz' })`)
  - `deletedAt?: Date` — Timestamptz (`@DeleteDateColumn({ type: 'timestamptz', nullable: true })`)
  - `customer?: Customer` — Relación OneToOne
  - `delivery?: Delivery` — Relación OneToOne
  - `cars?: Car[]` — Relación OneToMany
  - `admins?: Admin[]` — Relación OneToMany
  - `addresses?: UserAddress[]` — Relación OneToMany
- **Relaciones TypeORM (Total: 6):**
  1. `@ManyToOne(() => Role, (role) => role.users, { nullable: true })`
     `@JoinColumn({ name: 'role_id' })`
     `role?: Role;`
     - **Entidad destino:** `Role`
     - **Dirección:** `User` es dueña de la FK (`role_id`); lado inverso es `Role.users`.
  2. `@OneToOne(() => Customer, (customer) => customer.user, { cascade: true })`
     `customer?: Customer;`
     - **Entidad destino:** `Customer`
     - **Dirección:** Lado inverso (la FK `user_id` está en `Customer`).
  3. `@OneToOne(() => Delivery, (delivery) => delivery.user, { cascade: true })`
     `delivery?: Delivery;`
     - **Entidad destino:** `Delivery`
     - **Dirección:** Lado inverso (la FK `user_id` está en `Delivery`).
  4. `@OneToMany(() => Car, (car) => car.user, { cascade: true })`
     `cars?: Car[];`
     - **Entidad destino:** `Car`
     - **Dirección:** Lado inverso (la FK `user_id` está en `Car`).
  5. `@OneToMany(() => Admin, (admin) => admin.user)`
     `admins?: Admin[];`
     - **Entidad destino:** `Admin`
     - **Dirección:** Lado inverso (la FK `user_id` está en `Admin`).
  6. `@OneToMany(() => UserAddress, (userAddress) => userAddress.user, { cascade: true })`
     `addresses?: UserAddress[];`
     - **Entidad destino:** `UserAddress`
     - **Dirección:** Lado inverso (la FK `user_id` está en `UserAddress`).
