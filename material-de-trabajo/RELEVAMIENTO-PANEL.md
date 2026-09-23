# Relevamiento factual — `splg-app-admin`

Repo: `/Users/nahuelwagner/Desktop/myprojects/gearthlogic/projects/garrafitas/splg-app-admin`
Fecha del relevamiento: 2026-09-23
Stack declarado en `package.json`: React 18.2, TypeScript 5.0, Vite 4.4, `@tanstack/react-query` ^4.35.3, `@reduxjs/toolkit` ^2.2.3, `react-redux` ^9.1.1, `@mui/material` ^5.14, `@mui/x-data-grid` ^6.16, `react-hook-form` ^7.71, `sweetalert2` ^11.26, `socket.io-client` ^4.8.1, `leaflet`/`react-leaflet`, `recharts` ^3.7, `chart.js` ^4.4 + `react-chartjs-2`, `tailwindcss` ^3.4, `firebase` ^10.4, `axios` ^1.13.

**Conteo real de archivos:** 163 archivos bajo `src/` (162 `.ts`/`.tsx` + `src/styles/index.scss`). Total de líneas en `.ts`/`.tsx`: **13.284**.

Nota metodológica: todos los números salen de grep/find/AST-lite sobre el árbol `src/`. Los ficheros se abrieron para confirmar cada dato citado. **No se modificó ningún archivo del repositorio.**

---

## TABLA 1 — Pantallas (una fila por `<Route>` de `src/routes/DashboardRoutes.tsx`)

`src/routes/DashboardRoutes.tsx` tiene 96 líneas y declara **23 rutas** (22 de pantalla + 1 catch-all `Navigate`).

| ruta | componente | archivo | líneas | ¿llamadas a la API? | ¿form alta/edición? | ¿tabla/listado? | ¿completa o esqueleto? |
|---|---|---|---|---|---|---|---|
| `home` (`DashboardRoutes.tsx:48`) | `Home` | `src/pages/Home/Home.tsx` | 52 | No directas; delega en 4 vistas (`SalesStats.tsx:12`, `DashboardStats.tsx:16,23,29,35`, `RecentOrdersWidget.tsx:40`, `FleetStatus.tsx:19`) | No | Sí, indirecto (`RecentOrdersWidget.tsx` tiene `<table>`) | Completa (composición de 4 widgets con datos reales) |
| `users` (`:51`) | `Leads` | `src/pages/Leads/Leads.tsx` | 247 | Sí — `deleteUser`, `createUser`, `updateUser`, `blockUser` (`Leads.tsx:2`) | Sí — `UserModal.tsx:68` (`<form>` + react-hook-form) | Sí — `LeadsTable.tsx` usa `CustomTable` | Completa |
| `users/details/:leadId` (`:52`) | `LeadsDetailsView` | `src/pages/Leads/components/LeadsDetailsView.tsx` | 274 | Sí — `getUserById` (`:3`, llamada en `:47`) | No | No (fichas de detalle) | **Parcial**: `handleToggleBlock` (`:60-72`) no hace nada, sólo `console.log('Toggle block clicked (Lógica pendiente)')` en `:71`, con el código real comentado en `:66-70` |
| `customers` (`:55`) | `Customers` | `src/pages/Customers/Customers.tsx` | 170 | Sí — `createCustomer`/`updateCustomer`/`deleteCustomer` (`:3-7`) + `resetUserPassword` (`:8`) | Sí — `CustomerModal.tsx:98` | Sí — `CustomersTable.tsx` (`CustomTable`) | Completa |
| `customers/details/:id` (`:56`) | `CustomerDetails` | `src/pages/Customers/components/CustomerDetails.tsx` | 269 | Sí — `getCustomerById` (`:63`), `getOrdersByCustomer` (`:69`) | No | Sí — `<table>` en `:222` | Completa |
| `cylinders` (`:59`) | `Cylinders` | `src/pages/Gascilinders/Cylinders.tsx` | 239 | Sí — `services/api/cylinders` (`:4-9`) | Sí — `CylinderModal.tsx:104` | Sí — `CylindersTable.tsx` (`CustomTable`) | Completa |
| `cylinders/details/:id` (`:60`) | `CylinderDetails` | `src/pages/Gascilinders/components/CylinderDetails.tsx` | 266 | Sí — **axios directo** `privateAxiosInstance.get('/gascylinder/:id')` (`:3`, `:31`) + `updateCylinder` (`:6`) | Sí — reusa `CylinderModal` | No | Completa |
| `envases` (`:63`) | `Envases` | `src/pages/Envases/Envases.tsx` | 247 | Sí — `services/api/physicalCylinders` (`:8-14`) | Sí — `CreateEnvaseModal.tsx:73`, `TransitionModal.tsx` | Sí — `<table>` en `:155` | Completa |
| `deliveries` (`:66`) | `Deliveries` | `src/pages/Deilverys/Deliveries.tsx` | 159 | Sí — `createDelivery`/`updateDelivery`/`deleteDelivery` (`:4-8`) + `resetUserPassword` (`:9`) | Sí — `DeliveryModal.tsx:110` | Sí — `DeliveriesTable.tsx` (`CustomTable`) | Completa |
| `deliveries/details/:id` (`:67`) | `DeliveryDetails` | `src/pages/Deilverys/components/DeliveryDetails.tsx` | 225 | Sí — `services/api/deliveries` (`:3-6`) | No propio; embebe `CarsManager` (que sí abre `CarModal`) | Sí, vía `CarsManager.tsx` | Completa |
| `cars` (`:70`) | `Cars` | `src/pages/Cars/Cars.tsx` | 130 | Sí — `createCar`/`updateCar`/`deleteCar` (`:4`) | Sí — reusa `CarModal` de `Deilverys` (`Cars.tsx:3`) | Sí — `CarsTable.tsx` (`CustomTable`) | Completa |
| `configuracion` (`:71`) | `Configuration` | `src/pages/Configuration/Configuration.tsx` | 27 | **No** (0 imports de `services/api`) | No propio | No propio | **Esqueleto por criterio de líneas (<50)**: sólo renderiza título + `<TimeSlotsManager />` (`:20`) y un comentario `Aquí puedes agregar más tarjetas de configuración en el futuro` (`:22`). La funcionalidad real vive en `Configuration/components/TimeSlotsManager.tsx` (257 líneas, completa) |
| `ordenes` (`:74`) | `Orders` | `src/pages/Orders/Orders.tsx` | 157 | Sí — `assignDriverToOrder`, `cancelOrder` (`:6-10`) | No (Swal con input para motivo de cancelación, `:91`) | Sí — `OrdersTable.tsx` (`CustomTable`) | Completa. El comentario del router dice `{/* 7. Ordenes (Pendiente) */}` (`DashboardRoutes.tsx:73`) pero la pantalla está implementada |
| `tracking` (`:77`) | `Tracking` | `src/pages/Tracking/Tracking.tsx` | 94 | **No REST** (0 imports de `services/api`); consume socket `order:driver-location` (`:11`, `:40`) | No | Sí — `TrackingList.tsx` (109 líneas) + `TrackingMap.tsx` | Completa |
| `claims` (`:79`) | `Claims` | `src/pages/Claims/Claims.tsx` | 194 | Sí — `getAllClaims`, `resolveClaim` (`:3`) | Sí — `ResolveClaimModal.tsx:114` | Sí — `<table>` en `:126` | Completa |
| `incidents` (`:80`) | `Incidents` | `src/pages/Incidents/Incidents.tsx` | 194 | Sí — `services/api/incidents` (`:3-8`) | Sí — `ResolveIncidentModal.tsx:71` | Sí — `<table>` en `:120` | Completa |
| `coverage-zones` (`:81`) | `CoverageZones` | `src/pages/CoverageZones/CoverageZones.tsx` | 342 | Sí — `services/api/coverageZones` (`:3-9`) | Sí — inputs sueltos `:242`, `:253` + dibujo de polígono sobre Leaflet | Sí — listado de zonas | Completa |
| `reservations` (`:82`) | `Reservations` | `src/pages/Reservations/Reservations.tsx` | 211 | Sí — `getReservations`, `confirmDeposit` (`:2-6`) | No | Sí — `<table>` en `:121` | Completa |
| `reports` (`:83`) | `Reports` | `src/pages/Reports/Reports.tsx` | 418 | Sí — 4 `useQuery` (`:53`, `:58`, `:63`, `:69`) contra `services/api/reports` | No (sólo filtros de fecha, `:168`, `:177`) | Sí — `<table>` en `:391` + gráficos Recharts | Completa (incluye export CSV, `:143`) |
| `ratings` (`:84`) | `Ratings` | `src/pages/Ratings/Ratings.tsx` | 319 | Sí — `getAllDeliveries` (`:53`), `getAllCustomers` (`:59`), `getRatingSummary` (`:70`), `getRatingsForUser` (`:76`) | No (sólo buscador, `:148`) | Sí — listado de perfiles + historial | Completa |
| `distributors` (`:87`) | `Distributors` | `src/pages/Distributors/Distributors.tsx` | 196 | Sí — `getAllDistributors`, `createDistributor`, `updateDistributor` (`:3-8`) | Sí — 6 `<input>` controlados (`:93`–`:123`), sin `<form>` | Sí — `<table>` en `:149` | Completa. `deleteDistributor` existe en el servicio (`distributors.ts:39`) pero la pantalla no lo usa |
| `admins` (`:89`) | `Admins` | `src/pages/Admins/Admins.tsx` | 148 | Sí — `getAdmins` (`:16`), `registerAdmin` (`:19`) | Sí — `CreateAdminModal.tsx:69` | Sí — `<table>` en `:96` | Completa (sólo alta + listado; no hay editar/borrar) |
| `/*` → `Navigate to="/home"` (`:92`) | — | — | — | — | — | — | Redirección |

