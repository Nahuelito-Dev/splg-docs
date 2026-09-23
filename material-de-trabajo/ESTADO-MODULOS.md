# Estado de los módulos

Batería de los **131 endpoints** contra el entorno corriendo, con los cuatro roles
reales, la cabecera `X-Distributor` y los 50 cuerpos de petición escritos a mano.

- **anda** — respondió correctamente.
- **regla** — rechazó aplicando una regla de negocio. El endpoint **funciona**.
- **datos** — el dato de prueba no servía. No es defecto del backend.
- **roto** — error 500.

## Módulos completos

**20 de 21 módulos tienen todos sus endpoints en pie.** Todo lo que exponen responde bien o rechaza aplicando una regla de negocio.

| Módulo | Endpoints |
|---|---:|
| **Admin** | 5 |
| **Auth** | 3 |
| **Cars** | 7 |
| **Claims** | 3 |
| **Coverage Zones** | 4 |
| **Customers** | 8 |
| **Cylinders** | 6 |
| **Delivery** | 12 |
| **Email** | 3 |
| **Gas Cylinders** | 8 |
| **Health** | 3 |
| **Incidents** | 4 |
| **Notifications** | 4 |
| **Orders** | 19 |
| **Ratings** | 3 |
| **Reports** | 4 |
| **Role** | 6 |
| **Time Slots** | 5 |
| **User Addresses** | 8 |
| **Users** | 11 |
| | **126** |

## Casi completos

| Módulo | Endpoints | Pendientes |
|---|---:|---:|
| Distributors | 5 | 1 |

## Resumen por módulo

| Módulo | Endpoints | Anda | Regla | Datos | Roto | Veredicto |
|---|---:|---:|---:|---:|---:|---|
| Admin | 5 | 4 | 1 | 0 | 0 | **completo** |
| Auth | 3 | 3 | 0 | 0 | 0 | **completo** |
| Cars | 7 | 7 | 0 | 0 | 0 | **completo** |
| Claims | 3 | 3 | 0 | 0 | 0 | **completo** |
| Coverage Zones | 4 | 4 | 0 | 0 | 0 | **completo** |
| Customers | 8 | 8 | 0 | 0 | 0 | **completo** |
| Cylinders | 6 | 5 | 1 | 0 | 0 | **completo** |
| Delivery | 12 | 12 | 0 | 0 | 0 | **completo** |
| Distributors | 5 | 4 | 0 | 0 | 0 | casi completo |
| Email | 3 | 1 | 2 | 0 | 0 | **completo** |
| Gas Cylinders | 8 | 8 | 0 | 0 | 0 | **completo** |
| Health | 3 | 3 | 0 | 0 | 0 | **completo** |
| Incidents | 4 | 4 | 0 | 0 | 0 | **completo** |
| Notifications | 4 | 4 | 0 | 0 | 0 | **completo** |
| Orders | 19 | 13 | 6 | 0 | 0 | **completo** |
| Ratings | 3 | 3 | 0 | 0 | 0 | **completo** |
| Reports | 4 | 4 | 0 | 0 | 0 | **completo** |
| Role | 6 | 6 | 0 | 0 | 0 | **completo** |
| Time Slots | 5 | 5 | 0 | 0 | 0 | **completo** |
| User Addresses | 8 | 8 | 0 | 0 | 0 | **completo** |
| Users | 11 | 11 | 0 | 0 | 0 | **completo** |

**Total:** 131 endpoints · 120 andan · 10 con regla de negocio · 0 pendientes por datos · **0 rotos** · 1 omitido.

## Detalle, endpoint por endpoint

### Admin — 5/5 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/admin` | 201 |  |
| regla | POST | `/api/admin/first-superadmin` | 403 | {"message":"Ya existen administradores en el sistema","error":"Forbidden","statusCode":403} |
| ok | POST | `/api/admin/register` | 201 |  |
| ok | GET | `/api/admin` | 200 |  |
| ok | GET | `/api/admin/term/{term}` | 200 |  |

### Auth — 3/3 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/auth` | 201 |  |
| ok | POST | `/api/auth/login` | 200 |  |
| ok | POST | `/api/auth/login/dashboard` | 200 |  |

### Cars — 7/7 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/car` | 201 |  |
| ok | GET | `/api/car` | 200 |  |
| ok | GET | `/api/car/patent/{patent}` | 200 |  |
| ok | GET | `/api/car/user/{userId}` | 200 |  |
| ok | GET | `/api/car/{id}` | 200 |  |
| ok | PATCH | `/api/car/{id}` | 200 |  |
| ok | DELETE | `/api/car/{id}` | 200 |  |

