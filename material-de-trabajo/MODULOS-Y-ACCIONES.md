# Módulos, endpoints y qué hacer con cada uno

Cada endpoint probado contra la API corriendo con el rol que le corresponde.
La columna **Qué hacer** sale de los hallazgos verificados; el código entre
paréntesis remite a `HALLAZGOS-2026-09-23.md`.

| Estado | Qué significa |
|---|---|
| **anda** | Respondió correctamente |
| **anda (regla)** | Rechazó aplicando una regla de negocio. El endpoint funciona |
| **pendiente** | No se pudo ejercitar con los datos disponibles |
| **roto** | Devuelve 500 |

## Resumen

| Módulo | Endpoints | En pie | A arreglar | A refactorizar | Estado |
|---|---:|---:|---:|---:|---|
| Admin | 5 | 4 | 0 | 1 | casi completo |
| Auth | 3 | 3 | 2 | 0 | **completo** |
| Cars | 7 | 7 | 0 | 0 | **completo** |
| Claims | 3 | 3 | 0 | 0 | **completo** |
| Coverage Zones | 4 | 4 | 2 | 0 | **completo** |
| Customers | 8 | 8 | 1 | 0 | **completo** |
| Cylinders | 6 | 6 | 0 | 0 | **completo** |
| Delivery | 12 | 12 | 4 | 0 | **completo** |
| Distributors | 5 | 4 | 0 | 0 | casi completo |
| Email | 3 | 3 | 1 | 0 | **completo** |
| Gas Cylinders | 8 | 8 | 1 | 0 | **completo** |
| Health | 3 | 3 | 0 | 0 | **completo** |
| Incidents | 4 | 4 | 0 | 0 | **completo** |
| Notifications | 4 | 4 | 3 | 0 | **completo** |
| Orders | 19 | 19 | 0 | 2 | **completo** |
| Ratings | 3 | 3 | 0 | 0 | **completo** |
| Reports | 4 | 4 | 0 | 0 | **completo** |
| Role | 6 | 6 | 2 | 0 | **completo** |
| Time Slots | 5 | 5 | 0 | 1 | **completo** |
| User Addresses | 8 | 8 | 0 | 0 | **completo** |
| Users | 11 | 9 | 4 | 0 | casi completo |
| **Total** | **131** | **127** | **20** | **4** | |

De los 131 endpoints, **127 están en pie**. **20 hay que arreglarlos** y **4 refactorizarlos**, aunque hoy respondan: son defectos de contrato, de seguridad o de nombre.

## Detalle por módulo