**Ruta de auth** (fuera de `DashboardRoutes`): `src/routes/AuthRoutes.tsx` (11 líneas) → `login` y `*` apuntan ambos a `LoginPage` (`src/pages/Auth/LoginPage.tsx`, 141 líneas, formulario nativo en `:32`).

### Resumen Tabla 1
- Rutas de pantalla: **22** (+1 catch-all).
- Pantallas que cumplen el criterio objetivo de esqueleto (<50 líneas / sólo título / TODO sin implementar): **2** → `Configuration.tsx` (27 líneas, sólo cabecera + un hijo) y `LeadsDetailsView.tsx` (acción de bloqueo comentada + `console.log`, `:66-71`).
- Pantallas sin ninguna llamada REST: `Home.tsx` (delega), `Configuration.tsx`, `Tracking.tsx` (sólo socket).

---

## TABLA 2 — Manejo de estado

| mecanismo | archivos que lo usan | para qué |
|---|---|---|
| **Redux Toolkit — `authSlice`** | `src/store/auth/authSlice.ts` (54), `src/store/store.ts:7`, `src/store/auth/thunks.ts`, `src/hooks/useCheckAuth.ts:6,10`, `src/router/Navigation.tsx:10`, `src/routes/DashboardRoutes.tsx:4,39`, `src/context/SocketContext.tsx:23`, `src/common/components/sidemenu/SideMenu.tsx:69`, `src/pages/Auth/LoginPage.tsx:14`, `src/pages/Admins/Admins.tsx:12`, `src/pages/Deilverys/Deliveries.tsx:18`, `src/services/api/axiosConfig.ts:3,59` | Sesión: `status`, `uid`, `email`, `role`, `fullName`, `errorMessage`. Decide el árbol de rutas y el rol para gating de super_admin |
| **Redux Toolkit — `uiSlice`** | `src/store/ui/uiSlice.ts` (42), `src/store/store.ts:8`, `src/App.tsx:17`, `src/common/components/CustomAlert.tsx:14`, `src/hooks/useCRUDModal.ts:3,17,25` | Snackbar global de éxito/error (`setSuccessMessage`, `setErrorMessage`, `closeAlert`) |
| **React Context** | `src/context/SocketContext.tsx` (59) — único `createContext` del proyecto (`:13`) | Conexión socket.io compartida: expone `isOnline` y `subscribe`. Consumido por `NotificationBell.tsx:57` y `Tracking.tsx:14` |
| **React Query (TanStack v4)** | 56 usos de `useQuery(`/`useQuery<`/`useMutation(` repartidos en pages + `src/hooks/useTable.ts:21`, `src/hooks/useCRUDModal.ts:31,41,51`. `QueryClientProvider` en `src/App.tsx:14,20` | Todo el cacheo/fetching de datos de servidor y las mutaciones CRUD |
| **`useState` local** | 116 ocurrencias en 35 archivos `.tsx` | Apertura de modales, fila seleccionada, filtros de texto/fecha, paginación (`useTable.ts:16-18`), estado de dibujo de polígonos (`CoverageZones.tsx:67-70`), formulario no controlado por RHF (`Distributors.tsx:22`) |
| **`react-hook-form`** | 11 archivos: `CustomerModal`, `TimeSlotsManager`, `UserModal`, `CreateAdminModal`, `CreateEnvaseModal`, `ResolveIncidentModal`, `CylinderModal`, `PromotionsManager`, `ResolveClaimModal`, `DeliveryModal`, `CarModal` | Estado de formularios en modales |
| **`useForm` propio** | `src/hooks/UseForm.ts` (28) — usado sólo en `src/pages/Auth/LoginPage.tsx:15` | Formulario de login (no usa react-hook-form) |
| **`localStorage`** | `src/services/api/axiosConfig.ts:26,39,57,69`, `src/routes/DashboardRoutes.tsx:34`, `src/hooks/useCheckAuth.ts:20`, `src/context/SocketContext.tsx:37`, `src/store/auth/thunks.ts:24,29,64,70,78,85,91`, `src/pages/Distributors/Distributors.tsx:11,56,57` | `token`, `expireTimestamp`, `selectedDistributor` (header `X-Distributor`) |

### Casos en que conviven varios mecanismos para lo mismo
1. **Dos formas de notificar al usuario**: el snackbar Redux (`uiSlice` + `CustomAlert`), que sólo dispara `useCRUDModal` (`useCRUDModal.ts:17,25`), conviven con SweetAlert2 usado directamente en **18 archivos** (`Customers.tsx`, `Leads.tsx`, `Cylinders.tsx`, `Deliveries.tsx`, `Cars.tsx`, `Orders.tsx`, `Claims.tsx`, `Incidents.tsx`, `Envases.tsx`, `Admins.tsx`, `CoverageZones.tsx`, `Reservations.tsx`, `TimeSlotsManager.tsx`, `AssignDriverModal.tsx`, `CylinderDetails.tsx`, `DeliveryDetails.tsx`, `CarsManager.tsx`, `LeadsDetailsView.tsx`, más `store/auth/thunks.ts`).
2. **Dos formas de mutar la misma entidad**: `Customers.tsx` toma el `deleteMutation` de `useCRUDModal` (`:20-23`) pero define su propio `useMutation` para alta/edición (`:25-71`); idéntico patrón en `Deliveries.tsx:26-29` vs `:31-88` y en `Leads.tsx`. El borrado notifica por snackbar Redux y el alta por Swal, en la misma pantalla.
3. **Dos formas de leer listados**: el hook `useTable` (`src/hooks/useTable.ts`), usado por las 6 tablas que montan `CustomTable`, conviven con `useQuery` directo en 10 pantallas (`Claims`, `Incidents`, `Envases`, `Reservations`, `Reports`, `Ratings`, `Distributors`, `Admins`, `CoverageZones`, `CustomerDetails`) y con `useEffect` + `useState` manual en `FleetStatus.tsx:19-48`, `CarsManager.tsx:38-52`, `CylinderDetails.tsx:27-45`, `DeliveryDetails.tsx:26-38`, `LeadsDetailsView.tsx:43-57`.
4. **Dos formas de llegar al backend**: la capa `services/api/*` conviven con una llamada axios directa desde una pantalla, `CylinderDetails.tsx:3,31`.

