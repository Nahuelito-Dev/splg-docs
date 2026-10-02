# Normalización del modelo de datos — 25/09/2026

Análisis formal del esquema implementado (40 tablas, 93 claves foráneas, todas
declaradas). Se lee junto con `MODELO-DE-DOMINIO.md` (qué es cada entidad) y con
el diccionario de datos generado en `diagramas/base-de-datos/SPLG-modelo-de-datos.md`.

**Resultado:** el esquema está en **FNBC** en todas las tablas, salvo ocho
redundancias controladas (sección 4), cada una deliberada y con su porqué. No hay
dependencias multivaluadas ni de reunión que no se sigan de las claves, así que
también cumple **4FN y 5FN**. Las violaciones reales que había se corrigieron el
25/09 con migraciones que convierten los datos (sección 3).

---

## 1. Método

Para cada tabla se identificaron las claves candidatas (la primaria y los
`UNIQUE`) y las dependencias funcionales (DF) no triviales entre atributos, con
este criterio:

| Forma | Qué se verificó |
|---|---|
| 1FN | Cada columna guarda un valor atómico de un dominio; no hay grupos repetitivos (arreglos o listas dentro de una columna) ni valores compuestos en texto. |
| 2FN | Ningún atributo no primo depende de una parte de una clave compuesta. Todas las claves primarias son `uuid` simples, así que 2FN se sigue de 1FN; las claves candidatas compuestas (`UNIQUE` de dos columnas) se revisaron aparte. |
| 3FN | Ningún atributo no primo depende transitivamente de la clave (a través de otro atributo no primo). |
| FNBC | Todo determinante de una DF no trivial es clave candidata. |
| 4FN | No hay dependencias multivaluadas independientes dentro de una misma tabla. |
| 5FN | Toda dependencia de reunión se sigue de las claves candidatas. |

Los identificadores son sustitutos (`uuid`); donde el negocio tiene una clave
natural se declaró como `UNIQUE` (correo y teléfono del usuario, patente del
vehículo vigente, serie del envase por distribuidora, etc.), para que la DF que
esa clave natural determina quede también garantizada por la base.

## 2. Tabla por tabla

`→` indica dependencia funcional. Sólo se listan las DF no triviales además de
`PK → resto`.