### Admin — 4/5 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/admin` | anda | — |
| POST | `/api/admin/first-superadmin` | anda (regla) | — |
| POST | `/api/admin/register` | pendiente | revisar el dato de prueba — {"statusCode":400,"message":"Error creando usuario en Firebase: Invali |
| GET | `/api/admin` | anda | — |
| GET | `/api/admin/term/{term}` | anda | **REFACTORIZAR** (—) — se llama 'term' pero busca por UUID o email exacto, no por texto |

### Auth — 3/3 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/auth` | anda | — |
| POST | `/api/auth/login` | anda | **ARREGLAR** (H-02 · H-18) — devuelve el objeto crudo de Firebase (refreshToken, apiKey) y da token a usuarios dados de baja |
| POST | `/api/auth/login/dashboard` | anda | **ARREGLAR** (H-02 · H-18) — igual que el anterior |

### Cars — 7/7 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/car` | anda | — |
| GET | `/api/car` | anda | — |
| GET | `/api/car/patent/{patent}` | anda | — |
| GET | `/api/car/user/{userId}` | anda | — |
| GET | `/api/car/{id}` | anda | — |
| PATCH | `/api/car/{id}` | anda | — |
| DELETE | `/api/car/{id}` | anda | — |

### Claims — 3/3 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/claims` | anda | — |
| GET | `/api/claims` | anda | — |
| PATCH | `/api/claims/{id}/resolve` | anda | — |

### Coverage Zones — 4/4 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/coverage-zones` | anda | **ARREGLAR** (H-34) — no valida el polígono: con lat y lng invertidos guarda una zona inservible y responde 201 |
| GET | `/api/coverage-zones` | anda | — |
| GET | `/api/coverage-zones/check` | anda | **ARREGLAR** (H-09) — exige lat y lng pero el OpenAPI no los declara |
| DELETE | `/api/coverage-zones/{id}` | anda | — |

### Customers — 8/8 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| GET | `/api/customers` | anda | — |
| GET | `/api/customers/user/{userId}` | anda | — |
| GET | `/api/customers/{id}` | anda | — |
| PATCH | `/api/customers/{id}` | anda | — |
| PATCH | `/api/customers/{id}/invalidate` | anda | — |
| PATCH | `/api/customers/{id}/location` | anda | **ARREGLAR** (H-31) — sin DTO: acepta el campo mal escrito y devuelve 200 sin actualizar |
| PATCH | `/api/customers/{id}/validate` | anda | — |
| DELETE | `/api/customers/{id}` | anda | — |

### Cylinders — 6/6 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/cylinders` | anda | — |
| POST | `/api/cylinders/assign` | anda (regla) | — |
| GET | `/api/cylinders` | anda | — |
| GET | `/api/cylinders/{id}` | anda | — |
| GET | `/api/cylinders/{id}/history` | anda | — |
| PATCH | `/api/cylinders/{id}/transition` | anda | — |

### Delivery — 12/12 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| GET | `/api/delivery` | anda | — |
| GET | `/api/delivery/active` | anda | — |
| GET | `/api/delivery/user/{userId}` | anda | — |
| GET | `/api/delivery/{id}` | anda | — |
| PATCH | `/api/delivery/user/{userId}/availability` | anda | **ARREGLAR** (H-31) — sin DTO |
| PATCH | `/api/delivery/{id}` | anda | — |
| PATCH | `/api/delivery/{id}/balance` | anda | **ARREGLAR** (H-31) — sin DTO: mueve dinero sin validar el monto |
| PATCH | `/api/delivery/{id}/invalidate` | anda | — |
| PATCH | `/api/delivery/{id}/location` | anda | **ARREGLAR** (H-31) — sin DTO |
| PATCH | `/api/delivery/{id}/status` | anda | **ARREGLAR** (H-31) — sin DTO |
| PATCH | `/api/delivery/{id}/validate` | anda | — |
| DELETE | `/api/delivery/{id}` | anda | — |

### Distributors — 4/5 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/distributor` | anda | — |
| GET | `/api/distributor` | anda | — |
| GET | `/api/distributor/{id}` | anda | — |
| PATCH | `/api/distributor/{id}` | anda | — |
| DELETE | `/api/distributor/{id}` | no probado | — |

### Email — 3/3 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/email/change-email` | anda (regla) | — |
| POST | `/api/email/password-reset` | anda (regla) | **ARREGLAR** (H-30) — Firebase rechaza el dominio: falta autorizarlo en el proyecto |
| POST | `/api/email/test` | anda | — |

### Gas Cylinders — 8/8 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/gascylinder` | anda | — |
| GET | `/api/gascylinder` | anda | — |
| GET | `/api/gascylinder/available/list` | anda | — |
| GET | `/api/gascylinder/type/{type}` | anda | — |
| GET | `/api/gascylinder/{id}` | anda | — |
| PATCH | `/api/gascylinder/{id}` | anda | — |
| PATCH | `/api/gascylinder/{id}/stock` | anda | **ARREGLAR** (H-24 · H-31) — sin DTO: un valor no numerico llega a Postgres y da 500 |
| DELETE | `/api/gascylinder/{id}` | anda | — |

### Health — 3/3 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| GET | `/api/health` | anda | — |
| GET | `/api/health/live` | anda | — |
| GET | `/api/health/ready` | anda | — |

### Incidents — 4/4 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/incidents` | anda | — |
| GET | `/api/incidents` | anda | — |
| GET | `/api/incidents/order/{orderId}` | anda | — |
| PATCH | `/api/incidents/{id}/resolve` | anda | — |

### Notifications — 4/4 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/notifications/order-confirmation` | anda | **ARREGLAR** (H-31) — sin DTO |
| POST | `/api/notifications/send-test` | anda | **ARREGLAR** (H-31) — sin DTO |
| POST | `/api/notifications/token` | anda | **ARREGLAR** (H-31) — sin DTO |
| GET | `/api/notifications/user/{userId}` | anda | — |

### Orders — 19/19 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/orders` | anda | **REFACTORIZAR** (H-25) — customerId es en realidad un user_id: la columna lleva el nombre de otra entidad |
| POST | `/api/orders/{id}/confirm-delivery` | anda (regla) | — |
| POST | `/api/orders/{id}/reject` | anda | — |
| GET | `/api/orders` | anda | — |
| GET | `/api/orders/available` | anda | — |
| GET | `/api/orders/customer/{customerId}` | anda | — |
| GET | `/api/orders/delivery/{deliveryId}` | anda | — |
| GET | `/api/orders/reservations` | anda | — |
| GET | `/api/orders/stats/chart` | anda | — |
| GET | `/api/orders/stats/summary` | anda | — |
| GET | `/api/orders/{id}` | anda | — |
| GET | `/api/orders/{id}/delivery-code` | anda (regla) | — |
| PATCH | `/api/orders/{id}/arrived` | anda (regla) | — |
| PATCH | `/api/orders/{id}/assign/{deliveryId}` | anda | — |
| PATCH | `/api/orders/{id}/cancel` | anda | **REFACTORIZAR** (H-33) — para el chofer no cancela: libera el pedido a pending. El nombre engaña |
| PATCH | `/api/orders/{id}/confirm-deposit` | anda (regla) | — |
| PATCH | `/api/orders/{id}/location` | anda | — |
| PATCH | `/api/orders/{id}/status` | anda (regla) | — |
| DELETE | `/api/orders/{id}` | anda (regla) | — |

### Ratings — 3/3 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/ratings` | anda (regla) | — |
| GET | `/api/ratings/user/{userId}` | anda | — |
| GET | `/api/ratings/user/{userId}/summary` | anda | — |

### Reports — 4/4 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| GET | `/api/reports/sales-by-driver` | anda | — |
| GET | `/api/reports/sales-by-payment` | anda | — |
| GET | `/api/reports/sales-by-product` | anda | — |
| GET | `/api/reports/sales-evolution` | anda | — |

### Role — 6/6 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/role` | anda | — |
| POST | `/api/role/seed` | anda | — |
| GET | `/api/role` | anda | — |
| GET | `/api/role/{id}` | anda | — |
| PATCH | `/api/role/{id}` | anda | **ARREGLAR** (H-29) — renombrar un rol del sistema rompe el registro: se buscan por texto |
| DELETE | `/api/role/{id}` | anda | **ARREGLAR** (H-17) — 500 al borrar un rol en uso; deberia ser 409 |

### Time Slots — 5/5 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/time-slot` | anda | — |
| GET | `/api/time-slot` | anda | **REFACTORIZAR** (H-21) — recibe la distribuidora por query y sólo por slug; los otros la piden por cabecera |
| GET | `/api/time-slot/availability` | anda | — |
| GET | `/api/time-slot/{id}` | anda | — |
| DELETE | `/api/time-slot/{id}` | anda | — |

### User Addresses — 8/8 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/user-address` | anda | — |
| GET | `/api/user-address` | anda | — |
| GET | `/api/user-address/user/{userId}` | anda | — |
| GET | `/api/user-address/user/{userId}/default` | anda | — |
| GET | `/api/user-address/{id}` | anda | — |
| PATCH | `/api/user-address/{id}` | anda | — |
| PATCH | `/api/user-address/{id}/set-default` | anda | — |
| DELETE | `/api/user-address/{id}` | anda | — |

### Users — 9/11 en pie

| Método | Ruta | Estado | Qué hacer |
|---|---|---|---|
| POST | `/api/users` | anda | — |
| POST | `/api/users/check-exists` | anda | **ARREGLAR** (H-27 · H-28 · H-31) — publico (permite enumerar cuentas), sin DTO, acepta email numerico |
| POST | `/api/users/customer-registration` | pendiente | revisar el dato de prueba — {"message":"Invalid phone number format. Use E.164 format: +1234567890 |
| POST | `/api/users/delivery-registration` | pendiente | **ARREGLAR** (H-22) — 500 si falta distributorId, que el DTO marca opcional y la columna exige |
| GET | `/api/users` | anda | — |
| GET | `/api/users/email/{email}` | anda | **ARREGLAR** (H-26) — PUBLICO: devuelve el usuario completo con firebase_uid sin token |
| GET | `/api/users/phone/{phoneNumber}` | anda | — |
| GET | `/api/users/{id}` | anda | — |
| PATCH | `/api/users/{id}` | anda | — |
| PATCH | `/api/users/{id}/block` | anda | **ARREGLAR** (H-31) — sin DTO: 500 si se lo llama sin cuerpo, y Swagger no documenta el cuerpo |
| DELETE | `/api/users/{id}` | anda | — |