---

## TABLA 3 — Capa de datos (`src/services/api/`)

20 archivos. `index.ts` (1 línea) re-exporta sólo `./users` y **no lo importa nadie** (ver Tabla 6).

| archivo | funciones exportadas | endpoints | instancia | errores |
|---|---|---|---|---|
| `admins.ts` (52) | `getAdmins`, `registerAdmin`, `getRoles` (+ tipos `AdminRole`, `AdminUser`, `Admin`, `RegisterAdminPayload`) | `GET /admin`, `POST /admin/register`, `GET /role` | `privateAxiosInstance` | Propaga (sin try/catch) |
| `auth.ts` (29) | `checkToken`, `getAdmin` | `POST /users/validate`, `GET /users/email/:email` | **Ambas**: `publicAxiosInstance` en `checkToken` (`:5`), `privateAxiosInstance` en `getAdmin` (`:11`) | `getAdmin` captura, hace `console.error` (`:26`) y re-lanza (`:27`). También lanza `Error('No tienes permisos de administrador')` si el rol no es admin/super_admin (`:17`) |
| `axiosConfig.ts` (76) | `RequestSource` (enum), `privateAxiosInstance`, `publicAxiosInstance` | — (config) | define ambas | Interceptor de request rechaza sin token (`:30`). Interceptor de response: en 401 limpia `token`/`expireTimestamp` y despacha `logOut` (`:56-60`); en 500 con `code` `auth/id-token-expired` o `auth/argument-error` despacha `startLogOut` (`:62-73`); siempre `Promise.reject(error)` (`:74`) |
| `cars.ts` (32) | `getAllCars`, `getCarsByUserId`, `createCar`, `updateCar`, `deleteCar` | `GET /car`, `GET /car/user/:userId`, `POST /car`, `PATCH /car/:id`, `DELETE /car/:id` | `privateAxiosInstance` | Propaga |
| `claims.ts` (39) | `getAllClaims`, `resolveClaim` (+ `Claim`) | `GET /claims`, `PATCH /claims/:id/resolve` | `privateAxiosInstance` | Propaga |
| `coverageZones.ts` (37) | `getCoverageZones`, `createCoverageZone`, `deleteCoverageZone` (+ `CoverageZone`, `CreateCoverageZonePayload`) | `GET /coverage-zones`, `POST /coverage-zones`, `DELETE /coverage-zones/:id` | `privateAxiosInstance` | Propaga |
| `customers.ts` (70) | `getAllCustomers`, `getCustomerById`, `updateCustomer`, `deleteCustomer`, `validateCustomer`, `createCustomer` | `GET /customers?limit&offset[&term]`, `GET /customers/:id`, `PATCH /customers/:id`, `DELETE /customers/:id`, `PATCH /customers/:id/validate`, `POST /users/customer-registration-admin` | `privateAxiosInstance` | Sólo `getAllCustomers` captura: `console.error` (`:30`) + `throw` (`:31`). El resto propaga |
| `cylinders.ts` (74) | `getAllCylinders`, `updateCylinder`, `updateCylinderStock`, `createCylinder`, `deleteCylinder` | `GET /gascylinder?limit&offset`, `PATCH /gascylinder/:id`, `PATCH /gascylinder/:id/stock`, `POST /gascylinder`, `DELETE /gascylinder/:id` | `privateAxiosInstance` | Sólo `getAllCylinders` captura: `console.error` (`:15`) + `throw` (`:16`) |
| `deliveries.ts` (69) | `getAllDeliveries`, `getDeliveryById`, `createDelivery`, `updateDelivery`, `deleteDelivery`, `toggleDeliveryStatus` | `GET /delivery?limit&offset[&term]`, `GET /delivery/:id`, `POST /users/delivery-registration`, `PATCH /delivery/:id`, `DELETE /delivery/:id`, `PATCH /delivery/:id/status` | `privateAxiosInstance` | Sólo `getAllDeliveries` captura: `console.error` (`:28`) + `throw` (`:29`) |
| `distributors.ts` (42) | `getAllDistributors`, `createDistributor`, `updateDistributor`, `deleteDistributor` (+ `Distributor`) | `GET /distributor`, `POST /distributor`, `PATCH /distributor/:id`, `DELETE /distributor/:id` | `privateAxiosInstance` | Propaga |
| `incidents.ts` (41) | `getAllIncidents`, `resolveIncident` (+ `IncidentType`, `IncidentStatus`, `Incident`) | `GET /incidents`, `PATCH /incidents/:id/resolve` | `privateAxiosInstance` | Propaga |
| `index.ts` (1) | re-export de `./users` | — | — | — |
| `orders.ts` (104) | `getAllOrders`, `assignDriverToOrder`, `cancelOrder`, `getOrdersByCustomer` (+ `OrderItem`, `Order`) | `GET /orders?limit&offset[&term&startDate&endDate]`, `PATCH /orders/:id/assign/:deliveryId`, `PATCH /orders/:id/cancel`, `GET /orders/customer/:customerId?limit&offset` | `privateAxiosInstance` | Propaga |
| `physicalCylinders.ts` (94) | `getPhysicalCylinders`, `createPhysicalCylinder`, `transitionPhysicalCylinder`, `getCylinderHistory`, `assignCylindersToOrder` (+ `CylinderState`, `PhysicalCylinder`, `CylinderMovement`) | `GET /cylinders[?state=]`, `POST /cylinders`, `PATCH /cylinders/:id/transition`, `GET /cylinders/:id/history`, `POST /cylinders/assign` | `privateAxiosInstance` | Propaga |
| `ratings.ts` (42) | `getRatingSummary`, `getRatingsForUser` (+ `RaterRole`, `Rating`, `RatingSummary`) | `GET /ratings/user/:userId/summary`, `GET /ratings/user/:userId` | `privateAxiosInstance` | Propaga |
| `reports.ts` (75) | `getSalesByDriver`, `getSalesByProduct`, `getSalesByPayment`, `getSalesEvolution` (+ 4 interfaces; helper privado `buildQuery`) | `GET /reports/sales-by-driver`, `/sales-by-product`, `/sales-by-payment`, `/sales-evolution` (todos con `?from&to`, el último con `granularity`) | `privateAxiosInstance` | Propaga |
| `reservations.ts` (35) | `getReservations`, `confirmDeposit` (+ `ReservationItem`, `Reservation`) | `GET /orders/reservations`, `PATCH /orders/:id/confirm-deposit` | `privateAxiosInstance` | Propaga |
| `stats.ts` (52) | `getDashboardStats`, `getSalesChart` (+ `DashboardStats`, `ChartData`) | `GET /orders/stats/summary[?from&to]`, `GET /orders/stats/chart?aggregation[&from&to]` | `privateAxiosInstance` | Propaga |
| `timeslots.ts` (27) | `getAllTimeSlots`, `createTimeSlot`, `deleteTimeSlot` (+ `TimeSlot`) | `GET /time-slot`, `POST /time-slot`, `DELETE /time-slot/:id` | `privateAxiosInstance` | Propaga |
| `users.ts` (102) | `getAllUsers`, `createUser`, `deleteUser`, `updateUser`, `resetUserPassword`, `blockUser`, `getUserByEmail`, `getUserById` | `GET /users?limit&offset[&term]`, `POST /users`, `DELETE /users/:id`, `PATCH /users/:id`, `PATCH /users/:id` (reset password), `PATCH /users/:id/block`, `GET /users/email/:email`, `GET /users/:id` | `privateAxiosInstance` | 3 con try/catch: `getAllUsers` (`console.error`+`throw`, `:26-27`), `getUserByEmail` (devuelve `null` si 404, `:84`), `getUserById` (lanza `Error('Usuario no encontrado')` si 404, `:99`). Contiene **8 `console.*`** (`:16`, `:26`, `:77`, `:79`, `:82`, `:92`, `:94`, `:97`), el archivo con más logging del repo |

