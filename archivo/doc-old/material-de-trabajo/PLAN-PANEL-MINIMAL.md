# Plan: panel SPLG sobre Minimal — 01/10/2026

Material de trabajo (no entregable). Análisis de sólo lectura: no se tocó ningún
repo ni la base. Insumos verificados:

- Panel: `splg-app-admin` (rama `feat/panel-flota-documentacion`, 27 cambios sin
  commitear), React 18 · MUI 5 · DataGrid 6 · React Query 5 · Tailwind 3 ·
  Recharts 3 · Leaflet + Geoman · socket.io · Redux (sólo auth) · 22 páginas,
  ~13 k líneas en `src/pages`, 30 archivos de test.
- API: OpenAPI vivo de `splg-app-backend` en `:3010/docs-json` (148 endpoints).
- Plantilla: `~/Desktop/templates/Minimal_TypeScript_v7.3.0/{vite-ts,starter-vite-ts}`
  (React 19.1, MUI 7.1, DataGrid 8.5, react-router 7.6, Vite 6.3, `minimal-shared`).
- Relevamientos previos: `REUTILIZABLE-PLANTILLAS.md` y `COBERTURA-PANEL.md`
  (26/09: 131 endpoints / 64 usados; **quedó viejo**, ver §1).

> Cambio de criterio respecto de `REUTILIZABLE-PLANTILLAS.md`: aquel decía
> "adaptar piezas de Minimal a MUI 5 y no tomar su motor de tema". Este plan
> propone lo contrario: **Minimal entero como base** (tema MUI 7, layout,
> `minimal-shared`), porque el pedido ahora es rehacer el panel, no injertarle
> componentes.

---

## 1. Cobertura hoy

Fuente: OpenAPI vivo `GET http://localhost:3010/docs-json` (01/10/2026), **148 endpoints**; igual que `splg-app-admin/openapi/splg-api.json` (148). Cruce automático contra las llamadas `http.get/post/patch/delete` de `splg-app-admin/src/services/api/*.ts` (rama `feat/panel-flota-documentacion`, con 27 archivos sin commitear). Todas las funciones de servicio que llaman a un endpoint están importadas por alguna página o hook (las de `registration.ts` vía `createCustomer/createAdmin/createDriver`).

**Usados por el panel: 102/148 (68.9 %).** No usados: 46 = 11 propios de las apps o de infraestructura + 3 redundantes/a decidir + **32 que un admin debería tener y no tiene (21.6 %)**. Cobertura alcanzable para el panel: 134/148.

| Módulo | Usados | Total |
|---|---:|---:|
| Users | 6 | 8 |
| Registro | 1 | 3 |
| Admin | 1 | 3 |
| Role | 2 | 6 |
| Customers | 3 | 6 |
| Delivery | 6 | 12 |
| Distributors | 6 | 6 |
| Auth | 0 | 3 |
| Cars | 6 | 7 |
| Orders | 13 | 19 |
| Gas Cylinders | 6 | 8 |
| User Addresses | 5 | 8 |
| Notifications | 2 | 4 |
| Time Slots | 5 | 5 |
| Cylinders | 5 | 6 |
| Coverage Zones | 6 | 6 |
| Email | 1 | 3 |
| Claims | 3 | 3 |
| Reports | 4 | 4 |
| Health | 2 | 3 |
| Ratings | 2 | 3 |
| Incidents | 4 | 4 |
| Fleet · Plans | 1 | 4 |
| Fleet · Tasks | 8 | 10 |
| Fleet · Expirations | 1 | 1 |
| Fleet · Vehicle documents | 1 | 1 |
| Fleet · Driver documents | 1 | 1 |
| Audit | 1 | 1 |
| **Total** | **102** | **148** |

Leyenda: ✔ lo usa el panel · ✘ falta en el panel (admin) · app = es de las apps/infra · ? = redundante o a decidir.

**Users**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/users` | listUsers |
| ✘ | POST | `/users/check-exists` | CU-084 pre-chequeo en altas |
| ✔ | GET | `/users/email/{email}` | getAdmin |
| ✘ | GET | `/users/phone/{phoneNumber}` | búsqueda por teléfono |
| ✔ | DELETE | `/users/{id}` | deleteUser |
| ✔ | GET | `/users/{id}` | getUser |
| ✔ | PATCH | `/users/{id}` | updateUserAccount |
| ✔ | PATCH | `/users/{id}/block` | blockUser |

**Registro**

| | Método | Ruta | Nota |
|---|---|---|---|
| app | POST | `/auth/registro` |  |
| ✔ | POST | `/users` | registerUser |
| app | POST | `/users/customer-registration` |  |

**Admin**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/admin` | listAdmins |
| ? | POST | `/admin` | redundante con POST /users (alta única); decidir si se deprecia |
| ✘ | GET | `/admin/term/{term}` | CU-088 búsqueda |

**Role**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/role` | listRoles |
| ✘ | POST | `/role` | CU-089 (SA) |
| ✔ | POST | `/role/seed` | seedRoles |
| ✘ | DELETE | `/role/{id}` | CU-089 |
| ✘ | GET | `/role/{id}` | CU-089 |
| ✘ | PATCH | `/role/{id}` | CU-089 |

**Customers**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/customers` | listCustomers |
| ✘ | GET | `/customers/user/{userId}` | CU-130 |
| ✔ | DELETE | `/customers/{id}` | deleteCustomer |
| ✔ | GET | `/customers/{id}` | getCustomer |
| ✘ | PATCH | `/customers/{id}` | CU-131 |
| ✘ | PATCH | `/customers/{id}/location` | CU-094 |

