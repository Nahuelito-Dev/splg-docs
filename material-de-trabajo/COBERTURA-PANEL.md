# Cobertura del panel sobre la API (26/09/2026)

El panel es la base de todo lo demás: tiene que reflejar todo lo que hace el
back para los roles `admin` y `super_admin`. Relevamiento cruzando el OpenAPI
(131 endpoints) con las funciones de `splg-app-admin/src/services/api`: **64
usados**. De los 67 restantes, una parte es propia de las apps (el chofer
reporta su posición, el cliente califica o confirma con el QR) o de
infraestructura; lo que sigue es lo que un administrador puede hacer en la API y
el panel todavía no ofrece.

## 1. Choferes — lo más importante

| Endpoint | Qué falta en el panel |
|---|---|
| `PATCH /delivery/{id}/validate` · `/invalidate` | **Validar o invalidar al chofer (CU-032).** Sin esto un chofer nuevo no puede trabajar. |
| `PATCH /delivery/{id}/status` | Habilitar o deshabilitar la cuenta del chofer. |
| `PATCH /delivery/user/{id}/availability` | Ponerlo disponible o no disponible (ON/OFF) desde el panel. |
| `PATCH /delivery/{id}/balance` | Ajustar el saldo del chofer con la distribuidora. |
| `GET /orders/delivery/{id}` | Historial de pedidos del chofer en su ficha. |

## 2. Pedidos

| Endpoint | Qué falta |
|---|---|
| `GET /orders/{id}` | Ficha del pedido con URL propia (`/orders/:id`), para compartirla o llegar desde una notificación. |
| `PATCH /orders/{id}/status` | Cambio manual de estado (con las transiciones que valida el back). |
| `DELETE /orders/{id}` | Cancelación forzada; revisar contra `PATCH /orders/{id}/cancel`, que es la que usa hoy el panel. |
| `GET /orders/{id}/delivery-code` · `POST /orders/{id}/confirm-delivery` | Soporte: ver el código de entrega y confirmar la entrega en nombre del cliente. |
| `PATCH /orders/{id}/arrived` | Avisar al cliente que el chofer llegó. |

## 3. Clientes

| Endpoint | Qué falta |
|---|---|
| `PATCH /customers/{id}` | Editar los datos del cliente. |
| `GET/POST/PATCH/DELETE /user-address…` · `set-default` | Ver y administrar las direcciones del cliente y cuál es la predeterminada. |

## 4. Plataforma (administrador general)

| Endpoint | Qué falta |
|---|---|
| `DELETE /distributor/{id}` | Dar de baja una distribuidora. |
| `GET /health/ready` | Estado del sistema (base y Redis) a la vista. |
| `POST /email/test` · `POST /notifications/send-test` | Probar el envío de correos y de notificaciones push. |
| `GET/POST/PATCH/DELETE /role`, `POST /role/seed` | Roles del sistema. |

## 5. Atención al cliente

| Endpoint | Qué falta |
|---|---|
| `POST /claims` | Cargar un reclamo en nombre del cliente (por teléfono). |
| `POST /incidents` | Registrar una incidencia de entrega desde el panel. |

## 6. Más información en lo que ya existe

Cada tabla pasa a mostrar 4 o 5 columnas clave, y **todo** lo que devuelve la API
de ese registro va en su vista de detalle (hoy varias vistas muestran una parte).
Registros sin vista de detalle hasta ahora: reservas, reclamos, incidencias,
vehículos y distribuidoras.

## Orden de trabajo

1. Tablas de 4-5 columnas y detalles completos (en curso).
2. Choferes (validación, estado, disponibilidad, saldo, historial).
3. Pedidos (ficha con URL, estado manual, soporte de entrega).
4. Clientes (edición y direcciones).
5. Plataforma y atención al cliente.

Antes de cada punto se verifica en el back qué hace exactamente el endpoint
(roles, transiciones, efectos) y se prueba contra la API; el panel no promete
nada que la API no haga.