### Resumen Tabla 3
- Archivos: **20**. Funciones exportadas de acceso a datos: **64**. Endpoints distintos citados: **~52**.
- `publicAxiosInstance` se usa en **un solo** punto (`auth.ts:5`, `POST /users/validate`); las otras 63 funciones usan `privateAxiosInstance`.
- Sólo **5** funciones de servicio tienen `try/catch`, todas en listados paginados, y todas re-lanzan. El resto propaga.
- `baseURL` = `import.meta.env.VITE_APP_API_URL` (`axiosConfig.ts:11`). Hay `.env` en la raíz del repo.

---

## TABLA 4 — Tipado

**`strict` está ACTIVO.** `tsconfig.json:22` → `"strict": true`, junto con `"noUnusedLocals": true` (`:23`), `"noUnusedParameters": true` (`:24`) y `"noFallthroughCasesInSwitch": true` (`:25`). No existe `tsconfig.app.json`; sólo `tsconfig.json` y `tsconfig.node.json`.

| categoría | conteo | detalle |
|---|---|---|
| Ocurrencias totales del token `any` | **140** (en 52 archivos) | — |
| `as any` | **36** en 4 archivos | `OrderDetailsModal.tsx` 28, `OrdersTable.tsx` 4, `DeliveryModal.tsx` 2, `CustomerModal.tsx` 2 |
| Anotaciones `: any` | **97** | ver listado abajo |
| Genéricos `<any` | **7** | `CustomTable.tsx:15`, `useTable.ts:6`, `Leads.tsx:10`, `CarsTable.tsx:93`, `PromotionsManager.tsx:13,14`, `Ratings.tsx:76` (este último es `useQuery<Rating[]>`, tipado) |
| `@ts-ignore` / `@ts-expect-error` | **0** | — |
| `@ts-nocheck` | **1** | `src/firebase/providers.ts:1` — desactiva el chequeo de todo el archivo (33 líneas) |
| `/* eslint-disable */` de archivo completo | **2** | `src/store/auth/authSlice.ts:1`, `src/store/ui/uiSlice.ts:1` |
| `unknown` | **8** | usos legítimos (`useSocket.ts:10,70`, `csv.ts:3,12`, `NotificationBell.tsx:27`) |
| Props sin tipar | **0** | Se auditaron los 85 componentes `.tsx` con props destructuradas: **todos** llevan anotación de tipo en el parámetro. El problema no es la ausencia de tipo sino que el tipo contiene `any` (ver abajo) |
| Funciones exportadas sin tipo de retorno explícito | **89 de 90** | La única con retorno explícito es `rowsToCsv` (`src/utils/csv.ts:12`, `: string`) |

### `as any` — ubicaciones exactas
- `src/pages/Orders/components/OrderDetailsModal.tsx`: `:69`, `:73` (×2), `:99`, `:102`, `:104`, `:115`, `:118`, `:123` (×2), `:143` (×2), `:150` (×2), `:158`–`:161` (×4), `:168` (×2), `:178` (×2), `:185`, `:196`, `:199`, `:219`, `:252`, `:261`
- `src/pages/Orders/components/OrdersTable.tsx`: `:119`, `:129`, `:150`, `:188`
- `src/pages/Customers/components/CustomerModal.tsx`: `:238`, `:273`
- `src/pages/Deilverys/components/DeliveryModal.tsx`: `:285`, `:320`

### `: any` — listado completo (97)
`AuthLayout.tsx:8` · `UploadFileInput.tsx:13` · `CustomAlert.tsx:14` · `SideMenu.tsx:32` · `TableLoadingOrNoData.tsx:20` · `CustomTable.tsx:15,18,46` · `firebase/providers.ts:22` · `useTable.ts:6,7` · `UseForm.ts:11` (×2) · `Customers.tsx:26,57,73` · `CustomerModal.tsx:15,70,71` · `CustomerDetails.tsx:39,159,233,247` · `SalesStats.tsx:26` · `RecentOrdersWidget.tsx:27,84` · `CustomersTable.tsx:18,39,149` · `FleetStatus.tsx:42` · `DashboardStats.tsx:54` · `TimeSlotsManager.tsx:82` · `LoginPage.tsx:19` · `Leads.tsx:10,20,47,78,118,182` · `UserModal.tsx:6,9,50` · `LeadsTable.tsx:18,39,129` · `LeadsDetailsView.tsx:49` · `Admins.tsx:34` · `CreateAdminModal.tsx:174` · `Cars.tsx:16,61` · `CarsTable.tsx:16,45,93,132` · `Orders.tsx:45` · `AssignDriverModal.tsx:32,63` · `Envases.tsx:56,76` · `OrderDetailsModal.tsx:17,24,219` · `CreateEnvaseModal.tsx:101` · `OrdersTable.tsx:41,225` · `Cylinders.tsx:31,50,70,179` · `PromotionsManager.tsx:13,14,34` · `CylinderDetails.tsx:58` · `Claims.tsx:59` · `CylindersTable.tsx:17,30,151` · `CylinderModal.tsx:11` · `Deliveries.tsx:32,65,90` · `Reports.tsx:320,367` · `ResolveClaimModal.tsx:42` · `CarsManager.tsx:70,95` · `DeliveryModal.tsx:17,82,83,196` · `DeliveriesTable.tsx:19,40,164` · `CarModal.tsx:12,177` · `services/api/deliveries.ts:40` · `services/api/cylinders.ts:14` · `services/api/customers.ts:29,64` · `services/api/users.ts:25,81,96` · `services/api/auth.ts:25` · `store/auth/thunks.ts:89`