**Delivery**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/delivery` | listDeliveries |
| ✔ | GET | `/delivery/active` | listActiveDeliveries |
| ✘ | GET | `/delivery/user/{userId}` | CU-110 |
| ✘ | PATCH | `/delivery/user/{userId}/availability` | ON/OFF del chofer |
| ✔ | DELETE | `/delivery/{id}` | deleteDelivery |
| ✔ | GET | `/delivery/{id}` | listActiveDeliveries,getDelivery |
| ✔ | PATCH | `/delivery/{id}` | updateDeliveryStatus |
| ✘ | PATCH | `/delivery/{id}/balance` | CU-049 |
| ✘ | PATCH | `/delivery/{id}/invalidate` | CU-032 **crítico** |
| app | PATCH | `/delivery/{id}/location` |  |
| ✔ | PATCH | `/delivery/{id}/status` | setDeliveryEnabled |
| ✘ | PATCH | `/delivery/{id}/validate` | CU-032 **crítico** |

**Distributors**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/distributor` | listDistributors |
| ✔ | POST | `/distributor` | createDistributor |
| ✔ | GET | `/distributor/current` | getCurrentDistributor |
| ✔ | DELETE | `/distributor/{id}` | deleteDistributor |
| ✔ | GET | `/distributor/{id}` | getCurrentDistributor |
| ✔ | PATCH | `/distributor/{id}` | updateDistributor |

**Auth**

| | Método | Ruta | Nota |
|---|---|---|---|
| ? | POST | `/auth` | validar token (CU-091); útil para el guard de sesión |
| app | POST | `/auth/login` |  |
| ? | POST | `/auth/login/dashboard` | el panel entra con Firebase directo + GET /users/email; decidir cuál es el login del panel |

**Cars**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/car` | listCars |
| ✔ | POST | `/car` | createCar |
| ✘ | GET | `/car/patent/{patent}` | CU-114 |
| ✔ | GET | `/car/user/{userId}` | listCarsByUser |
| ✔ | DELETE | `/car/{id}` | deleteCar |
| ✔ | GET | `/car/{id}` | getCar |
| ✔ | PATCH | `/car/{id}` | updateCar |

**Orders**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/orders` | listOrders |
| ✘ | POST | `/orders` | CU-072 reserva/pedido telefónico |
| ✘ | GET | `/orders/available` | CU-080 pool |
| ✔ | GET | `/orders/customer/{customerId}` | listCustomerOrders |
| ✘ | GET | `/orders/delivery/{deliveryId}` | CU-081 historial del chofer |
| ✔ | GET | `/orders/reservations` | listReservations |
| ✔ | GET | `/orders/stats/chart` | getSalesChart |
| ✔ | GET | `/orders/stats/summary` | getOrderStats |
| ✘ | DELETE | `/orders/{id}` | CU-010 (forzada) |
| ✔ | GET | `/orders/{id}` | listReservations,getOrder |
| ✔ | PATCH | `/orders/{id}/arrived` | notifyOrderArrival |
| ✔ | PATCH | `/orders/{id}/assign/{deliveryId}` | assignOrderDelivery |
| ✔ | PATCH | `/orders/{id}/cancel` | cancelOrder |
| ✔ | POST | `/orders/{id}/confirm-delivery` | confirmOrderDelivery |
| ✔ | PATCH | `/orders/{id}/confirm-deposit` | confirmReservationDeposit |
| ✔ | GET | `/orders/{id}/delivery-code` | getOrderDeliveryCode |
| app | PATCH | `/orders/{id}/location` |  |
| app | POST | `/orders/{id}/reject` |  |
| ✔ | PATCH | `/orders/{id}/status` | updateOrderStatus |

**Gas Cylinders**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/gascylinder` | listGasCylinders |
| ✔ | POST | `/gascylinder` | createGasCylinder |
| app | GET | `/gascylinder/available/list` |  |
| app | GET | `/gascylinder/type/{type}` |  |
| ✔ | DELETE | `/gascylinder/{id}` | deleteGasCylinder |
| ✔ | GET | `/gascylinder/{id}` | getGasCylinder |
| ✔ | PATCH | `/gascylinder/{id}` | updateGasCylinder |
| ✔ | PATCH | `/gascylinder/{id}/stock` | updateGasCylinderStock |

**User Addresses**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✘ | GET | `/user-address` | listado global (SA) |
| ✔ | POST | `/user-address` | createUserAddress |
| ✔ | GET | `/user-address/user/{userId}` | listUserAddresses |
| ✘ | GET | `/user-address/user/{userId}/default` | predeterminada en la ficha del cliente |
| ✔ | DELETE | `/user-address/{id}` | deleteUserAddress |
| ✘ | GET | `/user-address/{id}` | ficha de dirección |
| ✔ | PATCH | `/user-address/{id}` | updateUserAddress |
| ✔ | PATCH | `/user-address/{id}/set-default` | setDefaultUserAddress |

**Notifications**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✘ | POST | `/notifications/order-confirmation` | CU-101 (SA) |
| ✔ | POST | `/notifications/send-test` | sendTestNotification |
| app | POST | `/notifications/token` |  |
| ✔ | GET | `/notifications/user/{userId}` | getUserNotificationTokens |

**Time Slots**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/time-slot` | listTimeSlots |
| ✔ | POST | `/time-slot` | createTimeSlot |
| ✔ | GET | `/time-slot/availability` | getTimeSlotAvailability |
| ✔ | DELETE | `/time-slot/{id}` | deleteTimeSlot |
| ✔ | GET | `/time-slot/{id}` | getTimeSlotAvailability |

**Cylinders**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/cylinders` | listCylinders |
| ✔ | POST | `/cylinders` | createCylinder |
| ✔ | POST | `/cylinders/assign` | assignCylinders |
| ✘ | GET | `/cylinders/{id}` | ficha de envase con URL |
| ✔ | GET | `/cylinders/{id}/history` | getCylinderHistory |
| ✔ | PATCH | `/cylinders/{id}/transition` | transitionCylinder |

**Coverage Zones**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/coverage-zones` | listCoverageZones |
| ✔ | POST | `/coverage-zones` | createCoverageZone |
| ✔ | GET | `/coverage-zones/check` | checkCoverage |
| ✔ | DELETE | `/coverage-zones/{id}` | deleteCoverageZone |
| ✔ | GET | `/coverage-zones/{id}` | checkCoverage |
| ✔ | PATCH | `/coverage-zones/{id}` | updateCoverageZone |

**Email**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✘ | POST | `/email/change-email` | cambio de email (perfil/usuarios) |
| ✘ | POST | `/email/password-reset` | CU-047 "olvidé mi contraseña" en el login |
| ✔ | POST | `/email/test` | testEmailService |