| Tabla | Claves candidatas | DF relevantes | Forma |
|---|---|---|---|
| `distributor` | `distributor_id`, `slug` | `slug → resto` | FNBC |
| `role` | `role_id`, `type` | `type → role_id` | FNBC (`type` único desde el 25/09) |
| `user` | `user_id`, `email`, `phone_number`, `firebase_uid` | cada clave natural determina el resto | FNBC (`firebase_uid` único desde el 25/09) |
| `admin` | `admin_id`, `user_id` (único) | `user_id → distributor_id` | FNBC (ver 3.3) |
| `customer` | `customer_id`, `user_id` | `user_id → resto` | FNBC salvo 4.5 (estimación de recompra) |
| `user_address` | `address_id` | — | FNBC |
| `delivery` | `delivery_id`, `user_id` | `user_id → resto` | FNBC salvo 4.4 (calificación promedio) |
| `car` | `car_id`, `car_patent` entre vigentes | `car_patent → resto` | FNBC |
| `gas_cylinder` | `gas_cylinder_id`, (`distributor_id`, `type`) | (`distributor_id`, `type`) → resto | FNBC (la clave natural se declaró el 25/09, ver 3.8) |
| `gas_cylinder_promotion` | `promotion_id`, (`gas_cylinder_id`, `quantity`) | (`gas_cylinder_id`, `quantity`) → `discount_percentage` | FNBC |
| `cylinder` | `cylinder_id`, (`distributor_id`, `serial`) | — | FNBC salvo 4.6 (vencimiento) |
| `cylinder_movement` | `movement_id` | — | FNBC salvo 4.1 (distribuidora) |
| `cylinder_inspection` | `inspection_id` | — | FNBC salvo 4.1 |
| `cylinder_recovery_case` / `_notice` | `case_id` / `notice_id` | — | FNBC salvo 4.1 |
| `time_slot` | `time_slot_id` | — | FNBC |
| `coverage_zone` | `coverage_zone_id` | — | FNBC |
| `cart` | `cart_id`, (`user_id`, `distributor_id`) | (`user_id`, `distributor_id`) → resto | FNBC |
| `cart_item` | `cart_item_id`, (`cart_id`, `gas_cylinder_id`) | (`cart_id`, `gas_cylinder_id`) → `quantity`, `unit_price` | FNBC |
| `order` | `order_id` | — | FNBC salvo 4.2 (importes y marcas de tiempo) y 4.7 (foto de la zona) |
| `order_item` | `order_item_id` | `quantity`, `unitPrice` → `subtotal` | Viola 3FN: `subtotal` depende transitivamente de `quantity` y `unitPrice`, dos atributos no primos. Redundancia controlada, ver 4.2 |
| `order_status_history` | `history_id` | — | FNBC |
| `order_address_change` | `change_id` | — | FNBC |
| `order_dispatch_offer` | `offer_id` | — | FNBC salvo 4.1 |
| `route_batch` / `_stop` / `_offer` | ids; (`batch_id`, `order_id`) en paradas | — | FNBC salvo 4.1 |
| `payment` | `payment_id`, `gateway_payment_id` (si existe) | — | FNBC salvo 4.1 |
| `claims`, `incident`, `rating` | ids; (`order_id`, `from_role`) en calificaciones | `order_id → customer_id` en reclamos | Viola 3FN en `claims` (`customer_id` depende transitivamente de `order_id`). Redundancia controlada, ver 4.1 y 4.3 |
| `maintenance_plan` / `_task` / `_window_proposal` | ids | — | FNBC |
| `vehicle_usage_log` | `log_id`, (`car_id`, `day`) | (`car_id`, `day`) → resto | FNBC |
| `vehicle_assignment` | `assignment_id`; (`car_id`) único mientras `released_at` es nulo; (`delivery_id`) único mientras `released_at` es nulo | en la asignación abierta, `car_id → delivery_id` y `delivery_id → car_id`; `car_id → distributor_id` | FNBC salvo 4.1 (`distributor_id`). Los dos índices únicos parciales son la invariante de negocio a nivel de base: un vehículo no está en uso por dos choferes a la vez ni un chofer usa dos vehículos a la vez |
| `maintenance_task_attachment` | `attachment_id` | — | FNBC salvo 4.1 (`distributor_id`) |
| `repurchase_invitation` | `invitation_id` | — | FNBC (ver 3.4 sobre el pedido sugerido) |
| `module_config` | `config_id`, (`distributor_id`, `module`) | (`distributor_id`, `module`) → `params` | FNBC |
| `audit_log` | `audit_id` | — | FNBC |

## 3. Lo que se corrigió el 25/09