### Patrones de tipado repetidos
- **Contrato de eventos de tabla sin tipar**: `setAction: (event: any) => void` / `setLead` / `setLocalAction` aparece en 5 tablas (`CustomersTable.tsx:18`, `LeadsTable.tsx:18`, `CarsTable.tsx:16`, `DeliveriesTable.tsx:19`, `CylindersTable.tsx:17`) y su consumidor lo desestructura también como `any` (`Customers.tsx:73`, `Cars.tsx:61`, `Deliveries.tsx:90`, `Cylinders.tsx:70`, `Leads.tsx:78`).
- **`onSave: (data: any) => void`** en 5 modales: `CustomerModal.tsx:15`, `UserModal.tsx:9`, `CylinderModal.tsx:11`, `DeliveryModal.tsx:17`, `CarModal.tsx:12`.
- **`getRowId={(row: any) => ...}`** en las 5 tablas: `CustomersTable.tsx:149`, `LeadsTable.tsx:129`, `CarsTable.tsx:132`, `CylindersTable.tsx:151`, `DeliveriesTable.tsx:164`, `OrdersTable.tsx:225`.
- **Interface duplicada**: `export interface Delivery` está declarada **dos veces** en el mismo archivo, `src/interfaces/index.ts:56` y `src/interfaces/index.ts:95`, con campos distintos (`id?: string` vs `delivery_id: string`, `cars?: Car[]` sólo en la segunda). TypeScript las fusiona en una sola declaración.
- **Comentarios que documentan desajuste de contrato**: `services/api/orders.ts:13` (`Ojo: Tu DTO dice 'id' pero tu entidad 'order_id'`), `interfaces/index.ts:45` (`OJO: Tu backend usa string "true" / "false", no boolean`), `interfaces/index.ts:57` (`A veces el ID está en user_id, depende de tu entidad TypeORM`).

---

## TABLA 5 — Manejo de errores en la interfaz

### Mecanismos disponibles
| mecanismo | dónde se define | dónde se consume |
|---|---|---|
| SweetAlert2 (`Swal.fire`) | dependencia directa | **18 archivos de `src/pages` + `src/store/auth/thunks.ts`** |
| Snackbar MUI vía Redux (`uiSlice` → `CustomAlert`) | `src/store/ui/uiSlice.ts`, `src/common/components/CustomAlert.tsx`, montado en `src/App.tsx:32` | Sólo lo dispara `src/hooks/useCRUDModal.ts:17,25` (usado por `Customers.tsx:20`, `Deliveries.tsx:26`, `Leads.tsx`) |
| Banner inline | — | Único caso: `src/pages/Distributors/Distributors.tsx:137-141` (`{createMut.isError && ...}`) |
| Toast Swal (`Swal.mixin`) | — | `src/pages/Deilverys/components/DeliveryDetails.tsx:55` |
| Estado de error de tabla | `src/hooks/useTable.ts:21,61` devuelve `isError` | **Nadie lo consume.** `CustomTable.tsx` sólo distingue `isLoading` y `rows.length === 0` (`:65-68`); si la query falla, la tabla muestra "No hay datos para mostrar." (`TableLoadingOrNoData.tsx:29`) |

### `catch` vacíos o que sólo loguean
Se auditaron los **25 bloques `catch`** del repo:
- **Vacío literal: 0.**
- **Sólo `console.error`, sin feedback al usuario: 2**
  - `src/pages/Deilverys/components/CarsManager.tsx:46` → `console.error('Error cargando autos:', error);`
  - `src/pages/Home/views/FleetStatus.tsx:45` → `console.error('Error cargando flota:', error);`
- **`console.error` + `throw` (capa de servicio, sin UI): 5** — `services/api/auth.ts:25`, `services/api/customers.ts:29`, `services/api/cylinders.ts:14`, `services/api/deliveries.ts:27`, `services/api/users.ts:25`
- El resto (18) muestra `Swal.fire` al usuario.
- Falso positivo descartado: el `catch` de `src/store/auth/thunks.ts:41` está dentro de un bloque comentado (`:36-45`).

### `console.*` en producción — 16 archivos, 24 llamadas
`services/api/users.ts` (8: `:16,26,77,79,82,92,94,97`), `services/api/customers.ts:30`, `services/api/cylinders.ts:15`, `services/api/deliveries.ts:28`, `services/api/auth.ts:26`, `store/auth/thunks.ts:50`, `hooks/useCheckAuth.ts:38`, `hooks/useSocket.ts:49`, `common/components/UploadFileInput.tsx`, `pages/Home/views/FleetStatus.tsx:45`, `pages/Leads/Leads.tsx:183`, `pages/Leads/components/LeadsDetailsView.tsx:71`, `pages/Gascilinders/Cylinders.tsx:51,180`, `pages/Gascilinders/components/CylinderDetails.tsx:36`, `pages/Deilverys/components/DeliveryDetails.tsx:33`, `pages/Deilverys/components/CarsManager.tsx:46`.

### Pantallas cuyas llamadas NO tienen manejo de error
| pantalla | archivo | llamadas sin `onError` / `isError` / `catch` con UI |
|---|---|---|
| `home` → Ventas | `src/pages/Home/views/SalesStats.tsx:12` | `useQuery` sin `onError`; si falla, cae al objeto por defecto de `:26` y muestra ceros como si fueran datos |
| `home` → KPIs | `src/pages/Home/views/DashboardStats.tsx:16,23,29,35` | 4 `useQuery`, ninguno con `onError` |
| `home` → Últimos pedidos | `src/pages/Home/views/RecentOrdersWidget.tsx:40` | `useQuery` sin `onError` |
| `home` → Flota | `src/pages/Home/views/FleetStatus.tsx:19-48` | `useEffect` + `catch` que sólo hace `console.error` (`:45`) |
| `reports` | `src/pages/Reports/Reports.tsx:53,58,63,69` | 4 `useQuery`, ninguno con `onError`; no hay `isError` en la vista |
| `ratings` | `src/pages/Ratings/Ratings.tsx:53,59,70,76` | 4 `useQuery`, ninguno con `onError` |
| `customers/details/:id` | `src/pages/Customers/components/CustomerDetails.tsx:63,69` | 2 `useQuery`, ninguno con `onError` |
| `ordenes` (cancelación) | `src/pages/Orders/Orders.tsx:58-74` | `cancelMutation` tiene `onSuccess` pero **no `onError`** (el `assignMutation` sí lo tiene, `:45`) |
| `distributors` | `src/pages/Distributors/Distributors.tsx:31,44` | El `useQuery` de listado y `toggleStatusMut` no tienen manejo de error; sólo `createMut` muestra banner (`:137`) |
| `admins` (listado) | `src/pages/Admins/Admins.tsx:16` | `useQuery(['admins'], getAdmins)` sin `onError`; si falla muestra el vacío "Sin admins" (`:89`) |
| `cars` (alta/edición) | `src/pages/Cars/Cars.tsx:15-42` | `saveMutation` tiene `onSuccess` pero **no `onError`** |
| `cars` (borrado) | `src/pages/Cars/Cars.tsx:44-59` | `deleteMutation` tiene `onSuccess` pero **no `onError`** |
| `configuracion` (borrado de franja) | `src/pages/Configuration/components/TimeSlotsManager.tsx:64` | `deleteMutation` con `onSuccess` y sin `onError` (el `createMutation` sí tiene, `:48`) |
| Todas las que usan `CustomTable` | `src/common/components/CustomTable/CustomTable.tsx:65` | El fallo de red se renderiza como "No hay datos para mostrar." — indistinguible de una lista vacía. Afecta a `users`, `customers`, `cylinders`, `deliveries`, `cars`, `ordenes` |

---

## TABLA 6 — Código muerto y restos

### 6.a — Archivos de 0 bytes
| archivo |
|---|
| `src/pages/Cars/components/CarsDetails.tsx` (0 bytes) |
| `src/pages/Cars/components/CarsModal.tsx` (0 bytes) |
| `src/pages/Cars/components/index.ts` (0 bytes) |
| `src/pages/Configuration/index.ts` (0 bytes) |
| `src/pages/Configuration/components/index.ts` (0 bytes) |

### 6.b — Archivos no alcanzables desde el entrypoint
Se recorrió el grafo de imports desde `src/index.tsx`: **137 de 162** archivos `.ts`/`.tsx` son alcanzables; **25 no lo son**.