**Claims**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/claims` | listClaims |
| ✔ | POST | `/claims` | createClaim |
| ✔ | PATCH | `/claims/{id}/resolve` | resolveClaim |

**Reports**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/reports/sales-by-driver` | getSalesByDriver |
| ✔ | GET | `/reports/sales-by-payment` | getSalesByPayment |
| ✔ | GET | `/reports/sales-by-product` | getSalesByProduct |
| ✔ | GET | `/reports/sales-evolution` | getSalesEvolution |

**Health**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/health` | getHealth |
| app | GET | `/health/live` |  |
| ✔ | GET | `/health/ready` | getReadiness |

**Ratings**

| | Método | Ruta | Nota |
|---|---|---|---|
| app | POST | `/ratings` |  |
| ✔ | GET | `/ratings/user/{userId}` | listRatingsForUser |
| ✔ | GET | `/ratings/user/{userId}/summary` | getRatingSummary |

**Incidents**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/incidents` | listIncidents |
| ✔ | POST | `/incidents` | createIncident |
| ✔ | GET | `/incidents/order/{orderId}` | listOrderIncidents |
| ✔ | PATCH | `/incidents/{id}/resolve` | resolveIncident |

**Fleet · Plans**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/fleet/plans` | listFleetPlans |
| ✘ | POST | `/fleet/plans` | CU-105/140 |
| ✘ | GET | `/fleet/plans/{id}` | CU-105 |
| ✘ | PATCH | `/fleet/plans/{id}` | CU-105 |

**Fleet · Tasks**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✘ | GET | `/fleet/tasks` | listado de tareas de flota |
| ✔ | POST | `/fleet/tasks` | createFleetTask |
| ✘ | GET | `/fleet/tasks/{id}` | ficha de tarea |
| ✔ | PATCH | `/fleet/tasks/{id}` | updateFleetTask |
| ✔ | GET | `/fleet/tasks/{id}/attachments` | listFleetTaskAttachments |
| ✔ | POST | `/fleet/tasks/{id}/attachments` | uploadFleetTaskAttachment |
| ✔ | DELETE | `/fleet/tasks/{id}/attachments/{attachmentId}` | deleteFleetTaskAttachment |
| ✔ | GET | `/fleet/tasks/{id}/attachments/{attachmentId}/download` | downloadFleetTaskAttachment |
| ✔ | PATCH | `/fleet/tasks/{id}/cancel` | cancelFleetTask |
| ✔ | PATCH | `/fleet/tasks/{id}/close` | closeFleetTask |

**Fleet · Expirations**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/fleet/expirations` | getFleetExpirations |

**Fleet · Vehicle documents**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/cars/{carId}/documents` | getCarDocuments |

**Fleet · Driver documents**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/delivery/{id}/documents` | getDriverDocuments |

**Audit**

| | Método | Ruta | Nota |
|---|---|---|---|
| ✔ | GET | `/audit` | listAudit |

### Lo que más pesa de los 32 faltantes

1. **Choferes:** validar/invalidar (CU-032, crítico), disponibilidad ON/OFF,
   saldo (CU-049), historial de pedidos (CU-081), búsqueda por usuario.
2. **Flota:** planes de mantenimiento (alta/edición, CU-105/140) y listado y
   ficha de tareas: hoy el panel crea, edita y cierra tareas pero no las lista.
3. **Pedidos:** cancelación forzada (`DELETE`), pool de disponibles (CU-080),
   alta telefónica (CU-072).
4. **Clientes:** edición (CU-131), ubicación (CU-094), dirección predeterminada.
5. **Plataforma:** CRUD de roles (CU-089), reenvío de confirmación (CU-101),
   recuperar contraseña desde el login (CU-047), cambio de email.

---

## 2. Inventario de Minimal (`vite-ts/src`)

### 2.1 Layouts

| Ruta | Qué hace | Para SPLG |
|---|---|---|
| `layouts/dashboard/` (`layout.tsx`, `nav-vertical`, `nav-horizontal`, `nav-mobile`, `content`) | Shell con nav vertical colapsable a "mini", horizontal o drawer móvil; header con slots | **Shell del panel.** `navColor: 'apparent'` da el menú oscuro que pide Brasa |
| `layouts/nav-config-dashboard.tsx` | Menú por secciones (`subheader` + items con hijos, `caption`, `info`, roles) | Nav por subsistema (Operación, Flota, Clientes, Catálogo, Posventa, Plataforma) |
| `layouts/components/workspaces-popover.tsx` | Selector de "workspace" en el header (hoy `_workspaces` fijo) | **Selector de distribuidora** del super admin (`X-Distributor`) |
| `layouts/components/notifications-drawer/` | Cajón con pestañas leídas/no leídas (hoy `_notifications`) | Campana con los eventos de socket `order:*` |
| `layouts/components/account-drawer.tsx`, `account-popover`, `sign-out-button` | Menú de cuenta (hoy `useMockedUser`) | Perfil, cerrar sesión |
| `layouts/components/searchbar/` | Búsqueda ⌘K sobre el menú | Saltar a pantallas; luego buscar pedido por id |
| `layouts/components/settings-button`, `components/settings/` | Drawer de modo/colores/fuente/layout | Dejar sólo modo claro/oscuro (si se hace oscuro) y nav mini; sacar presets |
| `contacts-popover`, `language-popover`, `nav-upgrade`, `menu-button` | Contactos, idiomas, banner "upgrade" | No |
| `layouts/auth-split`, `auth-centered` | Login a dos columnas / centrado | Login del panel |
| `layouts/simple`, `layouts/main` | Páginas sueltas / sitio público | `simple` para 403/404/500; `main` no |

### 2.2 Secciones