| # | Qué había | Qué violaba | Cómo quedó | Migración |
|---|---|---|---|---|
| 3.1 | `customer.lat_lang` y `delivery.latLng` guardaban `"latitud,longitud"` en un texto | **1FN**: valor compuesto, no atómico; la base no podía validarlo ni consultar por cercanía | columna `location` de tipo punto PostGIS (`geometry(Point, 4326)`) con índice espacial; la API sigue hablando `"lat,lng"` | `CoordenadasComoPunto` |
| 3.2 | `gas_cylinder.promotions` era un arreglo JSON | **1FN**: grupo repetitivo; la base no podía impedir dos promociones para la misma cantidad | tabla `gas_cylinder_promotion`, una fila por promoción, `UNIQUE (producto, cantidad)` y rangos como `CHECK` | `PromocionesEnTabla` |
| 3.3 | `admin.role_id` repetía `user.role_id` | **3FN**: `admin_id → user_id → role_id` (transitiva). Además permitía que los dos dijeran cosas distintas: fue la causa del hallazgo H-77 | se quitó la columna; el rol es el del usuario; un perfil por usuario | `NormalizarAdminYChofer` |
| 3.4 | `user_address.latitude` y `longitude` eran dos `varchar` | dominio incorrecto (texto para un número) y redundante con el punto propuesto | punto `location`, igual que 3.1 | `ModeloPropuesto` |
| 3.5 | `customer.validated` era texto `'true'/'false'` | dominio incorrecto (admitía cualquier cadena); inconsistente con `delivery.validated`, que ya era booleano | booleano `NOT NULL DEFAULT false` | `ValidacionDelClienteBooleana` |
| 3.6 | `delivery.isTraveling` | atributo derivable (se deduce de los pedidos en camino) y además nunca escrito (0 filas con valor) | se quitó | `NormalizarAdminYChofer` |
| 3.8 | (`distributor_id`, `type`) de producto, `role.type` y `user.firebase_uid` eran claves naturales que el código daba por únicas y la base no garantizaba | **FNBC**: un determinante que no es clave candidata. Había un producto duplicado: la edición permitía cambiarle el tipo al de otro (H-88) | `UNIQUE` en los tres; la migración renombra el duplicado inactivo | `ClavesNaturalesUnicas` |
| 3.7 | 13 referencias sin clave foránea (pago → pedido, movimiento → envase, etc.) | integridad referencial: la base no validaba la DF de inclusión | se declararon las 13, con su regla de borrado | `DeclararRelacionesSinClaveForanea` |

Todas las migraciones convierten los datos en el lugar y son reversibles.

**Sobre los JSON que quedan.** No violan 1FN porque cada uno se guarda y se usa
como un valor indivisible, nunca se consulta por sus partes:

- `repurchase_invitation.suggested_items`: una foto del pedido sugerido en el
  momento de la invitación. Recién al aceptarla se crean `order` y `order_item`.
- `payment.metadata`: la respuesta de la pasarela, tal cual.
- `module_config.params`: los parámetros de un proceso, validados por su DTO.
- `audit_log.changes`: el cuerpo de la operación, depurado.

## 4. Redundancias controladas (desnormalizaciones justificadas)

Cada una rompe 3FN o FNBC en sentido estricto. Se mantienen porque ganan algo
concreto, y el sistema garantiza su consistencia en un único lugar.