| archivo | bytes | nota |
|---|---|---|
| `src/common/components/Navbar/Items.tsx` | 779 | Exporta `items`, sólo lo importa `SideDrawer.tsx:9` (también muerto) |
| `src/common/components/Navbar/components/DrawerItem.tsx` | 1.970 | Exporta `DrawerItem` + `DrawerItemProps`; nadie lo importa. Tiene `useAppSelector` comentado en `:4` y `:17` |
| `src/common/components/Navbar/components/DrawerNestItem.tsx` | 2.864 | Nadie lo importa. `useAppSelector` comentado en `:6` y `:29` |
| `src/common/components/Navbar/components/NotificationDropdown.tsx` | 2.381 | Exporta `NotificationDropDown`; nadie lo importa. El vivo es `NotificationBell.tsx` |
| `src/common/components/Navbar/components/SideDrawer.tsx` | 3.683 | Nadie lo importa. Contiene bloque JSX comentado de **25 líneas** (`:89-113`) |
| `src/common/components/sidemenu/SideMenuItem.tsx` | 759 | Nadie lo importa; `SideMenu.tsx` no lo usa |
| `src/pages/Home/views/Widget.tsx` | 3.227 | Exporta `Widget`; nadie lo importa. El vivo es `RecentOrdersWidget.tsx` |
| `src/pages/Leads/components/ReturnButon.tsx` | 378 | Nadie lo importa (nótese el typo en el nombre del archivo y del símbolo) |
| `src/pages/Cars/components/CarsDetails.tsx` | 0 | vacío |
| `src/pages/Cars/components/CarsModal.tsx` | 0 | vacío |
| `src/pages/Cars/components/index.ts` | 0 | vacío |
| `src/pages/Configuration/index.ts` | 0 | vacío |
| `src/pages/Configuration/components/index.ts` | 0 | vacío |
| `src/routes/index.ts` | 19 | Contiene `export * from './';` — **se re-exporta a sí mismo** |
| `src/services/api/index.ts` | 24 | `export * from './users';` — nadie lo importa |
| `src/pages/Cars/index.ts` | 22 | Barrel sin importadores (el router importa `../pages/Cars/Cars`) |
| `src/pages/Customers/index.ts` | 27 | ídem |
| `src/pages/Gascilinders/index.ts` | 27 | ídem |
| `src/pages/Claims/components/index.ts` | 35 | ídem |
| `src/pages/Gascilinders/components/index.ts` | 98 | ídem |
| `src/pages/Home/views/index.ts` | 90 | ídem |
| `src/pages/Leads/components/index.ts` | 29 | ídem |
| `src/pages/Orders/components/index.ts` | 65 | ídem |
| `src/pages/Tracking/components/index.ts` | 96 | ídem |
| `src/vite-env.d.ts` | 38 | declaración de tipos, no es import |

### 6.c — Exports sin ningún importador externo (31 de 221)
| símbolo | archivo:línea |
|---|---|
| `DrawerItemProps` | `src/common/components/Navbar/components/DrawerItem.tsx:6` |
| `NotificationDropDown` | `src/common/components/Navbar/components/NotificationDropdown.tsx:10` |
| `SideDrawer` | `src/common/components/Navbar/components/SideDrawer.tsx:16` |
| `drawerWidth` | `src/common/components/Navbar/components/SideDrawer.tsx:50` |
| `SideMenuItem` | `src/common/components/sidemenu/SideMenuItem.tsx:10` |
| `UserAddress` | `src/interfaces/index.ts:14` |
| `Lead` | `src/interfaces/index.ts:25` |
| `ReturnButon` | `src/pages/Leads/components/ReturnButon.tsx:5` |
| `AdminRole` | `src/services/api/admins.ts:3` |
| `AdminUser` | `src/services/api/admins.ts:9` |
| `RequestSource` | `src/services/api/axiosConfig.ts:7` (sólo uso interno del propio archivo) |
| `CreateCoverageZonePayload` | `src/services/api/coverageZones.ts:15` |
| `validateCustomer` | `src/services/api/customers.ts:57` — endpoint `PATCH /customers/:id/validate` que ninguna pantalla llama |
| `toggleDeliveryStatus` | `src/services/api/deliveries.ts:64` — `PATCH /delivery/:id/status` sin consumidor |
| `deleteDistributor` | `src/services/api/distributors.ts:39` — `DELETE /distributor/:id` sin consumidor |
| `IncidentStatus` | `src/services/api/incidents.ts:4` |
| `OrderItem` | `src/services/api/orders.ts:4` |
| `CylinderMovement` | `src/services/api/physicalCylinders.ts:28` |
| `assignCylindersToOrder` | `src/services/api/physicalCylinders.ts:85` — `POST /cylinders/assign` sin consumidor |
| `RaterRole` | `src/services/api/ratings.ts:4` |
| `RatingSummary` | `src/services/api/ratings.ts:20` |
| `SalesByDriver` | `src/services/api/reports.ts:3` |
| `SalesByProduct` | `src/services/api/reports.ts:10` |
| `SalesByPayment` | `src/services/api/reports.ts:17` |
| `SalesEvolutionPoint` | `src/services/api/reports.ts:55` |
| `ReservationItem` | `src/services/api/reservations.ts:3` |
| `ChartData` | `src/services/api/stats.ts:29` |
| `getSalesChart` | `src/services/api/stats.ts:45` — `GET /orders/stats/chart` sin consumidor |
| `getUserByEmail` | `src/services/api/users.ts:75` — el comentario de `:74` dice "reemplaza getAdmin", pero `getAdmin` sigue vivo en `auth.ts:9` y es el que usan `useCheckAuth.ts:5` y `thunks.ts:7` |
| `checkingAuthentication` | `src/store/auth/thunks.ts:16` |
| `checkIfTokenExpired` | `src/store/auth/thunks.ts:22` — usa `checkToken` (única razón de que exista `publicAxiosInstance`) y nadie lo invoca |

### 6.d — Bloques comentados de más de 5 líneas
| ubicación | líneas comentadas | contenido |
|---|---|---|
| `src/App.tsx:23-33` | 11 | `<BrowserRouter>` + `<Routes>` viejos, más los imports comentados en `:1`, `:6`, `:7` |
| `src/store/auth/thunks.ts:36-45` | 10 | `startCreatingUserWithEmailPassword` completo, comentado; más los imports comentados de `:10-14` |
| `src/common/components/Navbar/components/SideDrawer.tsx:89-113` | 25 | bloque JSX `<Tooltip title='Logout'>` completo (archivo además no alcanzable) |
| `src/common/components/LogoSplg.tsx:6-11` | 6 | JSDoc (documentación legítima, no código muerto) |
| `src/hooks/useSocket.ts:82-88` | 7 | comentario explicativo del cleanup (legítimo) |
| `src/pages/Distributors/Distributors.tsx:13-18` | 6 | JSDoc (legítimo) |
| `src/pages/Leads/components/LeadsDetailsView.tsx:64-70` | 7 | lógica de bloqueo futura comentada + variable `action` comentada |