| Sección | Qué trae | Pantalla SPLG |
|---|---|---|
| `overview/e-commerce` | Widgets de KPI con variación, ventas anuales, mejor vendedor, últimos productos | **Tablero**: KPIs de `stats/summary`, ventas por chofer/producto |
| `overview/analytics` | KPIs, visitas (área), conversión (barras), **order-timeline**, tareas | Tablero: gráfico 7 días (`stats/chart`), últimos pedidos en línea de tiempo |
| `overview/booking` | Disponibles/reservados (radial), check-in, estadísticas | Widget de **reservas** y franjas ocupadas |
| `overview/app`, `banking`, `course`, `file` | KPIs genéricos, saldo, gastos por categoría, almacenamiento | `banking-balance-statistics` → saldo de choferes (opcional); el resto no |
| `order/` (`order-list-view`, `order-details-*`, `order-table-*`) | Lista con pestañas por estado y contadores, filtros con chips; ficha con cliente, entrega, ítems, pago, **historial** | **Pedidos** (lista y ficha). Es la sección más aprovechable |
| `user/` (`user-list-view`, `user-cards-view`, `user-profile-view`, `user-create-edit-form`, `user-quick-edit-form`) | ABM de usuarios con pestañas por estado, edición rápida en modal, perfil con portada y pestañas | **Choferes** (cola de validación), **Clientes**, **Administradores**, **Usuarios**; perfil → ficha de chofer |
| `product/` (`product-list-view` con DataGrid, `product-details-*`, `product-create-edit-form`) | Catálogo con DataGrid + toolbar, ficha, alta/edición | **Catálogo y stock** (garrafas, precio, stock, promociones) |
| `invoice/` (`invoice-list-view`, `invoice-details`, `invoice-pdf`) | Lista con análisis por estado, detalle, PDF con `@react-pdf/renderer` | Remito/comprobante del pedido en PDF (nuevo, opcional); `invoice-analytic` para tarjetas de resumen |
| `file-manager/` | Grilla/tabla de archivos, detalle, subir, compartir | **Documentación de flota** (adjuntos de tareas, licencias, VTV, seguro) |
| `calendar/` (FullCalendar daygrid/timegrid/list) | Calendario con eventos, filtros, formulario | **Franjas y reservas** en calendario |
| `kanban/` (dnd-kit) | Tablero por columnas con detalle y adjuntos | **Tareas de flota** por estado (`forecast`…`done`) — ver §7 |
| `address/` | Alta de dirección, ítem, diálogo de lista | **Direcciones del cliente** |
| `account/` (`account-general`, `account-change-password`, `account-notifications`) | Cuenta con pestañas | **Perfil** del admin |
| `permission/view.tsx` + `auth/guard/role-based-guard.tsx` | Demo de vista por rol | Rutas sólo super admin |
| `error/` (403, 404, 500), `maintenance`, `coming-soon` | Páginas de error | 403/404/500; `maintenance` para cuando `/health` cae |
| `tour/`, `job/` | Listados en tarjetas con filtros, fichas con "bookers"/"candidates" | Idea para **distribuidoras** en tarjetas; no más |
| `chat/`, `mail/` | Mensajería | No: la API no tiene mensajería |
| `blog`, `checkout`, `payment`, `pricing`, `home`, `about`, `contact`, `faqs`, `blank` | Sitio público y e-commerce | No (la landing es `splg-landing`) |
| `_examples/` | Demos de todos los componentes (incluye `extra/map-view` con clusters, heatmap, marcadores) | Referencia; no se copia |

### 2.3 Componentes (`components/*`)

| Componente | Qué hace | Uso en SPLG |
|---|---|---|
| `hook-form` (`Form`, `Field.*`, `schema-helper.ts`) | rhf + zod con campos MUI (texto, select, autocomplete, fecha, número, teléfono, switch, upload…) | **Todos los formularios** |
| `table` (`use-table`, `TableHeadCustom`, `TablePaginationCustom`, `TableSelectedAction`, `TableNoData`, `TableSkeleton`) | Tabla MUI con orden, selección y paginación (en cliente) | Listados con pestañas; adaptar a paginación del servidor |
| `custom-data-grid` | Toolbar y acciones para DataGrid 8 | Auditoría, reportes, catálogo |
| `filters-result` | Chips de filtros activos con "limpiar" | Todos los listados |
| `label` | Chip de estado con color suave | **Estados** de pedido, envase, reclamo, tarea |
| `chart` (ApexCharts) | Wrapper con tema | Tablero y reportes (ver §3.3) |
| `map` (react-map-gl + Mapbox) | Mapa, marcadores, popups, controles | Ver §3.3: no se adopta |
| `upload`, `file-thumbnail`, `lightbox` | Dropzone, miniaturas por tipo, visor | Adjuntos de flota y documentos de chofer |
| `custom-date-range-picker` | Rango de fechas propio (sin X Pro) | Filtros de reportes, pedidos y auditoría |
| `custom-dialog` (`ConfirmDialog`) | Confirmación | Reemplaza `sweetalert2` |
| `custom-popover` | Menú contextual | Acciones por fila |
| `custom-breadcrumbs` | Migas + acciones | Encabezado de cada pantalla (reemplaza `PageHeader`) |
| `empty-content`, `search-not-found` | Estados vacíos | Kit |
| `snackbar` (sonner) | Toasts | Reemplaza `notistack` |
| `nav-section` | Menú vertical/mini/horizontal | Shell |
| `iconify` | Íconos **offline** (sólo los registrados en `icon-sets.ts`, 702 líneas) | Reemplaza `lucide-react`; cada ícono nuevo se registra |
| `number-input`, `phone-input` | Número con +/-, teléfono internacional | Stock, precio, capacidad; teléfonos |
| `scrollbar`, `progress-bar`, `loading-screen`, `logo`, `svg-color`, `image`, `animate` | Utilidades de UI | Shell |
| `organizational-chart` | Organigrama | Opcional: distribuidora → administradores |
| `editor` (tiptap), `markdown`, `carousel`, `mega-menu`, `nav-basic`, `country-select`, `flag-icon` | — | No |

---

## 3. Arquitectura propuesta

### 3.1 Qué se conserva del panel actual

- **Datos:** `src/services/api/*` (una función por endpoint), `schema.d.ts`/`types.ts`
  generados con `npm run api:types`, `httpClient.ts` (Bearer de Firebase,
  `X-Distributor`, `toPage` con `X-Total-Count`, `Idempotency-Key`), `errors.ts`
  y `services/queries/*` (React Query 5 con `queryKeys`). Se copian tal cual con
  sus tests.