| # | Redundancia | DF que la hace derivable | Por qué se mantiene | Quién la mantiene consistente |
|---|---|---|---|---|
| 4.1 | `distributor_id` copiado en `incident`, `claims`, `rating`, `payment`, `cylinder_movement`, `order_dispatch_offer`, `cylinder_inspection`, `vehicle_assignment` (desde `car`), `maintenance_task_attachment` (desde la tarea), el recupero y los lotes | `<fila> → order_id → distributor_id` (transitiva) | Aislamiento entre distribuidoras: cada consulta del panel filtra por distribuidora con un índice propio, sin unir con `order`. Es la columna sobre la que se apoya la regla "lo de otra distribuidora no existe" | El servicio la copia del pedido al crear la fila; nunca sale del cuerpo de la petición |
| 4.2 | `order.totalAmount`, `order_item.unitPrice` y `order_item.subtotal`; `order.acceptedAt`, `onTheWayAt` y `deliveredAt` | el total y el subtotal se calculan desde los renglones; las marcas de tiempo, desde `order_status_history` | Una venta es un hecho histórico: el precio y el descuento del momento no pueden cambiar si mañana cambia el catálogo. Las marcas se conservan porque los listados las leen sin unir tablas; el historial es la fuente de verdad | `CreateOrderUseCase` fija precios con la promoción vigente; la máquina de estados de pedido escribe las marcas |
| 4.3 | `claims.customer_id` | `claim_id → order_id → customer_id` | Un reclamo se filtra y se autoriza por cliente ("sólo el dueño del pedido reclama"); la columna evita unir con `order` en cada consulta | `ClaimsService` verifica que coincida con el cliente del pedido antes de guardar |
| 4.4 | `delivery.calification` | promedio de `rating.stars` recibidas | El despacho y el panel muestran el promedio en cada listado de choferes | `RatingService` lo recalcula al registrar cada calificación |
| 4.5 | `customer.next_repurchase_estimate_at` | se calcula del consumo declarado y del historial de pedidos | Es la entrada del proceso de recompra (M2), que recorre a todos los clientes cada día | El proceso de recompra (M2) al recalcular; todavía no está construido |
| 4.6 | `cylinder.last_inspection_at` y `expires_at` | se deducen de la última fila de `cylinder_inspection` | El despacho consulta el vencimiento en cada asignación de envases | El registro de una revisión (CU-133) los actualizará en la misma transacción; todavía no está construido |
| 4.7 | `order.zone_name`, `zone_surcharge_type`, `zone_surcharge_value` y `zone_surcharge_amount` | se derivan de la `coverage_zone` vigente al momento de pedir | La zona se puede editar o borrar después; estas cuatro columnas fijan la foto de lo que se cobró, para que un pedido viejo no cambie de total si la zona cambia. `order.subtotal_items` es la misma idea para el subtotal de los ítems (ver 4.2), separado del recargo de zona | `CreateOrderUseCase` las calcula una sola vez al crear el pedido; no se vuelven a tocar |
| 4.8 | `order.vehicle_car_id`, `vehicle_patent`, `vehicle_brand` y `vehicle_model` | se derivan del vehículo en uso del chofer (`vehicle_assignment` abierta) al aceptar el pedido | El vehículo se puede reasignar, editar o dar de baja después; estas cuatro columnas fijan con qué vehículo se hizo la entrega, para que un pedido viejo no cambie de patente si la flota cambia | La aceptación del pedido (`OrderService.assignDelivery` y la actualización de estado a aceptado) las copia una sola vez; no se vuelven a tocar |

**Dos vocabularios para el mismo hecho, sin que sea una redundancia de dato.**
`order.paymentStatus` y `payment.status` no guardan lo mismo con otro nombre: el
primero es el estado de cobro *del pedido*, en el vocabulario del dominio
(`pending`/`paid`/`failed`); el segundo es el estado de *esta transacción* en el
ledger, en el vocabulario de la pasarela (`pending`/`approved`/`rejected`/
`cancelled`/`refunded`), y un pedido puede tener más de un `payment` (reintentos).
`ConfirmPaymentUseCase` traduce el segundo al primero. Lo mismo
`order.gatewayPaymentId` (una copia de conveniencia del último pago aprobado,
para el índice único que garantiza la idempotencia del webhook) contra
`payment.gateway_payment_id` (el de cada intento). No se lista en la tabla de
redundancias porque no hay una dependencia funcional entre ambos: son dos
conceptos relacionados, no el mismo dato duplicado.

## 5. Lo que queda por decidir

- ~~`order.deliveryLatitude` y `deliveryLongitude` son dos `varchar`~~
  **Resuelto el 26/09:** pasaron a `order.deliveryPoint`, un punto PostGIS
  (geometry Point, 4326) con el mismo camino que 3.1. Es el punto de entrega,
  copiado de la dirección al crear el pedido: la dirección del cliente puede
  cambiar después (`order_address_change`). La posición del chofer no se guarda
  en el pedido, vive en Redis (H-91). La API sigue devolviendo latitud y
  longitud como texto; ninguna app las leía.
- `role.type` es texto (único) y no un enumerado de Postgres: el ABM de roles
  permite crear otros además de los cuatro del sistema.
- `delivery.actual_location` guarda una dirección legible derivada de la
  posición. Es una caché de presentación y no participa en ninguna regla.