### 6.e — Marcas TODO / NUEVO / "Pendiente" / "Agregado"
| archivo:línea | texto |
|---|---|
| `src/hooks/useSocket.ts:12` | `// TODO(backend): centralizar acá todos los eventos que el gateway de Nest…` |
| `src/hooks/useSocket.ts:58` | `// TODO(backend): reemplazar por el handshake real (JWT/rol) cuando el gateway lo valide` |
| `src/context/SocketContext.tsx:36` | `// TODO: refrescar con getIdToken() si expira (los ID token duran 1h)` |
| `src/common/components/Navbar/components/NotificationBell.tsx:21` | `// TODO(backend): ajustar esta interfaz al payload real que emita el gateway` |
| `src/pages/Leads/components/LeadsDetailsView.tsx:71` | `console.log('Toggle block clicked (Lógica pendiente)')` |
| `src/routes/DashboardRoutes.tsx:15` | `import { Cars } from '../pages/Cars/Cars'; // <--- NUEVO IMPORT` |
| `src/routes/DashboardRoutes.tsx:73` | `{/* 7. Ordenes (Pendiente) */}` (la pantalla está implementada) |
| `src/pages/Orders/Orders.tsx:20` | `// <--- NUEVO ESTADO` |
| `src/pages/Orders/Orders.tsx:83` | `// NUEVO: Ver Detalles` |
| `src/pages/Orders/Orders.tsx:148` | `{/* Modal de Detalles (NUEVO) */}` |
| `src/pages/Home/Home.tsx:1-3` | `// <--- NUEVO` / `// <--- YA LO TENÍAS` / `// <--- EL QUE HICIMOS ANTES` |
| `src/hooks/useTable.ts:7` | `// <--- NUEVO: Para pasar filtros o búsqueda` |
| `src/common/components/CustomTable/CustomTable.tsx:18` | `// Agregado para flexibilidad` |
| `src/pages/Gascilinders/components/CylindersTable.tsx:32` | `{/* 1. Ver Detalle (NUEVO) */}` |
| `src/pages/Cars/components/CarsTable.tsx:28` | `// 1. Usamos useTable en lugar de useQuery directo para mantener consistencia` |
| `src/pages/Gascilinders/components/CylinderDetails.tsx:3` | `// Usaremos axios directo si no tienes la fn exportada` |
| `src/pages/Customers/components/CustomersTable.tsx:41` | `{/* --- BOTÓN VER DETALLE (CORREGIDO) --- */}` |
| `src/services/api/customers.ts:9-10` | `// Nota: Tu backend actual de CustomersService.findAll aún no filtra por 'term'…` |
| `src/services/api/users.ts:9` | `// Si el Backend deployado es viejo, simplemente va a ignorar este parámetro extra…` |
| `src/services/api/orders.ts:82-84` | comentario de 3 líneas explicando un bug de `ValidationPipe` ya resuelto |
| `src/services/api/users.ts:89` | `// services/api/users.ts - agregar esta función` |

---

## TABLA 7 — Tiempo real

### `src/hooks/useSocket.ts` (100 líneas)
| aspecto | hecho |
|---|---|
| URL | `SOCKET_URL` = `VITE_APP_SOCKET_URL` ?? `VITE_APP_API_URL` sin el sufijo `/api` (`:6-8`) |
| Catálogo de eventos | `ORDER_SOCKET_EVENTS` (`:14-20`): `order:created`, `order:accepted`, `order:on_the_way`, `order:delivered`, `order:cancelled` |
| Creación del socket | `io(...)` una sola vez, guardado en `useRef`, con `autoConnect: false` (`:36-44`) |
| **Reconexión** | **Sí, configurada explícitamente** (`:41-43`): `reconnection: true`, `reconnectionAttempts: Infinity`, `reconnectionDelay: 1000`, `reconnectionDelayMax: 10000`. `transports: ['websocket']` (`:40`) |
| **Manejo de desconexión** | **Sí**: listeners `connect` → `setIsOnline(true)` (`:46`), `disconnect` → `setIsOnline(false)` (`:47`), `connect_error` → `console.error` + `setIsOnline(false)` (`:48-51`) |
| API expuesta | `{ isOnline, connect, disconnect, subscribe }` (`:99`). `subscribe` devuelve la función de baja (`:75-77`) |
| Cleanup al desmontar | `removeAllListeners()` + `disconnect()` + `socketRef.current = null` (`:89-97`); el comentario `:82-88` documenta que antes se llamaba `.off()` sin argumentos y eso rompía `isOnline` |
| Auth del handshake | `socket.auth = auth ?? {}` (`:60`), con `TODO(backend)` en `:58` que dice que hoy `auth` viaja "como contexto informativo nomás" |

### `src/context/SocketContext.tsx` (59 líneas)
| aspecto | hecho |
|---|---|
| Namespace | `/admin` (`:20`) |
| Contexto | `SocketContextValue { isOnline, subscribe }` (`:5-11`); `createContext<... | undefined>(undefined)` (`:13`) |
| Cuándo conecta | `useEffect` (`:28-42`): si `status !== 'authenticated'` o no hay `uid` → `disconnect()` y sale (`:29-32`); si no, lee `localStorage.getItem('token')` y llama `connect({ token, uid, role })` (`:37-39`) |
| Cuándo desconecta | Cleanup del efecto: `return () => disconnect()` (`:41`) — es decir, también al cambiar `status`, `uid` o `role` |
| Guard | `useSocketContext` lanza `Error('useSocketContext debe usarse dentro de un <SocketProvider>')` si falta el provider (`:52-57`) |
| Montaje | `<SocketProvider>` envuelve `<Navigation />` y `<CustomAlert />` en `src/App.tsx:21-34` |
| Limitación anotada | `TODO` en `:36`: el ID token dura 1 h y no se refresca con `getIdToken()` |

### Consumidores
| pantalla / componente | archivo:línea | eventos a los que se suscribe |
|---|---|---|
| Campana de notificaciones (visible en todo el dashboard vía `Navbar` → `DashboardLayout`) | `src/common/components/Navbar/components/NotificationBell.tsx:57`, suscripción en `:77-87` | Los **5** de `ORDER_SOCKET_EVENTS` (`Object.values(...)`, `:79`). Acumula hasta `MAX_NOTIFICATIONS = 50` (`:45`, `:71`). Se dan de baja todos en el cleanup (`:86`) |
| `tracking` | `src/pages/Tracking/Tracking.tsx:14`, suscripción en `:39-45` | **`order:driver-location`** (`:11`) — evento que **no** está en `ORDER_SOCKET_EVENTS`, está hardcodeado en la pantalla. Un `Map<orderId, TrackedOrder>` que se actualiza por pedido (`:24-37`); centra el mapa sólo la primera vez (`:33-36`) |

**Total de consumidores del socket: 2.** Ninguna otra pantalla (ni `Orders`, ni `Home`, ni `Claims`) invalida su caché de React Query al llegar un evento: las notificaciones son sólo visuales.

---

## TABLA 8 — Duplicación (bloques de 10+ líneas casi idénticos, comparación normalizada por espacios y sin comentarios)

Se detectaron **23 pares/grupos** de archivos con al menos una ventana de 10 líneas normalizadas idénticas.