- **Formularios:** zod + rhf; los esquemas de `common/forms/` pasan a usarse con
  `Form`/`Field.*` de Minimal (mismo rhf; `@hookform/resolvers` 3 → 5).
- **Tiempo real:** `context/SocketContext`, `hooks/useSocket.ts` (eventos
  `order:*` y `order:driver-location` del `AdminGateway`).
- **Reglas:** `CONVENCIONES.md` (código en inglés, UI en castellano, sin `any`,
  páginas sólo con hooks). Cambia la §6 (paleta): de Tailwind a tokens del tema.

### 3.2 Qué de Minimal no se usa

| Pieza | Por qué | Reemplazo |
|---|---|---|
| `swr` + `src/actions/*` + `lib/axios.ts` (`endpoints`, `fetcher`) | Segunda capa de datos contra el mock server de Minimal | React Query + servicios tipados |
| `src/_mock/*` (los `*-list-view` arrancan de `useState(_orders)`, `_userList`…) | Datos falsos y filtrado en cliente | Hooks de `services/queries` con paginación y filtros en la API |
| `src/auth/*` de ejemplo (jwt, auth0, amplify, supabase, `useMockedUser`) | SPLG entra con Firebase y resuelve el rol en la API | Un `AuthProvider` propio (Firebase + `GET /users/email/:email`) con los guards de Minimal (`auth-guard`, `guest-guard`, `role-based-guard`) |
| `i18next`/`locales`, RTL, presets de color, fuentes extra | Un idioma, una marca | Fuera |
| `@fullcalendar/timeline` | Plugin **premium** de FullCalendar (licencia aparte) | Sólo `daygrid`/`timegrid`/`list`/`interaction` (MIT) |
| `mapbox-gl`/`react-map-gl` | Ver 3.3 | Leaflet |
| Redux Toolkit, Tailwind, notistack, sweetalert2, lucide-react (del panel actual) | Duplican lo que trae Minimal | Contexto de auth, `sx`/tema, sonner, `ConfirmDialog`, iconify |

Arrancar desde **`starter-vite-ts`** (mismo shell y tema, sin secciones ni la
mayoría de las dependencias) y copiar de `vite-ts` sólo las secciones y
componentes que se usan. El README de Minimal lo dice así: *"Good to start a new
project. You can copy components from the full version."*

### 3.3 Gráficos y mapas

**Gráficos — recomendación: ApexCharts (el `components/chart` de Minimal).**
Todos los widgets de `overview/*` e `invoice-analytic` vienen armados con él y
toman el tema; seguir con Recharts obliga a rehacer cada widget.
Contra: más peso (carga diferida, como ya hace `chart.tsx`) y hay que reescribir
los 2 gráficos actuales (`pages/Home`, `pages/Reports`). Recharts 3 funciona con
React 19, así que no es obligatorio cambiar.

**Mapas — recomendación: quedarse con Leaflet** (`react-leaflet` 5, que pide
React 19, + `@geoman-io/leaflet-geoman-free` 2.20 para dibujar polígonos).

| | Leaflet + Geoman (hoy) | Mapbox (Minimal) |
|---|---|---|
| Costo / cuenta | Sin token (tiles OSM; para producción, un proveedor de tiles) | Token y cuenta Mapbox; facturación por cargas de mapa |
| Zonas de cobertura | Dibujo/edición de polígonos andando (`pages/CoverageZones`, 1 110 líneas) | Hay que sumar `mapbox-gl-draw` y rehacer la edición |
| Despacho en vivo | Marcadores por chofer andando (`pages/Tracking`) | Mejor rendimiento (WebGL), clusters y heatmap ya en `_examples/extra/map-view` |
| Riesgo para la defensa | Bajo | Medio (token, cuota, red en el aula) |

Si más adelante hace falta clusters o heatmap, MapLibre GL (fork libre de Mapbox,
mismo API que `react-map-gl/maplibre`) los da sin token.

### 3.4 Tema: Brasa sobre Minimal

Se edita `src/theme/theme-config.ts` (paleta, fuentes) y se fija
`defaultSettings` en `components/settings/settings-config.ts`.