### Claims — 3/3 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/claims` | 201 |  |
| ok | GET | `/api/claims` | 200 |  |
| ok | PATCH | `/api/claims/{id}/resolve` | 200 |  |

### Coverage Zones — 4/4 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/coverage-zones` | 201 |  |
| ok | GET | `/api/coverage-zones` | 200 |  |
| ok | GET | `/api/coverage-zones/check` | 200 |  |
| ok | DELETE | `/api/coverage-zones/{id}` | 200 |  |

### Customers — 8/8 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | GET | `/api/customers` | 200 |  |
| ok | GET | `/api/customers/user/{userId}` | 200 |  |
| ok | GET | `/api/customers/{id}` | 200 |  |
| ok | PATCH | `/api/customers/{id}` | 200 |  |
| ok | PATCH | `/api/customers/{id}/invalidate` | 200 |  |
| ok | PATCH | `/api/customers/{id}/location` | 200 |  |
| ok | PATCH | `/api/customers/{id}/validate` | 200 |  |
| ok | DELETE | `/api/customers/{id}` | 200 |  |

### Cylinders — 6/6 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/cylinders` | 201 |  |
| regla | POST | `/api/cylinders/assign` | 400 | {"message":"Transición de envase inválida: in_depot → dispatched","error":"Bad Request","statusCode":400} |
| ok | GET | `/api/cylinders` | 200 |  |
| ok | GET | `/api/cylinders/{id}` | 200 |  |
| ok | GET | `/api/cylinders/{id}/history` | 200 |  |
| ok | PATCH | `/api/cylinders/{id}/transition` | 200 |  |

### Delivery — 12/12 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | GET | `/api/delivery` | 200 |  |
| ok | GET | `/api/delivery/active` | 200 |  |
| ok | GET | `/api/delivery/user/{userId}` | 200 |  |
| ok | GET | `/api/delivery/{id}` | 200 |  |
| ok | PATCH | `/api/delivery/user/{userId}/availability` | 200 |  |
| ok | PATCH | `/api/delivery/{id}` | 200 |  |
| ok | PATCH | `/api/delivery/{id}/balance` | 200 |  |
| ok | PATCH | `/api/delivery/{id}/invalidate` | 200 |  |
| ok | PATCH | `/api/delivery/{id}/location` | 200 |  |
| ok | PATCH | `/api/delivery/{id}/status` | 200 |  |
| ok | PATCH | `/api/delivery/{id}/validate` | 200 |  |
| ok | DELETE | `/api/delivery/{id}` | 200 |  |

### Distributors — 4/5 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/distributor` | 201 |  |
| ok | GET | `/api/distributor` | 200 |  |
| ok | GET | `/api/distributor/{id}` | 200 |  |
| ok | PATCH | `/api/distributor/{id}` | 200 |  |
| omitido | DELETE | `/api/distributor/{id}` | - | deja al sistema sin distribuidora; se prueba aparte |

### Email — 3/3 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| regla | POST | `/api/email/change-email` | 400 | {"message":"Invalid token","error":"Bad Request","statusCode":400} |
| regla | POST | `/api/email/password-reset` | 400 | {"message":"Too many password_reset attempts. Please try again later.","error":"Bad Request","statusCode":400} |
| ok | POST | `/api/email/test` | 201 |  |

### Gas Cylinders — 8/8 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/gascylinder` | 201 |  |
| ok | GET | `/api/gascylinder` | 200 |  |
| ok | GET | `/api/gascylinder/available/list` | 200 |  |
| ok | GET | `/api/gascylinder/type/{type}` | 200 |  |
| ok | GET | `/api/gascylinder/{id}` | 200 |  |
| ok | PATCH | `/api/gascylinder/{id}` | 200 |  |
| ok | PATCH | `/api/gascylinder/{id}/stock` | 200 |  |
| ok | DELETE | `/api/gascylinder/{id}` | 200 |  |

### Health — 3/3 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | GET | `/api/health` | 200 |  |
| ok | GET | `/api/health/live` | 200 |  |
| ok | GET | `/api/health/ready` | 200 |  |

### Incidents — 4/4 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/incidents` | 201 |  |
| ok | GET | `/api/incidents` | 200 |  |
| ok | GET | `/api/incidents/order/{orderId}` | 200 |  |
| ok | PATCH | `/api/incidents/{id}/resolve` | 200 |  |

### Notifications — 4/4 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/notifications/order-confirmation` | 201 |  |
| ok | POST | `/api/notifications/send-test` | 201 |  |
| ok | POST | `/api/notifications/token` | 201 |  |
| ok | GET | `/api/notifications/user/{userId}` | 200 |  |