| # | ubicaciones | qué se repite |
|---|---|---|
| 1 | `src/services/api/customers.ts:13-25` ↔ `src/services/api/deliveries.ts:11-23` | El `try { get(url) } / if (data && !Array.isArray(data) && data.rows !== undefined) { return {rows, total} } / return {rows: Array.isArray(data)?data:[], total: ...100}` completo, byte por byte |
| 2 | `src/pages/Home/views/RecentOrdersWidget.tsx:16-26` ↔ `src/pages/Orders/components/OrdersTable.tsx:30-40` | `getStatusColor` (switch de 5 estados con clases Tailwind) + comienzo de `getStatusLabel` |
| 3 | `src/pages/Claims/Claims.tsx:32-41` ↔ `src/pages/CoverageZones/CoverageZones.tsx:79-88` ↔ `src/pages/Incidents/Incidents.tsx:45-54` ↔ `src/pages/Reservations/Reservations.tsx:43-52` | Bloque `icon: 'success' / customClass.confirmButton: 'bg-indigo-600 …' / buttonsStyling: false` + apertura del `onError` |
| 4 | `src/pages/Configuration/components/TimeSlotsManager.tsx:52-61` ↔ `src/pages/Customers/Customers.tsx:62-71` ↔ `src/pages/Deilverys/Deliveries.tsx:79-88` ↔ `src/pages/Leads/Leads.tsx:61-70` | Cierre del `Swal.fire` de error + `customClass` con `popup: 'rounded-2xl shadow-xl'` |
| 5 | `src/pages/Customers/Customers.tsx:48-57` ↔ `src/pages/Deilverys/Deliveries.tsx:56-65` ↔ `src/pages/Leads/Leads.tsx:38-47` | `onSuccess` del `saveMutation`: invalidate + cerrar modal + Swal de éxito |
| 6 | `src/pages/Customers/Customers.tsx:65-76` ↔ `src/pages/Deilverys/Deliveries.tsx:82-93` | `onError` + arranque de `handleAction` |
| 7 | `src/pages/Customers/Customers.tsx:80-89` ↔ `src/pages/Deilverys/Deliveries.tsx:97-106` ↔ `src/pages/Deilverys/components/CarsManager.tsx:117-126` | Swal de confirmación de borrado (`icon: 'warning'`, `confirmButtonColor: '#f43f5e'`, `cancelButtonColor: '#cbd5e1'`, …) |
| 8 | `src/pages/Customers/Customers.tsx:84-94` ↔ `src/pages/Deilverys/components/CarsManager.tsx:121-131` | idem, ventana desplazada |
| 9 | `src/pages/Customers/Customers.tsx:112-121` ↔ `src/pages/Deilverys/components/CarsManager.tsx:150-159` ↔ `src/pages/Leads/Leads.tsx:187-196` | Swal de error post-borrado |
| 10 | `src/pages/Customers/Customers.tsx:114-124` ↔ `src/pages/Leads/Leads.tsx:189-199` | idem, ventana desplazada |
| 11 | `src/pages/Deilverys/Deliveries.tsx:58-68` ↔ `src/pages/Leads/Leads.tsx:40-50` | Swal de éxito + apertura del `onError` |
| 12 | `src/pages/Customers/components/CustomerModal.tsx:36-47` ↔ `src/pages/Deilverys/components/DeliveryModal.tsx:46-57` | `useEffect` de `reset()` del formulario según entidad seleccionada |
| 13 | `src/pages/Customers/components/CustomerModal.tsx:109-118` ↔ `src/pages/Deilverys/components/DeliveryModal.tsx:121-130` ↔ `src/pages/Leads/components/UserModal.tsx:77-86` | Campo "Nombre completo" con `register`, label, clases Tailwind y mensaje de error |
| 14 | `src/pages/Customers/components/CustomersTable.tsx:150-159` ↔ `src/pages/Deilverys/components/DeliveriesTable.tsx:165-174` | Props de cierre del `<CustomTable>` (`getRowId`, `setActive`, paginación) |
| 15 | `src/pages/Customers/components/CustomersTable.tsx:63-73` ↔ `src/pages/Leads/components/LeadsTable.tsx:70-81` | Definición de columna de contacto (email/teléfono) del DataGrid |
| 16 | `src/pages/Admins/Admins.tsx:127-136` ↔ `src/pages/Reservations/Reservations.tsx:198-207` | Cierre de `<tbody>/<table>/<div>` + estructura del estado vacío |
| 17 | `src/pages/Admins/components/CreateAdminModal.tsx:190-199` ↔ `src/pages/Envases/components/CreateEnvaseModal.tsx:122-131` ↔ `src/pages/Incidents/components/ResolveIncidentModal.tsx:127-136` | Footer del modal: botones Cancelar / Guardar con las mismas clases y estado `isSaving` |
| 18 | `src/pages/Admins/components/CreateAdminModal.tsx:191-200` ↔ `src/pages/Envases/components/CreateEnvaseModal.tsx:123-132` | idem, ventana desplazada |
| 19 | `src/pages/Envases/components/CreateEnvaseModal.tsx:119-129` ↔ `src/pages/Envases/components/TransitionModal.tsx:88-98` | Footer del modal |
| 20 | `src/pages/Envases/components/CreateEnvaseModal.tsx:120-130` ↔ `src/pages/Envases/components/TransitionModal.tsx:89-99` ↔ `src/pages/Incidents/components/ResolveIncidentModal.tsx:125-135` | idem |
| 21 | `src/pages/Envases/components/HistoryModal.tsx:34-43` ↔ `src/pages/Envases/components/TransitionModal.tsx:45-54` | Cabecera del modal (overlay + título + botón de cierre) |
| 22 | `src/pages/Cars/Cars.tsx:34-44` ↔ `src/pages/Configuration/components/TimeSlotsManager.tsx:53-64` | Swal de éxito con `customClass` + cierre del `onSuccess` |
| 23 | `src/pages/CoverageZones/CoverageZones.tsx:173-182` ↔ `src/pages/Tracking/components/TrackingMap.tsx:20-29` | Bloque `<MapContainer>` + `<TileLayer url="https://{s}.tile.openstreetmap.org/…">` con los mismos atributos |

**Patrón dominante**: 14 de los 23 grupos son bloques de configuración de `Swal.fire` (mismo `customClass`, mismo `buttonsStyling: false`, mismas clases Tailwind). Los otros 9 son footers/headers de modales, columnas de DataGrid, o el bloque de normalización `{rows, total}` de la capa de servicios.

---

## Anexo — otros hechos verificables

- `src/routes/index.ts` contiene `export * from './';`, un re-export circular sobre sí mismo (nadie lo importa, así que no se evalúa).
- `src/services/api/index.ts` re-exporta sólo `./users` de los 19 módulos de servicio; nadie lo importa.
- `src/pages/index.ts` (2 líneas) re-exporta sólo `Home`, `Auth` y `Leads`; el router usa ese barrel para `Home` y `Leads` (`DashboardRoutes.tsx:8`) y rutas directas para las otras 20 pantallas.
- `src/pages/Home/index.ts` exporta `export * from './Home.tsx'` — con extensión `.tsx` en el especificador (posible gracias a `allowImportingTsExtensions: true`, `tsconfig.json:11`).
- Directorio `src/pages/Deilverys/` — typo en el nombre del directorio (por "Deliverys"/"Deliveries"), presente en 8 rutas de import a lo largo del repo.
- `src/pages/Leads/components/ReturnButon.tsx` — typo en nombre de archivo y símbolo (`ReturnButon`).
- `src/store/auth/index.ts` re-exporta sólo `authSlice`; `thunks.ts` se importa siempre por ruta completa (`axiosConfig.ts:4`, `LoginPage.tsx:4`).
- El script de build es `tsc && vite build` (`package.json`), así que los errores de tipo bloquean el build; el script `lint` corre con `--max-warnings 0`.
- Dos librerías de gráficos instaladas: `recharts` ^3.7 (usada en `Reports.tsx:320,367`) y `chart.js`+`react-chartjs-2` ^4.4/^5.2. No se encontró ningún import de `chart.js` ni de `react-chartjs-2` en `src/`.
- `scss` ^0.2.4 está en dependencias junto a `sass` ^1.68; sólo hay un `.scss` (`src/styles/index.scss`, importado en `src/index.tsx:8`).