| Minimal (`themeConfig.palette`) | Brasa (`src/theme/brand.json`) |
|---|---|
| `primary` lighter/light/main/dark/darker | `llama` 100 / 400 / **500 #F26B1D** / 700 #B8430B / 900 · contrastText blanco |
| `secondary` | `gas` 100 / 300 / **400 #FFB020** / 600 / 800 · contrastText `tinta-900` |
| `info` / `success` / `warning` / `error` `.main` | `status.info` #175CD3 / `success` #067647 / `warn` #B54708 / `danger` #B42318 |
| mismos `.lighter` | `statusSoft.*` (#EFF8FF, #ECFDF3, #FFFAEB, #FEF3F2) |
| `grey` 50…900 | `tinta` 25/50/100/200/300/400/500/600/800/900 |
| `background.default` / `paper` | `canvas` #F5F6F8 / #FFFFFF |
| nav (`navColor: 'apparent'`, `layouts/dashboard/css-vars.ts`) | `sidebar.bg` #0B0F16, `raised` #121824, `line`, `text` #98A2B3 |
| `MuiButton` `containedPrimary` (override en `theme/core/components`) | degradé `primaryGradient` #D24E0D → #B23F0A, borde #A13A09 |
| `fontFamily.primary` / `secondary` | Geist / Geist Mono (montos), según `MARCA.md` |

Defaults: `mode: 'light'`, `navColor: 'apparent'`, `primaryColor: 'default'`,
`compactLayout: true`; el drawer de ajustes se saca o se deja sólo con modo y nav.
El script `npm run colors` se adapta para rechazar hex fuera de `theme/`.
Los colores de estado de pedido (`utils/statusLabels`) se mapean a las variantes
de `Label`.

### 3.5 Estrategia de migración — recomendación

**Proyecto nuevo sobre Minimal, dentro del mismo repo** (`splg-app-admin`, remoto
`Nahuelito-Dev/splg-front-web`), en una rama `refactor/panel-minimal` desde
`develop`: se reemplaza el andamiaje por `starter-vite-ts` y se portan servicios,
hooks y pantallas por fases. El panel viejo sigue en `develop` (y desplegado)
hasta que la rama tenga paridad; se integra con squash.

Por qué no actualizar el actual: el salto es React 18→19, MUI 5→7, DataGrid
6→8, react-router 6→7, Vite 4→6, ESLint 8→9 y sacar Tailwind de 22 páginas; se
reescribe todo igual y además se arrastra el layout propio, que es lo que se
quiere cambiar. Por qué el mismo repo: conserva Netlify/Firebase hosting, el
versionado y release por repo, `CONVENCIONES.md` y la historia.

---

## 4. Mapa de pantallas objetivo

Rutas: se mantienen las de hoy (`src/routes/DashboardRoutes.tsx`) para no romper
enlaces; **N** = pantalla o capacidad nueva. SA = sólo super admin.

| Pantalla | Ruta | Minimal | Endpoints | CU |
|---|---|---|---|---|
| Login + recuperar contraseña | `/login` | `layouts/auth-split`, `auth/view/firebase` (forma) | Firebase, `GET /users/email/{email}`, **N** `POST /email/password-reset` | 001, 047, 091 |
| Tablero | `/home` | `overview/e-commerce`, `overview/analytics`, `chart` | `GET /orders/stats/summary`, `/orders/stats/chart`, `/reports/*`, `/fleet/expirations`, `/claims`, `/incidents` | 026, 030 |
| Pedidos (lista) | `/orders` | `order/order-list-view` (pestañas por estado, chips), `table` | `GET /orders` | 011 |
| Pedido (ficha) | `/orders/:id` | `order/order-details-*` (historial, cliente, entrega, pago), `ConfirmDialog` | `GET /orders/{id}`, `PATCH …/assign/{deliveryId}`, `…/cancel`, `…/status`, `…/arrived`, `GET …/delivery-code`, `POST …/confirm-delivery`, **N** `DELETE /orders/{id}`, `GET /incidents/order/{id}`, `POST /cylinders/assign` | 006, 010, 012, 068, 078, 079 |
| Alta telefónica de pedido/reserva **N** | `/orders/new` | `checkout` (pasos, sólo forma), `hook-form` | **N** `POST /orders`, `GET /coverage-zones/check`, `GET /time-slot/availability`, `GET /gascylinder` | 072 |
| Despacho en vivo | `/tracking` | `overview/analytics` (lista), Leaflet | socket `order:*`, `order:driver-location`, `GET /delivery/active`, **N** `GET /orders/available` | 080, SS-03/04 |
| Reservas | `/reservations` | `calendar` + `table` | `GET /orders/reservations`, `PATCH /orders/{id}/confirm-deposit` | 073, 074 |
| Choferes (lista, cola de validación) | `/deliveries` | `user/user-list-view` (pestañas: por validar / activos / deshabilitados) | `GET /delivery`, `/delivery/active`, `POST /users` | 003, 031, 035 |
| Chofer (ficha) | `/deliveries/details/:id` | `user/user-profile-view` (pestañas), `file-manager`, `lightbox` | `GET /delivery/{id}`, `PATCH /delivery/{id}`, `…/status`, `DELETE`, `GET /delivery/{id}/documents`, `GET /car/user/{userId}`, `GET /ratings/user/{userId}{,/summary}`, **N** `…/validate`, `…/invalidate`, `…/balance`, `PATCH /delivery/user/{userId}/availability`, `GET /orders/delivery/{id}` | 032, 033, 049, 065, 066, 081, 096, 097, 109, 138 |
| Vehículos | `/cars`, `/cars/details/:id` | `product/product-list-view` (DataGrid), ficha con `file-manager` | `GET/POST/PATCH/DELETE /car…`, `GET /cars/{carId}/documents`, **N** `GET /car/patent/{patent}` | 034, 051, 111–115, 136, 137 |
| Flota: vencimientos | `/fleet/expirations` | `table` con pestañas (vigente / por vencer / vencido), `Label` | `GET /fleet/expirations` | 139, 142 |
| Flota: planes **N** | `/fleet/plans` | `table`, `hook-form` | `GET /fleet/plans`, **N** `POST`, `GET/PATCH /fleet/plans/{id}` | 105, 140 |
| Flota: tareas **N** | `/fleet/tasks`, `/fleet/tasks/:id` | `kanban` (columnas por `status`, sin arrastrar) o `table`; `upload`, `file-thumbnail`, `lightbox` | **N** `GET /fleet/tasks`, `GET /fleet/tasks/{id}`, `POST/PATCH …`, `…/close`, `…/cancel`, adjuntos (4) | 141, 155–158 |
| Clientes | `/customers`, `/customers/details/:id` | `user/user-list-view`, `user-profile-view`, `address/*` | `GET /customers{,/id}`, `DELETE`, `GET /orders/customer/{id}`, `/user-address/user/{userId}`, POST/PATCH/DELETE/set-default, **N** `PATCH /customers/{id}`, `…/location`, `GET /customers/user/{userId}`, `GET /user-address/user/{userId}/default` | 092, 094, 095, 129–131 |
| Catálogo y stock | `/cylinders`, `/cylinders/details/:id` | `product/*` (DataGrid, ficha, form), `number-input` | `GET/POST/PATCH/DELETE /gascylinder…`, `PATCH …/stock` | 036–041 |
| Envases y trazabilidad | `/physical-cylinders`, **N** `/physical-cylinders/:id` | `table` + `Label`, `order-details-history` (línea de tiempo) | `GET/POST /cylinders`, `PATCH …/transition`, `GET …/history`, **N** `GET /cylinders/{id}` | 067, 069–071, 132–134 |
| Zonas de cobertura | `/coverage-zones` | Leaflet + Geoman, `hook-form` | `GET/POST/PATCH/DELETE /coverage-zones…`, `GET …/check` | 056–059, 150, 151 |
| Franjas horarias | `/settings` → **N** `/time-slots` | `calendar` (timegrid semanal), `hook-form` | `GET/POST/DELETE /time-slot…`, `GET /time-slot/availability` | 042, 043, 103, 154 |
| Reclamos | `/claims`, **N** `/claims/:id` | `invoice-list-view` (pestañas pending / in_process / resolved / rejected), drawer de detalle | `GET /claims`, `PATCH …/resolve`, **N** alta telefónica `POST /claims` (ya en el servicio) | 024, 025 |
| Incidencias | `/incidents`, **N** `/incidents/:id` | ídem (open / resolved) | `GET /incidents`, `PATCH …/resolve`, `POST /incidents` | 060–063 |
| Calificaciones | `/ratings` | `product-details-review` (forma) | `GET /ratings/user/{userId}{,/summary}` | 065, 066 |
| Reportes | `/reports` | `chart`, `custom-date-range-picker`, DataGrid | `GET /reports/*` (4) | 027–030 |
| Auditoría | `/audit` | DataGrid server-side + filtros | `GET /audit` | 152 |
| Usuarios | `/users`, `/users/details/:id` | `user/*` | `GET /users`, `/users/{id}`, `PATCH`, `…/block`, `DELETE`, **N** `GET /users/phone/{p}`, `POST /users/check-exists`, `POST /email/change-email` | 050, 083–085 |
| Administradores | `/admins` | `user/user-list-view`, `user-quick-edit-form` | `GET /admin`, `POST /users`, **N** `GET /admin/term/{term}` | 086, 088 |
| Distribuidoras (SA) | `/distributors`, **N** `/distributors/:id` | `tour`/`job` (tarjetas) o `table`, ficha con admins | `GET/POST/PATCH/DELETE /distributor…`, `GET /distributor/current` | 052–055 |
| Sistema (SA) | `/system` | `overview/app` (widgets), `maintenance` | `GET /health`, `/health/ready`, `POST /email/test`, `/notifications/send-test`, `GET /notifications/user/{id}`, **N** `POST /notifications/order-confirmation` | 099–102, 104 |
| Roles (SA) | `/system/roles` **N** | `table`, `hook-form` | `GET /role`, `POST /role/seed`, **N** `POST`, `GET/PATCH/DELETE /role/{id}` | 089, 090 |
| Notificaciones | cajón del header | `notifications-drawer` | socket `order:*` | SS-17 |
| Perfil **N** | `/account` | `account/account-general`, `account-change-password` | `GET/PATCH /users/{id}`, `POST /email/password-reset` | 004 (admin) |
| Selector de distribuidora | header | `workspaces-popover` | `GET /distributor`, `X-Distributor` | SS-10 |

---

## 5. Plan por fases

Estimación en puntos relativos (1 = la pantalla más chica). Cada fase cierra con
la DoD del repo: `npm run verify` verde corrido por quien integra, recorrido en
Chrome contra la API real (`splg-dev.sh` + `npm run seed:demo`) con la paleta
Brasa, revisión cruzada del diff, y sin commitear sin el ok de nahue.

| Fase | Contenido | Puntos | Depende de | Criterio de aceptación |
|---|---|---:|---|---|
| **F0 Base** | `starter-vite-ts` en la rama; tema Brasa (§3.4) y Geist; nav por secciones con roles; `AuthProvider` Firebase + guards; selector de distribuidora; copiar `services/api`, `services/queries`, `httpClient`, socket, tests; ESLint 9/Prettier de Minimal + reglas de `CONVENCIONES.md`; `verify` y `colors` adaptados; 403/404/500 | 8 | — | Login/logout de admin y super admin; un admin no ve rutas SA ni entra por URL; cambiar de distribuidora recarga los datos; los 30 tests portados pasan; ni un `_mock`, `swr` ni `useMockedUser` en `src` (grep) |
| **F1 Operación** (lo que se muestra en la defensa) | Tablero; pedidos lista + ficha con todas las acciones (incluye `DELETE` forzado, código de entrega, confirmar, llegó, asignar envases); despacho en vivo con pool de disponibles; reservas en calendario | 13 | F0 | Circuito completo desde el panel: pedido nuevo (app o seed) → aparece por socket → asignar → en camino → entregar con código; cancelar y forzar cancelación restituyen stock (verificado en la API); reserva → confirmar seña |
| **F2 Choferes y flota** | Cola de validación; ficha de chofer con validar/invalidar, habilitar, ON/OFF, saldo, historial, calificaciones, documentos y vehículos; vehículos; vencimientos; planes (**nuevo**); tareas lista/kanban + adjuntos | 13 | F0 | Alta de chofer → validar → habilitar → ON → recibe un pedido; planes ABM; tarea creada → adjunto subido/visto/borrado → cerrada; vencimiento bloqueante inhabilita al chofer/vehículo según la API |
| **F3 Clientes, catálogo, envases, zonas, franjas** | Clientes con edición, ubicación y direcciones; catálogo/stock/promos; envases con ficha e historial; zonas en Leaflet; franjas en calendario | 12 | F0 | Editar cliente y su predeterminada se refleja en `GET`; stock y precio cambian y el pedido nuevo los toma; envase recorre `in_depot → … → empty_returned` con historial; zona dibujada valida una dirección con `check` |
| **F4 Posventa** | Reclamos e incidencias con pestañas, detalle y alta telefónica; calificaciones | 5 | F1 | Reclamo cargado por teléfono → resuelto; incidencia desde la ficha del pedido → resuelta; contadores por estado coinciden con la API |
| **F5 Plataforma (SA)** | Distribuidoras con ficha y baja; administradores; usuarios (bloqueo, baja, búsqueda); roles CRUD; sistema (salud, pruebas, reenvío de confirmación); auditoría con filtros | 8 | F0 | Alta de distribuidora → su admin → entra y sólo ve lo suyo; baja de distribuidora; cada escritura de las fases anteriores aparece en auditoría |
| **F6 Cierre** | Perfil y cambio de contraseña/email; campana; ⌘K; responsive 360 px; accesibilidad (contraste del tema medido como en `MARCA.md`); borrar el panel viejo | 5 | F1–F5 | Cobertura de endpoints ≥ 134/148 (script de §1 re-corrido); recorrido por rol del guion de demo sin errores de consola; squash a `develop` con ok de nahue |

Orden sugerido si el tiempo aprieta: F0 → F1 → F2 (choferes primero, flota después)
→ F4 → F3 → F5 → F6. F1 y F2 son lo que diferencia SPLG en la defensa
(despacho, trazabilidad, flota); F3 hoy ya funciona en el panel viejo.

---

## 6. Licencia

**Qué hay en el disco.** `~/Desktop/templates/Minimal_TypeScript_v7.3.0/` no tiene
LICENSE; está dentro de los zip (`Minimal_TypeScript_v7.3.0-e22mzp.zip`,
`Minimal_TypeScript_v7.3.0/LICENSE.md`) y sólo remite a la web:

> "You can find more details about the license at: https://docs.minimals.cc/package · https://mui.com/store/license/"

El FAQ de la propia plantilla (`vite-ts/src/sections/home/home-faqs.tsx`) dice:

> "All licenses do not apply to open source." · "One licenses / one end product (3 licenses / 3 products...)." · "**Standard / Plus** license used in free products (Internal management...)." · "**Extended** license used in charge products, collect fees from users (SAAS...)." · "The license is lifetime." · "The Standard license is designed for internal applications in which staff will access the application. An example could be the back-office dashboard of a public-facing e-commerce website…"

**Términos de MUI Store** (https://mui.com/store/license/, leído el 01/10/2026):
la Standard permite usar el contenido en un *End Product* gratuito; la Extended,
en uno que se cobra ("a SaaS web service with a monthly subscription fee"). Ambas
prohíben "Re-distribute the Content's source (other than as permitted herein),
even if the Content is modified" y "Allow the End User of the End Product to
access the Content's source".

**Qué se puede afirmar:**

- Que esté la versión TypeScript indica Plus o Extended (según
  docs.minimals.cc/package, la Standard sólo trae JavaScript). **No hay recibo
  ni dato de quién la compró ni cuál.**
- Uso en un proyecto propio/tesis, gratuito, como panel interno: cubierto por
  Plus/Standard **si la licencia es de nahue y no se gastó en otro producto**.
  Ojo: `tutu_admin` (gearthlogic) es un fork de Minimal; si la licencia es de
  gearthlogic y se usó para Tutu, SPLG es un segundo *end product* y necesita
  la suya.
- Repo privado: el texto no prohíbe guardar el código en un repo privado propio;
  prohíbe redistribuir el fuente. `splg-front-web` devuelve 404 sin sesión
  (privado). **No** puede quedar público, ni publicarse el fuente del panel en
  el sitio de docs, ni entregarse a la cátedra como código abierto sin consultar.
- Si SPLG se vende a distribuidoras (SaaS), hace falta **Extended**.

---

## 7. Riesgos y decisiones abiertas para nahue

**Decisiones:**

1. **Licencia:** ¿de quién es y cuál (Plus/Extended)? ¿La cátedra pide el
   código fuente del panel? Si la respuesta complica, el plan B es el mismo
   diseño con MUI 7 sin Minimal (más trabajo en F0).
2. **Login del panel:** hoy es Firebase directo + `GET /users/email`; existe
   `POST /auth/login/dashboard` (setea cookie y restringe a administradores) sin
   usar. Elegir uno y documentarlo.
3. **Gráficos:** ApexCharts (reusar widgets) o Recharts (lo que hay).
4. **Modo oscuro:** Brasa sólo define modo claro con menú oscuro. ¿Se diseña la
   variante oscura o se fija `light`?
5. **"Vehículo en uso":** la API no lo modela. `CarResponseDto` tiene `user_id`
   (dueño), no hay campo de vehículo activo. Si se quiere en la ficha del
   chofer, es un cambio de back.
6. **Reclamos:** tienen 4 estados (`pending`, `in_process`, `resolved`,
   `rejected`) pero el único cambio de estado es `PATCH /claims/{id}/resolve`.
   Kanban o "tomar el reclamo" necesitan endpoint nuevo; si no, pestañas.
7. **Kanban de tareas de flota:** los estados (`forecast`, `scheduled`,
   `in_progress`, `done`, `overdue`, `cancelled`) los cambian `PATCH`, `close`
   y `cancel`; arrastrar entre columnas no tiene equivalente uno a uno. Propuesta:
   kanban de lectura + acciones en la tarjeta.
8. **`POST /admin`** (alta "basic") duplica `POST /users`: ¿se depreca en el back?
9. **Rutas:** mantener las actuales (`/deliveries/details/:id`) o normalizarlas
   (`/drivers/:id`); cambiarlas rompe enlaces de notificaciones.

**Riesgos:**

- **Trabajo en vuelo:** el panel tiene 27 archivos sin commitear en
  `feat/panel-flota-documentacion`. Cerrarlo o archivarlo antes de abrir la rama
  nueva, o se porta código que no está en `develop`.
- **Tiempo vs. defensa:** el panel viejo funciona y cubre 102 endpoints. Una
  migración a medias el día de la defensa es peor que el panel actual: no se
  integra hasta tener F0+F1+F2 con paridad, y el viejo queda desplegado.
- **Inconsistencia en el contrato:** `OrderResponseDto.status` usa
  `out_for_delivery` y `OrderRecordResponseDto.status` usa `on_the_way` (el
  servicio `orders.ts` ya lo advierte). Conviene arreglarlo en el back antes de
  mapear estados a `Label`.
- **Saltos de versión:** `@hookform/resolvers` 3→5, `zod` 3 (Minimal también 3:
  sin salto), react-router 7 (`react-router` en vez de `react-router-dom`),
  `react-leaflet` 4→5, ESLint 9 flat config. Los tests con Testing Library 14
  pasan a 16.
- **Peso de Minimal:** `minimal-shared` aparece en 382 archivos de `vite-ts`;
  partir de `starter-vite-ts` y copiar a mano evita arrastrar dependencias
  (auth0, amplify, supabase, tiptap, mapbox) que después hay que limpiar.
- **Íconos offline:** iconify sólo pinta lo registrado en
  `components/iconify/icon-sets.ts`; cada ícono nuevo hay que agregarlo.
- **`COBERTURA-PANEL.md` quedó viejo** (131/64 del 26/09 contra 148/102 hoy);
  reemplazarlo por la §1 de este archivo o regenerarlo con el mismo script.