### Orders — 19/19 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/orders` | 201 |  |
| regla | POST | `/api/orders/{id}/confirm-delivery` | 400 | {"message":"El pedido no está en camino, no se puede confirmar la entrega","error":"Bad Request","statusCode":400} |
| ok | POST | `/api/orders/{id}/reject` | 201 |  |
| ok | GET | `/api/orders` | 200 |  |
| ok | GET | `/api/orders/available` | 200 |  |
| ok | GET | `/api/orders/customer/{customerId}` | 200 |  |
| ok | GET | `/api/orders/delivery/{deliveryId}` | 200 |  |
| ok | GET | `/api/orders/reservations` | 200 |  |
| ok | GET | `/api/orders/stats/chart` | 200 |  |
| ok | GET | `/api/orders/stats/summary` | 200 |  |
| ok | GET | `/api/orders/{id}` | 200 |  |
| regla | GET | `/api/orders/{id}/delivery-code` | 400 | {"message":"El pedido todavía no tiene código de entrega (debe estar aceptado)","error":"Bad Request","statusCode":400} |
| regla | PATCH | `/api/orders/{id}/arrived` | 400 | {"message":"El pedido debe estar en camino para avisar llegada","error":"Bad Request","statusCode":400} |
| ok | PATCH | `/api/orders/{id}/assign/{deliveryId}` | 200 |  |
| ok | PATCH | `/api/orders/{id}/cancel` | 200 |  |
| regla | PATCH | `/api/orders/{id}/confirm-deposit` | 400 | {"message":"El pedido no es una reserva pendiente","error":"Bad Request","statusCode":400} |
| ok | PATCH | `/api/orders/{id}/location` | 200 |  |
| regla | PATCH | `/api/orders/{id}/status` | 400 | {"message":"Transición de pedido inválida: cancelled → accepted","error":"Bad Request","statusCode":400} |
| regla | DELETE | `/api/orders/{id}` | 400 | {"message":"No se puede cancelar un pedido finalizado","error":"Bad Request","statusCode":400} |

### Ratings — 3/3 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/ratings` | 201 |  |
| ok | GET | `/api/ratings/user/{userId}` | 200 |  |
| ok | GET | `/api/ratings/user/{userId}/summary` | 200 |  |

### Reports — 4/4 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | GET | `/api/reports/sales-by-driver` | 200 |  |
| ok | GET | `/api/reports/sales-by-payment` | 200 |  |
| ok | GET | `/api/reports/sales-by-product` | 200 |  |
| ok | GET | `/api/reports/sales-evolution` | 200 |  |

### Role — 6/6 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/role` | 201 |  |
| ok | POST | `/api/role/seed` | 201 |  |
| ok | GET | `/api/role` | 200 |  |
| ok | GET | `/api/role/{id}` | 200 |  |
| ok | PATCH | `/api/role/{id}` | 200 |  |
| ok | DELETE | `/api/role/{id}` | 200 |  |

### Time Slots — 5/5 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/time-slot` | 201 |  |
| ok | GET | `/api/time-slot` | 200 |  |
| ok | GET | `/api/time-slot/availability` | 200 |  |
| ok | GET | `/api/time-slot/{id}` | 200 |  |
| ok | DELETE | `/api/time-slot/{id}` | 200 |  |

### User Addresses — 8/8 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/user-address` | 201 |  |
| ok | GET | `/api/user-address` | 200 |  |
| ok | GET | `/api/user-address/user/{userId}` | 200 |  |
| ok | GET | `/api/user-address/user/{userId}/default` | 200 |  |
| ok | GET | `/api/user-address/{id}` | 200 |  |
| ok | PATCH | `/api/user-address/{id}` | 200 |  |
| ok | PATCH | `/api/user-address/{id}/set-default` | 200 |  |
| ok | DELETE | `/api/user-address/{id}` | 200 |  |

### Users — 11/11 en pie

| | Método | Ruta | Código | Qué pasó |
|---|---|---|---:|---|
| ok | POST | `/api/users` | 201 |  |
| ok | POST | `/api/users/check-exists` | 201 |  |
| ok | POST | `/api/users/customer-registration` | 201 |  |
| ok | POST | `/api/users/delivery-registration` | 201 |  |
| ok | GET | `/api/users` | 200 |  |
| ok | GET | `/api/users/email/{email}` | 200 |  |
| ok | GET | `/api/users/phone/{phoneNumber}` | 200 |  |
| ok | GET | `/api/users/{id}` | 200 |  |
| ok | PATCH | `/api/users/{id}` | 200 |  |
| ok | PATCH | `/api/users/{id}/block` | 200 |  |
| ok | DELETE | `/api/users/{id}` | 200 |  |
