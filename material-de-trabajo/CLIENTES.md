# Los clientes por dentro

El panel de administración y las dos aplicaciones, mirados por dentro:
arquitectura, pantallas, manejo de errores, código muerto y qué hace falta para
que corran. Todo verificado contra el código, abriendo cada archivo que se cita.

La **Parte I** es la lectura transversal: lo que se repite en los tres y lo que
afecta a una demostración. Las partes II a IV son el detalle de cada uno, para
cuando hay que tocar algo puntual.

---

## Parte I — Lectura transversal

Los tres clientes por dentro: arquitectura, pantallas, manejo de errores, código
muerto y qué hace falta para que corran. Todo verificado contra el código y
contra lo que compila; los hallazgos que se citan acá se comprobaron uno por
uno abriendo el archivo.

---

### Resumen

| | Panel | App cliente | App chofer |
|---|---|---|---|
| Archivos | 163 | 98 | 38 |
| Líneas | 13.284 | 10.922 | 5.183 |
| Compila | sí | sí (0 errores) | sí (0 errores) |
| Pantallas | 22 rutas | 12 vistas | 6 vistas |
| Esqueletos | 2 (+5 archivos vacíos) | 0 | 2 |
| **Pruebas reales** | **0** | **2** | **1** |

Los tres compilan y se pueden correr. El problema no es que estén rotos: es
que **fallan en silencio** y que **no hay red de seguridad** para tocarlos.

---

### 1. Lo que ningún usuario ve: los errores invisibles

Es el patrón que comparten los tres, y el más caro de arreglar después.

#### Panel — seis tablas que mienten

`useTable` expone `isError`, y **ningún componente lo consume**. El componente
que decide qué mostrar lo dice en su propio tipo:

```ts
// CustomTable/TableLoadingOrNoData.tsx
interface Props {
  status: "loading" | "noData"   // no existe un estado de error
}
```

Cuando la consulta falla, las **seis** tablas —clientes, usuarios, autos,
pedidos, garrafas, choferes— muestran *"No hay datos para mostrar."*. El
operador no puede distinguir "la API está caída" de "no hay registros".

Además, once pantallas no manejan el error de sus consultas: el tablero
principal y sus cuatro tarjetas, informes, calificaciones, detalle de cliente,
distribuidoras, administradores, autos, pedidos y configuración.

#### App cliente — la excepción muere en el datasource

Los **ocho** datasources atrapan la excepción, la escriben en el log y devuelven
`false` o `[]`. El motivo —401, 500, tiempo agotado— nunca llega a la pantalla.
Hay 22 `catch` que sólo loguean.

Lo que se ve en consecuencia: el catálogo de garrafas, el historial y las
franjas horarias muestran "vacío" cuando falló la consulta. El alta de dirección
desde el checkout es optimista y el propio código lo admite: *"This not check if
the address was created successfully"*. Con la sesión vencida, sólo el flujo del
QR avisa; en otros doce lugares falla mudo.

Dos casos puntuales:
- **El mapa**: el `catch` está literalmente vacío, con la única línea adentro
  comentada. Si falla la geolocalización, cae al centro por defecto sin avisar.
- **Direcciones**: el viewmodel escribe tres mensajes de error en `actionError`
  y **la vista nunca lo lee**. Los tres son invisibles.

#### App chofer — pasos críticos sin aviso

Aceptar un pedido: si la llamada falla, sólo se escribe en consola. **El diálogo
ya se cerró y el chofer cree que aceptó.** Lo mismo al ponerse disponible, al
rechazar, y en el reporte de posición: si el socket está caído, la posición se
descarta sin reintento.

---

### 2. Los tres hallazgos que afectan una demostración

#### El seguimiento en vivo sólo funciona en localhost

La app cliente configura la API por `--dart-define`, pero la URL del socket está
fija:

```dart
static const String _socketBaseUrl = 'http://localhost:3000/customers';
```

No pasa por `AppConfig`. En un teléfono real, el cliente **nunca ve moverse al
chofer**.

#### La entrega no la marca el chofer

La app del chofer **no llama nunca** a `confirm-delivery`. Muestra un QR, **lo
escanea el cliente**, y el chofer se entera porque consulta el pedido cada cinco
segundos hasta ver `delivered`.

Para mostrar el recorrido completo hacen falta **las dos apps funcionando a la
vez**, no sólo la del chofer.

#### "Cerrar sesión" no cierra la sesión

En la app del chofer, el `logout()` sólo frena el GPS y navega al login. No llama
a `signOut()` de Firebase, no desconecta el socket y **no marca al chofer como no
disponible**: sigue recibiendo ofertas de pedidos.

---

### 3. Seguridad

#### El token queda escrito en el log del dispositivo

App del chofer: `PrettyDioLogger` con `requestHeader: true` y
`requestBody: true`, **sin guarda de `kDebugMode`** —que no aparece en ninguna
parte del código—. En una compilación de producción, cada `Authorization:
Bearer` y cada contraseña del login quedan en el log.

#### Un archivo entero sin verificación de tipos

`src/firebase/providers.ts` empieza con `// @ts-nocheck`. Es el archivo que
maneja el inicio de sesión del panel.

#### Claves versionadas

La clave de Google Maps está en `AndroidManifest.xml` y en `AppDelegate.swift`,
y las de Firebase en `firebase_options.dart`. Son claves que por diseño viajan
en el cliente, pero conviene saber que están en el repositorio.

---

### 4. Arquitectura

#### Panel — siete mecanismos de estado conviviendo

Redux (dos slices), un Context para el socket, React Query (56 usos), 116
`useState` en 35 archivos, react-hook-form en 11 archivos, un `useForm` propio
usado sólo en el login, y localStorage. No hay una regla de cuándo usar cuál.

`strict` **sí** está activo en TypeScript, junto con `noUnusedLocals` y
`noUnusedParameters`. Pero hay **140 usos de `any`** en 52 archivos (36 de ellos
`as any`, 28 concentrados en un solo archivo) y **89 de 90 funciones exportadas
sin tipo de retorno**. El tipado está declarado pero vaciado por dentro.

Dato revelador: `interface Delivery` está declarada **dos veces en el mismo
archivo** (`interfaces/index.ts:56` y `:95`) con campos distintos. TypeScript las
fusiona en silencio.

#### App cliente — MVVM sobre Stacked, con la separación a medias

Cero `setState` en todo el código, lo cual es consistente. El camino completo
(vista → viewmodel → servicio → caso de uso → repositorio → datasource) se
respeta **sólo para pedidos, clientes, garrafas y direcciones**.

Cinco servicios instancian el datasource directo sin repositorio ni caso de uso,
y `OrderTrackingService` usa el cliente HTTP crudo salteándose toda la capa de
datos. Los siete casos de uso son un `call()` de una línea: hoy no agregan nada.

#### App chofer — la más simple y la más sólida en su flujo

No tiene `data/` ni `domain/`: los servicios hablan directo con el cliente HTTP.
Para el tamaño de la app es una decisión razonable.

El flujo del reparto está bien armado: login con Firebase más resolución del
usuario real contra la base, socket con `driver:join`, oferta por
`server:new-order-request` con cuenta regresiva, aceptación con
`Idempotency-Key`, y **posición reportada cada 10 metros en vez de por
intervalo de tiempo** —que es la decisión correcta para no gastar batería.

Detalle a revisar: la pantalla de reparto **consulta el pedido cada 5 segundos**
aunque ya tiene un socket abierto que podría avisarle del cambio.

---

### 5. Código muerto

| | Qué hay |
|---|---|
| **Panel** | 5 archivos de 0 bytes · 8 componentes inalcanzables · 10 barrels sin importador · 31 exports sin usar · 7 endpoints implementados que ninguna pantalla llama · `chart.js` y `react-chartjs-2` instalados con **cero importaciones** |
| **App cliente** | `BusinessHours` (66 líneas, huérfano) · `Market`, `NoticeSheet` e `InfoAlertDialog` registrados y nunca invocados · un cliente inventado hardcodeado (`customerId: '1234'`) como valor inicial |
| **App chofer** | `order_service.dart`: **153 líneas con 6 pedidos falsos** tras un `Future.delayed(2s)`, referenciado sólo por el locator · `DirectionsView` registrada sin llamadores · botones vacíos en notificaciones y "olvidé mi contraseña" |

---

### 6. Qué hace falta para correr cada uno

**Panel** — tiene su `.env`, compila y corre. El bundle son 1,93 MB en una sola
pieza (558 KB comprimido), sin dividir.

**Las dos apps** — no necesitan `.env`: todo va por `--dart-define`. La del
cliente espera cinco variables (`API_BASE_URL`, `DISTRIBUTOR` y las tres de
MercadoPago); la del chofer, una sola (`API_BASE_URL`). **No falta ningún
archivo**: toda la configuración de Firebase está versionada. Necesitan
`../splg-lib` en disco y el backend accesible.

Pendiente de infraestructura: el **certificado APNs** para las notificaciones en
iOS. Android no lo necesita.

---

### 7. Las pruebas

| Proyecto | Archivos | Pruebas reales |
|---|---:|---:|
| Backend | 18 specs / 238 archivos | una no compila |
| **Panel** | **0** | **0** — no hay ni script de test |
| App cliente | 20 | **2** (19 archivos vacíos) |
| App chofer | 9 | **1** (8 archivos vacíos) |

Los archivos de test de las apps son los esqueletos que genera el CLI de
`stacked`, sin contenido.

Y hay una razón arquitectónica detrás: los tests que existen **fallan** porque el
service locator instancia `DriverAuthService` al arrancar, que llama a
`FirebaseAuth.instance`, y en un test Firebase no está inicializado. No hay forma
de sustituirlo por un doble. Es el mismo problema de depender de una clase
concreta que ya vimos en el backend.

**Esto importa para lo que viene:** hay 26 casos de uso por programar y varios
refactors pendientes, y hoy no hay nada que avise si algo se rompe.

---

## Parte II — El panel de administración

Repo: `/Users/nahuelwagner/Desktop/myprojects/gearthlogic/projects/garrafitas/splg-app-admin`
Fecha del relevamiento: 2026-09-23
Stack declarado en `package.json`: React 18.2, TypeScript 5.0, Vite 4.4, `@tanstack/react-query` ^4.35.3, `@reduxjs/toolkit` ^2.2.3, `react-redux` ^9.1.1, `@mui/material` ^5.14, `@mui/x-data-grid` ^6.16, `react-hook-form` ^7.71, `sweetalert2` ^11.26, `socket.io-client` ^4.8.1, `leaflet`/`react-leaflet`, `recharts` ^3.7, `chart.js` ^4.4 + `react-chartjs-2`, `tailwindcss` ^3.4, `firebase` ^10.4, `axios` ^1.13.

**Conteo real de archivos:** 163 archivos bajo `src/` (162 `.ts`/`.tsx` + `src/styles/index.scss`). Total de líneas en `.ts`/`.tsx`: **13.284**.

Nota metodológica: todos los números salen de grep/find/AST-lite sobre el árbol `src/`. Los ficheros se abrieron para confirmar cada dato citado. **No se modificó ningún archivo del repositorio.**

---

### TABLA 1 — Pantallas (una fila por `<Route>` de `src/routes/DashboardRoutes.tsx`)

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

#### Resumen Tabla 1
- Rutas de pantalla: **22** (+1 catch-all).
- Pantallas que cumplen el criterio objetivo de esqueleto (<50 líneas / sólo título / TODO sin implementar): **2** → `Configuration.tsx` (27 líneas, sólo cabecera + un hijo) y `LeadsDetailsView.tsx` (acción de bloqueo comentada + `console.log`, `:66-71`).
- Pantallas sin ninguna llamada REST: `Home.tsx` (delega), `Configuration.tsx`, `Tracking.tsx` (sólo socket).

---

### TABLA 2 — Manejo de estado

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

#### Casos en que conviven varios mecanismos para lo mismo
1. **Dos formas de notificar al usuario**: el snackbar Redux (`uiSlice` + `CustomAlert`), que sólo dispara `useCRUDModal` (`useCRUDModal.ts:17,25`), conviven con SweetAlert2 usado directamente en **18 archivos** (`Customers.tsx`, `Leads.tsx`, `Cylinders.tsx`, `Deliveries.tsx`, `Cars.tsx`, `Orders.tsx`, `Claims.tsx`, `Incidents.tsx`, `Envases.tsx`, `Admins.tsx`, `CoverageZones.tsx`, `Reservations.tsx`, `TimeSlotsManager.tsx`, `AssignDriverModal.tsx`, `CylinderDetails.tsx`, `DeliveryDetails.tsx`, `CarsManager.tsx`, `LeadsDetailsView.tsx`, más `store/auth/thunks.ts`).
2. **Dos formas de mutar la misma entidad**: `Customers.tsx` toma el `deleteMutation` de `useCRUDModal` (`:20-23`) pero define su propio `useMutation` para alta/edición (`:25-71`); idéntico patrón en `Deliveries.tsx:26-29` vs `:31-88` y en `Leads.tsx`. El borrado notifica por snackbar Redux y el alta por Swal, en la misma pantalla.
3. **Dos formas de leer listados**: el hook `useTable` (`src/hooks/useTable.ts`), usado por las 6 tablas que montan `CustomTable`, conviven con `useQuery` directo en 10 pantallas (`Claims`, `Incidents`, `Envases`, `Reservations`, `Reports`, `Ratings`, `Distributors`, `Admins`, `CoverageZones`, `CustomerDetails`) y con `useEffect` + `useState` manual en `FleetStatus.tsx:19-48`, `CarsManager.tsx:38-52`, `CylinderDetails.tsx:27-45`, `DeliveryDetails.tsx:26-38`, `LeadsDetailsView.tsx:43-57`.
4. **Dos formas de llegar al backend**: la capa `services/api/*` conviven con una llamada axios directa desde una pantalla, `CylinderDetails.tsx:3,31`.

---

### TABLA 3 — Capa de datos (`src/services/api/`)

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

#### Resumen Tabla 3
- Archivos: **20**. Funciones exportadas de acceso a datos: **64**. Endpoints distintos citados: **~52**.
- `publicAxiosInstance` se usa en **un solo** punto (`auth.ts:5`, `POST /users/validate`); las otras 63 funciones usan `privateAxiosInstance`.
- Sólo **5** funciones de servicio tienen `try/catch`, todas en listados paginados, y todas re-lanzan. El resto propaga.
- `baseURL` = `import.meta.env.VITE_APP_API_URL` (`axiosConfig.ts:11`). Hay `.env` en la raíz del repo.

---

### TABLA 4 — Tipado

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

#### `as any` — ubicaciones exactas
- `src/pages/Orders/components/OrderDetailsModal.tsx`: `:69`, `:73` (×2), `:99`, `:102`, `:104`, `:115`, `:118`, `:123` (×2), `:143` (×2), `:150` (×2), `:158`–`:161` (×4), `:168` (×2), `:178` (×2), `:185`, `:196`, `:199`, `:219`, `:252`, `:261`
- `src/pages/Orders/components/OrdersTable.tsx`: `:119`, `:129`, `:150`, `:188`
- `src/pages/Customers/components/CustomerModal.tsx`: `:238`, `:273`
- `src/pages/Deilverys/components/DeliveryModal.tsx`: `:285`, `:320`

#### `: any` — listado completo (97)
`AuthLayout.tsx:8` · `UploadFileInput.tsx:13` · `CustomAlert.tsx:14` · `SideMenu.tsx:32` · `TableLoadingOrNoData.tsx:20` · `CustomTable.tsx:15,18,46` · `firebase/providers.ts:22` · `useTable.ts:6,7` · `UseForm.ts:11` (×2) · `Customers.tsx:26,57,73` · `CustomerModal.tsx:15,70,71` · `CustomerDetails.tsx:39,159,233,247` · `SalesStats.tsx:26` · `RecentOrdersWidget.tsx:27,84` · `CustomersTable.tsx:18,39,149` · `FleetStatus.tsx:42` · `DashboardStats.tsx:54` · `TimeSlotsManager.tsx:82` · `LoginPage.tsx:19` · `Leads.tsx:10,20,47,78,118,182` · `UserModal.tsx:6,9,50` · `LeadsTable.tsx:18,39,129` · `LeadsDetailsView.tsx:49` · `Admins.tsx:34` · `CreateAdminModal.tsx:174` · `Cars.tsx:16,61` · `CarsTable.tsx:16,45,93,132` · `Orders.tsx:45` · `AssignDriverModal.tsx:32,63` · `Envases.tsx:56,76` · `OrderDetailsModal.tsx:17,24,219` · `CreateEnvaseModal.tsx:101` · `OrdersTable.tsx:41,225` · `Cylinders.tsx:31,50,70,179` · `PromotionsManager.tsx:13,14,34` · `CylinderDetails.tsx:58` · `Claims.tsx:59` · `CylindersTable.tsx:17,30,151` · `CylinderModal.tsx:11` · `Deliveries.tsx:32,65,90` · `Reports.tsx:320,367` · `ResolveClaimModal.tsx:42` · `CarsManager.tsx:70,95` · `DeliveryModal.tsx:17,82,83,196` · `DeliveriesTable.tsx:19,40,164` · `CarModal.tsx:12,177` · `services/api/deliveries.ts:40` · `services/api/cylinders.ts:14` · `services/api/customers.ts:29,64` · `services/api/users.ts:25,81,96` · `services/api/auth.ts:25` · `store/auth/thunks.ts:89`

#### Patrones de tipado repetidos
- **Contrato de eventos de tabla sin tipar**: `setAction: (event: any) => void` / `setLead` / `setLocalAction` aparece en 5 tablas (`CustomersTable.tsx:18`, `LeadsTable.tsx:18`, `CarsTable.tsx:16`, `DeliveriesTable.tsx:19`, `CylindersTable.tsx:17`) y su consumidor lo desestructura también como `any` (`Customers.tsx:73`, `Cars.tsx:61`, `Deliveries.tsx:90`, `Cylinders.tsx:70`, `Leads.tsx:78`).
- **`onSave: (data: any) => void`** en 5 modales: `CustomerModal.tsx:15`, `UserModal.tsx:9`, `CylinderModal.tsx:11`, `DeliveryModal.tsx:17`, `CarModal.tsx:12`.
- **`getRowId={(row: any) => ...}`** en las 5 tablas: `CustomersTable.tsx:149`, `LeadsTable.tsx:129`, `CarsTable.tsx:132`, `CylindersTable.tsx:151`, `DeliveriesTable.tsx:164`, `OrdersTable.tsx:225`.
- **Interface duplicada**: `export interface Delivery` está declarada **dos veces** en el mismo archivo, `src/interfaces/index.ts:56` y `src/interfaces/index.ts:95`, con campos distintos (`id?: string` vs `delivery_id: string`, `cars?: Car[]` sólo en la segunda). TypeScript las fusiona en una sola declaración.
- **Comentarios que documentan desajuste de contrato**: `services/api/orders.ts:13` (`Ojo: Tu DTO dice 'id' pero tu entidad 'order_id'`), `interfaces/index.ts:45` (`OJO: Tu backend usa string "true" / "false", no boolean`), `interfaces/index.ts:57` (`A veces el ID está en user_id, depende de tu entidad TypeORM`).

---

### TABLA 5 — Manejo de errores en la interfaz

#### Mecanismos disponibles
| mecanismo | dónde se define | dónde se consume |
|---|---|---|
| SweetAlert2 (`Swal.fire`) | dependencia directa | **18 archivos de `src/pages` + `src/store/auth/thunks.ts`** |
| Snackbar MUI vía Redux (`uiSlice` → `CustomAlert`) | `src/store/ui/uiSlice.ts`, `src/common/components/CustomAlert.tsx`, montado en `src/App.tsx:32` | Sólo lo dispara `src/hooks/useCRUDModal.ts:17,25` (usado por `Customers.tsx:20`, `Deliveries.tsx:26`, `Leads.tsx`) |
| Banner inline | — | Único caso: `src/pages/Distributors/Distributors.tsx:137-141` (`{createMut.isError && ...}`) |
| Toast Swal (`Swal.mixin`) | — | `src/pages/Deilverys/components/DeliveryDetails.tsx:55` |
| Estado de error de tabla | `src/hooks/useTable.ts:21,61` devuelve `isError` | **Nadie lo consume.** `CustomTable.tsx` sólo distingue `isLoading` y `rows.length === 0` (`:65-68`); si la query falla, la tabla muestra "No hay datos para mostrar." (`TableLoadingOrNoData.tsx:29`) |

#### `catch` vacíos o que sólo loguean
Se auditaron los **25 bloques `catch`** del repo:
- **Vacío literal: 0.**
- **Sólo `console.error`, sin feedback al usuario: 2**
  - `src/pages/Deilverys/components/CarsManager.tsx:46` → `console.error('Error cargando autos:', error);`
  - `src/pages/Home/views/FleetStatus.tsx:45` → `console.error('Error cargando flota:', error);`
- **`console.error` + `throw` (capa de servicio, sin UI): 5** — `services/api/auth.ts:25`, `services/api/customers.ts:29`, `services/api/cylinders.ts:14`, `services/api/deliveries.ts:27`, `services/api/users.ts:25`
- El resto (18) muestra `Swal.fire` al usuario.
- Falso positivo descartado: el `catch` de `src/store/auth/thunks.ts:41` está dentro de un bloque comentado (`:36-45`).

#### `console.*` en producción — 16 archivos, 24 llamadas
`services/api/users.ts` (8: `:16,26,77,79,82,92,94,97`), `services/api/customers.ts:30`, `services/api/cylinders.ts:15`, `services/api/deliveries.ts:28`, `services/api/auth.ts:26`, `store/auth/thunks.ts:50`, `hooks/useCheckAuth.ts:38`, `hooks/useSocket.ts:49`, `common/components/UploadFileInput.tsx`, `pages/Home/views/FleetStatus.tsx:45`, `pages/Leads/Leads.tsx:183`, `pages/Leads/components/LeadsDetailsView.tsx:71`, `pages/Gascilinders/Cylinders.tsx:51,180`, `pages/Gascilinders/components/CylinderDetails.tsx:36`, `pages/Deilverys/components/DeliveryDetails.tsx:33`, `pages/Deilverys/components/CarsManager.tsx:46`.

#### Pantallas cuyas llamadas NO tienen manejo de error
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

### TABLA 6 — Código muerto y restos

#### 6.a — Archivos de 0 bytes
| archivo |
|---|
| `src/pages/Cars/components/CarsDetails.tsx` (0 bytes) |
| `src/pages/Cars/components/CarsModal.tsx` (0 bytes) |
| `src/pages/Cars/components/index.ts` (0 bytes) |
| `src/pages/Configuration/index.ts` (0 bytes) |
| `src/pages/Configuration/components/index.ts` (0 bytes) |

#### 6.b — Archivos no alcanzables desde el entrypoint
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

#### 6.c — Exports sin ningún importador externo (31 de 221)
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

#### 6.d — Bloques comentados de más de 5 líneas
| ubicación | líneas comentadas | contenido |
|---|---|---|
| `src/App.tsx:23-33` | 11 | `<BrowserRouter>` + `<Routes>` viejos, más los imports comentados en `:1`, `:6`, `:7` |
| `src/store/auth/thunks.ts:36-45` | 10 | `startCreatingUserWithEmailPassword` completo, comentado; más los imports comentados de `:10-14` |
| `src/common/components/Navbar/components/SideDrawer.tsx:89-113` | 25 | bloque JSX `<Tooltip title='Logout'>` completo (archivo además no alcanzable) |
| `src/common/components/LogoSplg.tsx:6-11` | 6 | JSDoc (documentación legítima, no código muerto) |
| `src/hooks/useSocket.ts:82-88` | 7 | comentario explicativo del cleanup (legítimo) |
| `src/pages/Distributors/Distributors.tsx:13-18` | 6 | JSDoc (legítimo) |
| `src/pages/Leads/components/LeadsDetailsView.tsx:64-70` | 7 | lógica de bloqueo futura comentada + variable `action` comentada |

#### 6.e — Marcas TODO / NUEVO / "Pendiente" / "Agregado"
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

### TABLA 7 — Tiempo real

#### `src/hooks/useSocket.ts` (100 líneas)
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

#### `src/context/SocketContext.tsx` (59 líneas)
| aspecto | hecho |
|---|---|
| Namespace | `/admin` (`:20`) |
| Contexto | `SocketContextValue { isOnline, subscribe }` (`:5-11`); `createContext<... | undefined>(undefined)` (`:13`) |
| Cuándo conecta | `useEffect` (`:28-42`): si `status !== 'authenticated'` o no hay `uid` → `disconnect()` y sale (`:29-32`); si no, lee `localStorage.getItem('token')` y llama `connect({ token, uid, role })` (`:37-39`) |
| Cuándo desconecta | Cleanup del efecto: `return () => disconnect()` (`:41`) — es decir, también al cambiar `status`, `uid` o `role` |
| Guard | `useSocketContext` lanza `Error('useSocketContext debe usarse dentro de un <SocketProvider>')` si falta el provider (`:52-57`) |
| Montaje | `<SocketProvider>` envuelve `<Navigation />` y `<CustomAlert />` en `src/App.tsx:21-34` |
| Limitación anotada | `TODO` en `:36`: el ID token dura 1 h y no se refresca con `getIdToken()` |

#### Consumidores
| pantalla / componente | archivo:línea | eventos a los que se suscribe |
|---|---|---|
| Campana de notificaciones (visible en todo el dashboard vía `Navbar` → `DashboardLayout`) | `src/common/components/Navbar/components/NotificationBell.tsx:57`, suscripción en `:77-87` | Los **5** de `ORDER_SOCKET_EVENTS` (`Object.values(...)`, `:79`). Acumula hasta `MAX_NOTIFICATIONS = 50` (`:45`, `:71`). Se dan de baja todos en el cleanup (`:86`) |
| `tracking` | `src/pages/Tracking/Tracking.tsx:14`, suscripción en `:39-45` | **`order:driver-location`** (`:11`) — evento que **no** está en `ORDER_SOCKET_EVENTS`, está hardcodeado en la pantalla. Un `Map<orderId, TrackedOrder>` que se actualiza por pedido (`:24-37`); centra el mapa sólo la primera vez (`:33-36`) |

**Total de consumidores del socket: 2.** Ninguna otra pantalla (ni `Orders`, ni `Home`, ni `Claims`) invalida su caché de React Query al llegar un evento: las notificaciones son sólo visuales.

---

### TABLA 8 — Duplicación (bloques de 10+ líneas casi idénticos, comparación normalizada por espacios y sin comentarios)

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

### Anexo — otros hechos verificables

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

---

## Parte III — La aplicación del cliente

Repositorio: `/Users/nahuelwagner/Desktop/myprojects/gearthlogic/projects/garrafitas/splg-app-cliente`
Rama: `develop` — último commit `5793d87 ci: la version se calcula sola en cada merge a main`
Paquete: `splg_customer` (`pubspec.yaml:1`), SDK Dart `>=3.0.3 <4.0.0`
Volumen: 98 archivos `.dart` en `lib/`, 10.922 líneas.

Todo dato de abajo está verificado abriendo el archivo indicado. Este informe no modificó ningún archivo del repositorio.

---

### TABLA 1 — Pantallas (`lib/ui/views/`)

Criterio de esqueleto aplicado: menos de 60 líneas en la vista, o sólo un `Scaffold` con texto, o TODO sin implementar.

| Pantalla | Archivo | Líneas | ¿Viewmodel? | Qué hace | ¿Completa o esqueleto? |
|---|---|---|---|---|---|
| Startup (splash) | `lib/ui/views/startup/startup_view.dart` | 54 | Sí — `startup_viewmodel.dart` (57) | Logo + "Cargando ..." + spinner (`startup_view.dart:22-40`); en `onViewModelReady` dispara `runStartupLogic()` (`startup_view.dart:52-53`), que rehidrata el customer con reintento en loop (`startup_viewmodel.dart:21-47`), inicializa notificaciones (`:53`) y hace `replaceWithHomeView()` (`:55`) | **<60 líneas** por el criterio, pero funcional: tiene lógica real en el VM |
| Home (contenedor de tabs) | `lib/ui/views/home/home_view.dart` | 60 | Sí — `home_viewmodel.dart` (13) | `IndexedStack` con `History`, `Order`, `Account` (`home_view.dart:20-28`) + `BottomNavigationBar` de 3 ítems (`:31-53`); el VM sólo guarda el índice, arranca en 1 (`home_viewmodel.dart:4-12`) | Completa (delega todo en los 3 widgets) |
| Login | `lib/ui/views/login/login_view.dart` | 193 | Sí — `login_viewmodel.dart` (80) + `login_view.form.dart` (206, generado) | Form email/password con `@FormView` (`login_view.dart:10-17`), toggle de visibilidad (`:120-127`), botón a signup (`:154-175`); el VM valida con `EmailValidator`, llama `signInWithEmailAndPassword`, registra el token FCM y hace `back()` (`login_viewmodel.dart:26-48`) | Completa |
| Signup | `lib/ui/views/signup/signup_view.dart` | 243 | Sí — `signup_viewmodel.dart` (138) + `signup_view.form.dart` (268, generado) | 4 campos vía widget `TextInput` (`signup_view.dart:75,86,98,119`), links a Términos y Privacidad (`:187,:194`); el VM valida, normaliza el teléfono a `+54…` (`signup_viewmodel.dart:71-84`), registra, loguea y `clearStackAndShow(Routes.homeView)` (`:55-60`) | Completa |
| Checkout | `lib/ui/views/checkout/checkout_view.dart` | 346 (+3 widgets: `cylinder_checkout_item.dart` 118, `payment_method_selector.dart` 78, `time_range_selector.dart` 111) | Sí — `checkout_viewmodel.dart` (366) | Lista de ítems con subtotal y descuento (`checkout_view.dart:62-77`), total (`:97`), selector de método de pago (`:112`), fecha (`:126`), franjas horarias (`:254-289`), notas (`:186`), dirección por mapa o bottom sheet (`:310-325`), botón confirmar (`:222`). El VM calcula descuentos y recargo del 10% online (`checkout_viewmodel.dart:124-178`), crea o edita el pedido y abre el WebView de MercadoPago (`:212-322`) | Completa |
| Map (elegir ubicación) | `lib/ui/views/map/map_view.dart` | 128 | Sí — `map_viewmodel.dart` (86) | `GoogleMap` con pin fijo al centro (`map_view.dart:21-41`), panel inferior con la dirección geocodificada y "Confirmar Ubicación" (`:42-112`); el VM geolocaliza, hace reverse geocoding en `onCameraIdle` y devuelve un `Address` por `back(result:)` (`map_viewmodel.dart:30-85`) | Completa |
| Addresses (mis direcciones) | `lib/ui/views/addresses/addresses_view.dart` | 223 | Sí — `addresses_viewmodel.dart` (49) | Lista de direcciones con badge "Predeterminada", marcar predeterminada y borrar con confirmación (`addresses_view.dart:93-118`, `:131-223`), FAB "Agregar" que abre el mapa (`:36-40`); el VM refresca contra backend y llama a `CustomerService` (`addresses_viewmodel.dart:18-48`) | Completa |
| Profile | `lib/ui/views/profile/profile_view.dart` | 337 | Sí — `profile_viewmodel.dart` (109) | Editar nombre y teléfono con diálogo + SnackBar de resultado (`profile_view.dart:175-212`), email de sólo lectura (`:80`), dirección predeterminada con acceso a Addresses (`:86-87`), links legales (`:103,:108`), cerrar sesión (`:123`) y "Borrar cuenta" (`:142`) | Completa, con una salvedad verificable: `deleteAccount()` sólo hace `signOut()` + navegar a login (`profile_viewmodel.dart:104-107`); no llama a ningún endpoint de borrado |
| Order tracking | `lib/ui/views/order_tracking/order_tracking_view.dart` | 484 | Sí — `order_tracking_viewmodel.dart` (829, el archivo más grande del repo después del router generado) | Mapa con marcadores cliente/chofer, polilínea y radar (`order_tracking_view.dart:38-45`), stepper de 4 pasos (`:149`), tarjeta del chofer con llamar/WhatsApp (`:347-458`), botón de confirmar entrega por QR (`:190-195`), cancelar pedido (`:238-243`), detalle expandible (`:205-227`) | Completa |
| QR scan (confirmar entrega) | `lib/ui/views/qr_scan/qr_scan_view.dart` | 158 | Sí — `qr_scan_viewmodel.dart` (108) | Cámara `MobileScanner` con overlay y manejo de permiso denegado (`qr_scan_view.dart:43-50`, `:119-157`); el VM manda el código a `confirm-delivery` con diálogos de éxito/código inválido/red (`qr_scan_viewmodel.dart:37-93`) | Completa. Tiene un `TODO` documentado en `qr_scan_viewmodel.dart:32-36` sobre no distinguir "código de otro pedido" de "código mal leído" |
| Legal (T&C / Privacidad) | `lib/ui/views/legal/legal_view.dart` | 100 | Sí — `legal_viewmodel.dart` (32) | Renderiza el markdown de `legal/terminos-y-condiciones.md` o `legal/politica-de-privacidad.md` según el enum `LegalDocument` (`legal_view.dart:8-22`, `:78-86`), con estados de carga y error (`:61-76`) | Completa |
| Payment WebView (MercadoPago) | `lib/ui/views/payment_webview/payment_webview_view.dart` | 52 | Sí — `payment_webview_viewmodel.dart` (84) | `WebViewWidget` + spinner (`payment_webview_view.dart:32-34`); el VM carga el `init_point`, intercepta las back_urls de MP y cierra devolviendo `PaymentOutcome` (`payment_webview_viewmodel.dart:32-83`) | **<60 líneas** por el criterio, pero funcional: la lógica está en el VM |

**Totales:** 12 pantallas registradas como rutas (`lib/app/app.dart:34-45`, `lib/app/app.router.dart:29-52`). Las 12 tienen viewmodel propio. Ninguna es un `Scaffold` con texto y nada más; las dos que caen bajo el umbral de 60 líneas (`startup_view.dart` 54, `payment_webview_view.dart` 52) son vistas delgadas con VM de lógica real.

**Esqueleto real fuera de `views/`:** `lib/ui/widgets/common/market/market.dart:15` devuelve `const SizedBox.shrink()` y su modelo `lib/ui/widgets/common/market/market_model.dart:3` es `class MarketModel extends BaseViewModel {}` — vacío. Ver TABLA 7.

**Botones sin acción:** en `lib/ui/widgets/common/account/account.dart` las opciones "Notificaciones" (`:42`), "Privacidad" (`:49`) y "Ayuda" (`:56`) tienen `onTap: () {}`.

---

### TABLA 2 — Arquitectura

#### Patrón

**MVVM sobre el framework Stacked**, con una capa Clean parcial (`domain/repository` + `domain/usecases` + `data/repository` + `data/datasource`) que sólo cubre una parte de los flujos.

- Stacked es la base: `pubspec.yaml:11-12` (`stacked ^3.4.0`, `stacked_services ^1.1.0`), configuración en `stacked.json`, y el árbol declarativo en `lib/app/app.dart:32-75` (`@StackedApp` con `routes`, `dependencies`, `bottomsheets`, `dialogs`).
- Código generado por `stacked_generator`: `lib/app/app.locator.dart` (50), `lib/app/app.router.dart` (912), `lib/app/app.bottomsheets.dart` (38), `lib/app/app.dialogs.dart` (26), más los `*_view.form.dart` de login y signup.
- Cada vista es un `StackedView<TViewModel>` y cada VM extiende `BaseViewModel`, `ReactiveViewModel` o `FormViewModel`.

#### Qué hay en cada capa

| Capa | Contenido | Archivos |
|---|---|---|
| `lib/app/` | Wiring generado: locator, router, registro de sheets y dialogs | 5 archivos, 1.102 líneas (el 10% del repo es router generado) |
| `lib/core/` | `AppConfig` (config por `--dart-define`) y `ApiClient` (singleton Dio con headers y timeouts) | `core/config/app_config.dart` (44), `core/network/api_client.dart` (148) |
| `lib/data/datasource/` | 8 clases que hablan HTTP contra `ApiClient` y devuelven `bool` / `(bool, dynamic)` / `List<Map>` | ver TABLA 4 |
| `lib/data/repository/` | 4 implementaciones que mapean el crudo a modelos de `splg_lib` | `address_repository_imp.dart` (15), `customer_repository_imp.dart` (43), `gascylinder_repository_imp.dart` (29), `order_repository_imp.dart` (111) |
| `lib/data/mappers/` | `OrderApiMapper`: normaliza la respuesta de pedidos (tolera `order`/`data`/`result` anidados y snake/camel) y extrae `paymentUrl` | `order_api_mapper.dart` (267), `extractPaymentUrl` en `:238-253` |
| `lib/domain/repository/` | 4 interfaces `abstract interface class` | `address_repository.dart` (5), `customer_repository.dart` (6), `gascylinder_repository.dart` (5), `order_repository.dart` (28) |
| `lib/domain/usecases/` | 7 use cases, todos de una línea: delegan al repositorio | `create_address_usecases.dart` … `update_order_status_usecases.dart` |
| `lib/domain/` (modelos) | `CreateOrderResult` (19), `PaymentOutcome` (19), `TimeSlotAvailability` (41), `BusinessHours` (66) | los modelos de dominio "grandes" (`Order`, `Customer`, `Address`, `GasCylinder`, `Discount`, `OrderItem`) viven en el paquete externo `splg_lib` (`pubspec.yaml:41-42`, `path: ../splg-lib`) |
| `lib/services/` | 10 singletons registrados en el locator: estado de app + orquestación de casos de uso | `cart_service.dart` (35), `claim_service.dart` (30), `customer_service.dart` (248), `gas_cylinder_service.dart` (28), `history_service.dart` (231), `location_service.dart` (43), `notification_service.dart` (147), `order_tracking_service.dart` (260), `rating_service.dart` (26), `time_slot_service.dart` (18) |
| `lib/ui/` | 12 vistas + 12 viewmodels, 4 widgets "common" con su propio modelo, 4 bottom sheets, 1 dialog, 3 archivos `common/` (colores, strings, helpers) | |

#### Cómo se relacionan

El camino "canónico" que sí existe es:

```
View (StackedView) → ViewModel → Service (locator) → UseCase → Repository (interface)
  → RepositoryImp → RemoteDatasource → ApiClient (Dio) → backend
```

Verificado punta a punta en dos flujos:
- Pedidos: `checkout_viewmodel.dart:267` → `history_service.dart:59` (`_createOrderUseCase`) → `create_order_usecases.dart:13` → `order_repository_imp.dart:15-43` → `order_remote_datasource.dart:8-22` → `api_client.dart:52`.
- Garrafas: `order_model.dart:36` → `gas_cylinder_service.dart:21` → `fetch_gascylinders_usecases.dart:9` → `gascylinder_repository_imp.dart:13` → `gascylinder_remote_datasource.dart:8`.

#### Dónde NO se respeta la separación

Ninguna **vista** ni **viewmodel** llama a un datasource ni a `ApiClient`: el grep sobre `lib/ui` no devuelve imports de `data/datasource`, `data/repository` ni `core/network`. La única fuga hacia `ui/` es un mapper: `order_tracking_viewmodel.dart:11` importa `data/mappers/order_api_mapper.dart` y lo usa en `:401` para parsear el crudo del backend dentro del VM.

Los saltos reales están en la capa de servicios:

1. **5 servicios instancian el datasource directamente, sin repositorio ni use case:**
   - `rating_service.dart:7` → `RatingRemoteDatasource()`
   - `claim_service.dart:8` → `ClaimRemoteDatasource()`
   - `time_slot_service.dart:10` → `TimeSlotRemoteDatasource()`
   - `notification_service.dart:25` → `NotificationRemoteDatasource()`
   - `customer_service.dart:40` → `CustomerRemoteDatasource()` (usado directo en `updateProfile`, `:142`)
   Para rating, claim, time-slot y notificaciones **no existe** repositorio ni interfaz en `domain/`.

2. **`OrderTrackingService` saltea toda la capa `data/`:** usa `ApiClient` directo (`order_tracking_service.dart:5,32`) para `GET orders/:id` (`:53`) y `POST orders/:id/confirm-delivery` (`:79-84`). Es el único lugar del repo que inspecciona el status HTTP de una `DioException` (`:91-96`).

3. **`CustomerService` mezcla dos caminos para direcciones:** el "clean" (`AddressRepositoryImp` + `CreateAddressUsecases`, `:234-237`) y el directo (`AddressRemoteDataSource()` instanciado inline cinco veces: `:162, :175, :188, :201, :210`). Además instancia `AddressRemoteDataSource()` nuevo en cada llamada en vez de tener un campo.

4. **`HistoryService.updateOrder` saltea el use case:** llama `_orderRepository.updateOrder(...)` directo (`history_service.dart:90`), a diferencia de create/fetch/cancel que sí pasan por su use case. No existe `UpdateOrderUseCase`.

5. **La capa `usecases` no agrega comportamiento:** los 7 archivos son un `call()` de una línea que reenvía al repositorio (p. ej. `create_order_usecases.dart:9-13`, `fetch_customer_usecases.dart:9-10`).

6. **`CustomerService` mantiene un customer mock hardcodeado** como valor inicial: `customer_service.dart:240-247` (`customerId: '1234'`, `'Demo user'`, `demo@email.com`). Si `init()`/`fetchCustomerByEmail` fallan, ese `customerId: '1234'` es el que se manda al backend.

---

### TABLA 3 — Estado y navegación

| Aspecto | Qué usa | Evidencia |
|---|---|---|
| Gestor de estado | **Stacked** (MVVM con `provider` por debajo). No hay Riverpod, Bloc ni GetX en `pubspec.yaml` | `pubspec.yaml:11-12`; `StackedView` + `BaseViewModel` en las 12 vistas |
| Estado local de pantalla | `BaseViewModel` + `rebuildUi()` / `notifyListeners()` / `setBusy()` | `home_viewmodel.dart:11`, `login_viewmodel.dart:78`, `checkout_viewmodel.dart:98` |
| Estado compartido | Servicios singleton registrados como `LazySingleton` en el locator, expuestos con `ListenableServiceMixin` + `ReactiveValue` / `ReactiveList` | `app.locator.dart:37-49`; `cart_service.dart:5-13`; `history_service.dart:17,34,37` |
| Reactividad vista↔servicio | `ReactiveViewModel` con `listenableServices` | `checkout_viewmodel.dart:364-365` (`[_cartService]`), `order_model.dart:172-176` (`[_cartService, _historyService]`), `history_model.dart:104-105` (`[_historyService]`) |
| `setState` | **No se usa en ninguna parte de `lib/`** (no hay `StatefulWidget` propio; el grep de `setState(` no devuelve resultados) | |
| Sesión / auth | `FirebaseAuth.instance` dentro de `CustomerService`; el ID token se pide en cada request (`await _firebaseAuth.currentUser?.getIdToken()`) | `customer_service.dart:22-38` |
| Carrito | `CartService` con `ReactiveValue<Order?>` + `editingOrderId` para distinguir alta de edición | `cart_service.dart:10-34` |
| Polling | `HistoryModel` refresca el historial cada 10 s con un `Timer.periodic` y evalúa si abrir el tracking | `history_model.dart:107-113`; cancelado en `dispose()` (`:125-129`) |
| Navegación | `NavigationService` de `stacked_services` con rutas generadas; `navigatorKey: StackedService.navigatorKey` en el `MaterialApp` | `main.dart:32-37`; rutas en `app.router.dart:29-52` |
| Ruta inicial | `Routes.startupView` → `replaceWithHomeView()` al terminar el arranque | `main.dart:32`; `startup_viewmodel.dart:55` |
| Patrones de navegación usados | `navigateToXView()` (push), `replaceWithXView()` (`checkout_viewmodel.dart:283`, `startup_viewmodel.dart:55`), `clearStackAndShow()` (`signup_viewmodel.dart:60`, `profile_viewmodel.dart:90,106`), `back(result: …)` para devolver datos (`map_viewmodel.dart:81`, `qr_scan_viewmodel.dart:77`, `payment_webview_viewmodel.dart:75`) | |
| Paso de argumentos | Tipado por el generador: `orderId` a tracking y QR, `document` a legal, `paymentUrl` al WebView | `order_tracking_view.dart:7`, `qr_scan_view.dart:11-14`, `legal_view.dart:27-29`, `payment_webview_view.dart:10-13` |
| Navegación fuera de la app | `url_launcher` para `tel:` y `wa.me` | `order_tracking_viewmodel.dart:286-287`, `:317-321` |
| Overlays | `DialogService` (`showDialog`, `showConfirmationDialog`) y `BottomSheetService` (`showCustomSheet`) con `BottomSheetType` | `app.dialogs.dart:13-25`, `app.bottomsheets.dart:16-37` |
| Navegación imperativa cruda | `showDialog`/`showModalBottomSheet` de Flutter directo desde la vista, conviviendo con los servicios de Stacked | `addresses_view.dart:98`, `profile_view.dart:175`, `history.dart:126`, `order.dart:217` |

---

### TABLA 4 — Capa de datos (`lib/data/datasource/`)

Todas las llamadas pasan por `ApiClient` (`lib/core/network/api_client.dart`), singleton de Dio con `baseUrl = AppConfig.apiUrl` (= `$API_BASE_URL/api/`), `connectTimeout`/`receiveTimeout` de 10 s (`api_client.dart:17-22`) y `PrettyDioLogger` con `requestHeader: true` y `requestBody: true` siempre activo, incluso en release (`:23-30`). Todos los verbos mandan los headers `X-Client-Source: customer-app` y `X-Distributor: <AppConfig.distributorSlug>` (`:40-41, :66-67, :92-93, :112-113, :136-137`). En `get` y `post` el token es opcional; en `patch`, `delete` y `put` es obligatorio por firma.

| Archivo | Métodos | Endpoints | ¿Manda token? | ¿Maneja errores o los propaga? |
|---|---|---|---|---|
| `address_remote_datasource.dart` (88) | `createAddress` (`:8`), `fetchByUser` (`:28`), `updateAddress` (`:45`), `setDefault` (`:64`), `deleteAddress` (`:79`) | `POST user-address`, `GET user-address/user/:userId`, `PATCH user-address/:id`, `PATCH user-address/:id/set-default`, `DELETE user-address/:id` | Sí, en los 5 | **Los traga.** `catch (e) { log(...) }` y devuelve `false` o `const []` (`:20-24, :38-41, :56-59, :72-75, :83-86`). El llamador no distingue "falló la red" de "el backend dijo que no" |
| `claim_remote_datasource.dart` (22) | `createClaim` (`:10`) | `POST claims` | Sí (`:15`) | Los traga: `log` + `return false` (`:17-20`) |
| `customer_remote_datasource.dart` (53) | `createCustomer` (`:8`), `fetchCustomerByEmail` (`:26`), `updateUser` (`:43`) | `POST users/customer-registration`, `GET users/email/:email`, `PATCH users/:id` | `createCustomer` **no** manda token (registro público, `:11-14`); los otros dos sí | Los traga: `log` + `(false, null)` / `false` (`:19-23, :33-38, :48-51`) |
| `gascylinder_remote_datasource.dart` (21) | `getGasCylinders` (`:8`) | `GET gascylinder` | **No** (endpoint público, `:10`) | Los traga: `log` + `(false, null)` (`:15-19`) |
| `notification_remote_datasource.dart` (34) | `registerToken` (`:12`) | `POST notifications/token` | Sí — `authToken` explícito (`:26`) | Los traga: `log` + `false` (`:29-32`) |
| `order_remote_datasource.dart` (99) | `createOrder` (`:8`), `updateOrder` (`:24`), `fetchCustomerHistory` (`:58`), `updateOrderStatus` (`:80`) | `POST orders`, `PATCH orders/:id` **con fallback a `PUT orders/:id`** (`:42-53`), `GET orders/customer/:id?limit=&offset=`, `PATCH orders/:id/status` | Sí, en los 4 | Los traga: `log` + `(false, null)` / `false`. `updateOrder` hace dos requests: si el PATCH tira o no devuelve 200/204, reintenta con PUT y recién ahí falla (`:30-55`) |
| `rating_remote_datasource.dart` (23) | `createRating` (`:11`) | `POST ratings` | Sí (`:16`) | Los traga: `log` + `false` (`:17-21`) |
| `time_slot_remote_datasource.dart` (28) | `fetchAvailability` (`:12`) | `GET time-slot/availability?date=YYYY-MM-DD&distributor=<slug>` | **No** (endpoint público, `:14-16`) | Los traga: `log` + `const []` (`:23-26`) |

**Fuera de `data/datasource/` pero llamando HTTP:** `lib/services/order_tracking_service.dart` usa `ApiClient` directo para `GET orders/:orderId` (`:53`, token sí) y `POST orders/:orderId/confirm-delivery` con header `Idempotency-Key: uuid v4` por intento (`:79-84`, token sí). Es el **único** punto del repo que distingue tipos de error: mapea `DioException` con status 400 a `ConfirmDeliveryResult.invalidCode` y el resto a `networkError` (`:91-100`).

**Patrón general:** ningún datasource propaga la excepción hacia arriba. Todos la registran con `log()` de `dart:developer` y devuelven un valor "vacío". La información de por qué falló (401 vs 500 vs timeout) se pierde en el borde HTTP y no llega nunca a la UI.

---

### TABLA 5 — Manejo de errores

#### Dónde se le muestra el error al usuario

| Lugar | Mecanismo | Mensaje | Línea |
|---|---|---|---|
| Arranque con sesión rota | `DialogService.showDialog` con Reintentar/Cancelar en loop | "No se pudo iniciar sesión. Por favor, verifica tu conexión…" | `startup_viewmodel.dart:32-38` |
| Login fallido | `showDialog` | "No se pudo iniciar sesión. Por favor, verifique sus credenciales…" | `login_viewmodel.dart:40-44` |
| Validación de login | `errorText` en los `TextFormField` | "Email inválido" / "Contraseña inválida" | `login_viewmodel.dart:50-63`; pintado en `login_view.dart:101,119` |
| Registro fallido | `showDialog` | `signupViewErrorDialogDescription` | `signup_viewmodel.dart:62-65` |
| Validación de signup | `errorText` por campo | 4 mensajes | `signup_viewmodel.dart:86-121`; pintado en `signup_view.dart:80,91,103,124` |
| Checkout sin sesión | `showDialog` + navegar a login | "Iniciá sesión para continuar" | `checkout_viewmodel.dart:216-221` |
| Crear pedido falla | `showDialog` | "Error al crear pedido / No se pudo crear la orden…" | `checkout_viewmodel.dart:287-291` |
| Modificar pedido falla | `showDialog` | "Error al modificar pedido…" | `checkout_viewmodel.dart:256-260` |
| MercadoPago sin `paymentUrl` | `showDialog` | "No se pudo iniciar el pago…" | `checkout_viewmodel.dart:304-312` |
| Resultado del pago | `showDialog` por cada `PaymentOutcome`, incluido `null` | 3 variantes | `checkout_viewmodel.dart:324-355` |
| Cancelar pedido desde historial | `showDialog` | "Error al cancelar pedido…" | `history_model.dart:94-100` |
| Cancelar pedido desde tracking | `showDialog` | "No se pudo cancelar. Intenta nuevamente en unos segundos." | `order_tracking_viewmodel.dart:335-341` |
| Llamar / mensajear al chofer | `showDialog` (sin teléfono, número inválido, no abrió el marcador/WhatsApp) | 5 variantes | `order_tracking_viewmodel.dart:278-293`, `:296-327` |
| Confirmar entrega por QR | `showDialog` diferenciando sesión expirada / código inválido / error de red | 3 variantes | `qr_scan_viewmodel.dart:57-63`, `:81-88` |
| Cámara del QR | `errorBuilder` con pantalla dedicada y botón "Abrir Ajustes" si el permiso está denegado | | `qr_scan_view.dart:46-49`, `:119-157` |
| Documento legal que no carga | Texto en el cuerpo de la pantalla | "No pudimos cargar este documento…" | `legal_view.dart:65-76` |
| Editar nombre/teléfono en perfil | `SnackBar` | "Datos actualizados." / "No se pudo actualizar." | `profile_view.dart:206-212` |
| Reclamo | Texto rojo dentro del sheet | "No se pudo enviar el reclamo. Intentá de nuevo." / "Contanos qué pasó antes de enviar." | `claim_sheet_model.dart:37,52`; pintado en `claim_sheet.dart:90-95` |
| Calificación del chofer | Texto dentro del sheet | "Elegí una puntuación de 1 a 5." / "No se pudo enviar la calificación…" | `rate_driver_sheet_model.dart:27,41`; pintado en `rate_driver_sheet.dart:92-95` |

#### `catch` vacíos, silenciosos o sólo con log

- **No hay ni un `print(`** en todo `lib/` (grep sin resultados). El logging es `log()` de `dart:developer`.
- **`catch` con el cuerpo vacío — 1 caso, y es el peor:** `map_viewmodel.dart:35-37`. Si falla la geolocalización, el `catch` está vacío y arriba, en `:14` y `:36`, quedan comentados el `_snackbarService` y su `showSnackbar('Error al obtener la ubicación.')`. El usuario ve el mapa centrado en el fallback de Buenos Aires (`map_view.dart:24`) sin ningún aviso de que no se pudo ubicar.
- **`catch (_)` que devuelven null/flag, sin avisar:** `profile_viewmodel.dart:28-30` (no hay dirección primaria), `order_api_mapper.dart:10-12` y `:22-24` (un pedido que no parsea se descarta en silencio: `continue`), `legal_viewmodel.dart:27-29` (este sí se refleja en la UI).
- **`catch` con sólo `log()` — 22 ocurrencias**, en los 8 datasources (ver TABLA 4), en los 4 repositorios (`customer_repository_imp.dart:21-23,37-39`, `gascylinder_repository_imp.dart:23-25`, `order_repository_imp.dart:38-40,66-68,90-92,105-107`), en `location_service.dart:38-40`, en `customer_service.dart:35`, `:108`, y en los 6 `catch` de `notification_service.dart` (`:40-42, :56-58, :67-70, :76-78, :88-90, :117-119`).
- **`api_client.dart` tiene cinco `try { … } catch (e) { rethrow; }`** (`:47-49, :74-76, :99-101, :119-121, :144-146`): son no-ops, no agregan nada sobre no escribir el try.

#### Flujos sin ningún manejo de error visible para el usuario

| Flujo | Qué pasa | Evidencia |
|---|---|---|
| **Geolocalización en el mapa** | `catch` vacío; el snackbar está comentado; se muestra el fallback de CABA sin aviso | `map_viewmodel.dart:35-37`; fallback en `map_view.dart:23-24` |
| **Gestión de direcciones (Addresses)** | El VM sí construye los mensajes de error ("No se pudo guardar la dirección.", "No se pudo marcar como predeterminada.", "No se pudo eliminar la dirección.") en `actionError`, pero **`addresses_view.dart` nunca lee `actionError`**: el grep sólo lo encuentra en el viewmodel. Los 3 errores son invisibles | `addresses_viewmodel.dart:16,31,39,46` vs. `addresses_view.dart` (223 líneas, sin una sola referencia) |
| **Alta de dirección desde el checkout** | `CustomerService.addAddress` es optimista y fire-and-forget: inserta la dirección local y dispara `_submitAddress` sin esperar ni chequear el resultado. El propio código lo dice en `:224` ("This not check if the address was created successfully") | `customer_service.dart:215-238`; llamado en `checkout_viewmodel.dart:56` |
| **Carga del catálogo de garrafas** | Si el `GET gascylinder` falla, el repositorio devuelve `[]` y la pantalla de pedido muestra una lista vacía sin mensaje ni reintento | `gascylinder_repository_imp.dart:23-27` → `order.dart:52-65` |
| **Carga del historial de pedidos** | Si falla, `refreshHistory` deja `_history` vacío y la vista muestra el estado "sin pedidos" (indistinguible de "no tenés pedidos") | `history_service.dart:131-157`; `history.dart:38` |
| **Franjas horarias del checkout** | Si el endpoint falla, `fetchAvailability` devuelve `const []` y el checkout muestra la sección vacía; sin franja no se puede confirmar (`canConfirmOrder` exige `_selectedTimeSlotId != null`) pero no se explica por qué | `time_slot_remote_datasource.dart:23-26` → `time_slot_service.dart:15` → `checkout_view.dart:254-289`; `checkout_viewmodel.dart:180-185` |
| **Carga de los datos del tracking** | Si no hay token o `fetchOrderById` devuelve null, `_loadTrackingData` hace `return` sin avisar: la pantalla queda con los valores por defecto ("Repartidor", "Vehiculo sin datos", "--", "Calculando llegada...") como si el pedido estuviera bien cargado | `order_tracking_viewmodel.dart:390-399`; defaults en `:51-56` |
| **Socket de tiempo real** | `onError` y `onDisconnect` sólo hacen `log()`; la UI no muestra "sin conexión en vivo" ni nada equivalente | `order_tracking_service.dart:142-143` |
| **Registro del token FCM** | Todo el flujo está envuelto en `try/catch` con `log()`; si nunca se registra, el usuario no se entera de que no va a recibir push | `notification_service.dart:34-43`, `:49-59`, `:104-120` |
| **Actualización del perfil** | El SnackBar dice "No se pudo actualizar." sin distinguir validación, permisos o red, porque esa información se perdió en el datasource | `profile_view.dart:206-212` ← `customer_service.dart:129-154` ← `customer_remote_datasource.dart:43-52` |
| **Sesión expirada en medio de la app** | `CustomerService.token` devuelve `null` y cada servicio hace `return false` / `return` temprano; sólo el flujo de QR muestra un diálogo de "Sesion expirada" (`qr_scan_viewmodel.dart:58-61`). En `history_service.dart:54-56, 86-88, 109-111, 136-141`, `claim_service.dart:19`, `rating_service.dart:18` y `customer_service.dart:131,160,174,187,200,209` el `null` se traduce a un fallo mudo | |
| **Borrar cuenta** | El diálogo dice "Esta acción no se puede deshacer", pero sólo se hace `signOut()` y se navega a login; no hay llamada al backend ni manejo de error porque no hay request | `profile_viewmodel.dart:94-108` |

---

### TABLA 6 — Tiempo real (`lib/services/order_tracking_service.dart`, 260 líneas)

| Aspecto | Hecho verificado |
|---|---|
| Transporte | `socket_io_client ^3.1.2` (`pubspec.yaml:19-20`), importado como `io` en `:6` |
| URL del socket | **Hardcodeada:** `static const String _socketBaseUrl = 'http://localhost:3000/customers'` (`:30`). No usa `AppConfig`, así que **no se puede cambiar por `--dart-define`**. Tiene el `TODO(config)` en `:29` y el comentario de `:27-28` aclara que en emulador Android hay que usar `10.0.2.2` |
| Namespace | `/customers` (el `CustomersGateway` del backend, `:27`) |
| Autenticación del handshake | Manda el token de Firebase por duplicado: `setAuth({'token': token})` y `setExtraHeaders({'Authorization': 'Bearer $token'})` (`:120-123`) |
| Sala | En `onConnect` emite `customer:join` con `{'customerId': customerId}` (`:127-131`) |
| **Eventos a los que se suscribe** | `order:driver-location` → `_onDriverLocationUpdate` (`:134`)<br>`order:accepted` → `_onOrderStatusUpdate` (`:137`)<br>`order:on-the-way` (`:138`)<br>`order:delivered` (`:139`)<br>`order:cancelled` (`:140`)<br>Más los meta-handlers `onError` y `onDisconnect`, que sólo loguean (`:142-143`) |
| Eventos que emite | Sólo `customer:join` (`:130`) |
| Salidas | Dos `StreamController.broadcast`: `driverLocationUpdates` (`Stream<DriverLocationUpdate>`) y `orderStatusUpdates` (`Stream<String>`) (`:40-46`) |
| Filtrado | `_isForTrackedOrder` descarta eventos de otros pedidos del mismo cliente comparando `orderId`/`order_id` contra `_trackedOrderId`; si el payload no trae orderId, **lo deja pasar** para no perder eventos legacy (`:200-208`) |
| Tolerancia de formato | Acepta `lat`/`latitude`, `lng`/`longitude`, `heading`/`bearing` (`:171-177`) y `status`/`orderStatus`/`state` (`:193-194`) |
| **Reconexión** | **Sí, configurada en el cliente:** `enableReconnection()`, `setReconnectionAttempts(8)`, `setReconnectionDelay(1000)` (ms), con `disableAutoConnect()` + `connect()` explícito (`:111-116, :145`). Lo que **no** hay: re-emisión de `customer:join` tras una reconexión más allá del `onConnect` (que sí vuelve a dispararse), refresco del token de Firebase si expiró durante la desconexión, ni aviso al usuario cuando se agotan los 8 intentos |
| Desconexión | `disconnect()` hace `off` de los 5 eventos, `disconnect()`, `dispose()` y limpia `_trackedOrderId` (`:148-158`). `subscribeToOrder` llama a `disconnect()` primero, así que sólo puede seguirse **un pedido a la vez** (`:108`) |
| Resto del servicio | Además del socket expone HTTP: `fetchOrderById` (`:48-68`) y `confirmDelivery` con `Idempotency-Key` (`:73-101`), y define `enum ConfirmDeliveryResult { success, invalidCode, networkError }` (`:12`) y `class DriverLocationUpdate` (`:14-24`) |

#### Qué pantallas lo consumen

`OrderTrackingService` está registrado como `LazySingleton` (`app.locator.dart:45`) y lo referencian **dos** archivos:

| Consumidor | Qué usa | Línea |
|---|---|---|
| `lib/ui/views/order_tracking/order_tracking_viewmodel.dart` | Único consumidor de los streams. En `_startRealtimeTracking` se suscribe a `driverLocationUpdates` (mueve el marcador, recalcula ETA, redibuja la ruta, reencuadra el mapa) y a `orderStatusUpdates` (actualiza el stage) y luego llama a `subscribeToOrder` | `:33`, `:417-448`; cancelación de ambas suscripciones + `disconnect()` en `dispose()` (`:821-828`); también usa `fetchOrderById` (`:396`) y `disconnect()` en cancelar/confirmar (`:343`, `:362`) |
| `lib/ui/views/qr_scan/qr_scan_viewmodel.dart` | Sólo `confirmDelivery` (HTTP), no el socket | `:18`, `:66-70` |

**No hay reconexión de aplicación**: si el VM se destruye (salir de la pantalla de tracking) el socket se cierra, y el estado del pedido fuera de esa pantalla se actualiza por **polling HTTP cada 10 segundos** desde `history_model.dart:107-113`, no por socket.

---

### TABLA 7 — Código muerto y restos

#### Clases y widgets que nadie usa

| Elemento | Archivo | Verificación |
|---|---|---|
| `Market` (widget) | `lib/ui/widgets/common/market/market.dart` (23) | `builder` devuelve `const SizedBox.shrink()` (`:15`). Grep de `Market` fuera de su carpeta: **0 resultados**. No está en `home_view.dart` |
| `MarketModel` | `lib/ui/widgets/common/market/market_model.dart` (3) | Clase vacía, sólo usada por `Market` |
| `BusinessHours` + `_BusinessHours` | `lib/domain/business_hours.dart` (66) | Grep de `BusinessHours` fuera del archivo: **0 resultados**. Es el modelo del selector de rango horario libre, reemplazado por las franjas fijas (`TimeSlotAvailability`) |
| `NoticeSheet` / `NoticeSheetModel` | `lib/ui/bottom_sheets/notice/notice_sheet.dart` (53) + `notice_sheet_model.dart` (3, clase vacía) | Registrado en `app.dart:65` y `app.bottomsheets.dart:27-28`, pero `BottomSheetType.notice` **nunca se invoca**: los 3 `showCustomSheet` del repo usan `addressList` (`checkout_viewmodel.dart:62`), `rateDriver` (`order_tracking_viewmodel.dart:375`) y `claim` (`history_model.dart:75`) |
| `InfoAlertDialog` / `InfoAlertDialogModel` | `lib/ui/dialogs/info_alert/info_alert_dialog.dart` (107) + `info_alert_dialog_model.dart` (3, clase vacía) | Registrado en `app.dart:72` y `app.dialogs.dart:21-22`, pero **`showCustomDialog` no se llama nunca** (grep: 0 resultados). Todos los diálogos usan `showDialog`/`showConfirmationDialog` genéricos |

#### Métodos y campos sin uso

| Elemento | Archivo:línea | Verificación |
|---|---|---|
| `HistoryService.addOrder(Order)` | `history_service.dart:45-47` | Wrapper de `createOrder`. Grep de `addOrder`: sólo la definición |
| `HistoryService.hasPendingOrder` (getter) | `history_service.dart:35` | `_hasPendingOrder` se escribe en `:70, :101, :138, :153`, pero el getter no se lee desde ningún otro archivo |
| `GasCylinderService.gasCylinder` (getter) | `gas_cylinder_service.dart:18` | La caché `_gasCylinder` se usa internamente; el getter no lo lee nadie fuera del servicio |
| `AddressesViewModel.actionError` | `addresses_viewmodel.dart:16` | Se escribe en `:31, :39, :46` y no se lee en ninguna parte (ver TABLA 5) |
| `OrderTrackingViewModel._arrivingNotified` | `order_tracking_viewmodel.dart:60` | Sólo se escribe (`:578-580`); nunca se lee. Es el resto de una notificación de llegada que no se implementó |
| `MapViewModel._controllerComparer` | `map_viewmodel.dart:18` | Se completa en `:44` y nunca se hace `.future`. El controller real se guarda aparte en `_mapController` (`:19, :45`) |
| `PaymentMethod.online` vs `PaymentMethod.mercadoPago` | `checkout_viewmodel.dart:172` vs `:276` | El recargo del 10% se aplica cuando el método es `online` (`:171-176`), pero el checkout de MercadoPago se dispara cuando es `mercadoPago` (`:276`). Son dos valores distintos del enum de `splg_lib` (`../splg-lib/lib/domain/order.dart:127-137`) |

#### Constantes sin uso — `lib/ui/common/app_strings.dart`

16 de 32 constantes no se referencian en ninguna parte fuera del propio archivo: `signupViewRepeatPassword`, `signupViewPhone`, `signupViewAddress`, `signupViewVerificationCode`, `signupViewResendCode`, `signupViewAddressHint`, `signupViewFinishButton`, `signupViewBack`, `signupViewSendCode`, `signupViewVerifyCode`, `signupViewVaildPasswordError`, `signupViewVaildRepeatPasswordError`, `signupViewVaildPasswordNotEqualError`, `signupViewDialogOtpTitle`, `signupViewDialogOtpDescription`, `signupViewDialogOtpConfirm`, `signupViewDialogOtpCancel`. El grupo OTP (5 constantes, `:33-37`) es el resto de un flujo de verificación por SMS que no existe en el código.

#### Helpers sin uso — `lib/ui/common/ui_helpers.dart` (90 líneas, plantilla de Stacked)

Sin ninguna referencia fuera del archivo: `horizontalSpaceTiny`, `horizontalSpaceMedium`, `horizontalSpaceLarge`, `verticalSpaceMassive`, `spacedDivider`, `verticalSpace()`, `screenWidth()`, `screenHeight()`, `screenHeightFraction()`, `screenWidthFraction()`, `halfScreenWidth()`, `thirdScreenWidth()`, `quarterScreenWidth()`, `getResponsiveHorizontalSpaceMedium()` y las 6 funciones `getResponsive*FontSize()`. Los únicos usados son `horizontalSpaceSmall` (3), `verticalSpaceTiny` (4), `verticalSpaceSmall` (4), `verticalSpaceMedium` (7) y `verticalSpaceLarge` (1), todos en los 4 bottom sheets, el dialog y `startup_view.dart`.

#### TODO / FIXME

Sólo **2** en todo `lib/` (no hay ningún `FIXME`, `HACK` ni `XXX`):

1. `lib/services/order_tracking_service.dart:29` — `// TODO(config): centralizar esta base junto a la de ApiClient por entorno.` Es la causa de que la URL del socket esté fija en `localhost:3000`.
2. `lib/ui/views/qr_scan/qr_scan_viewmodel.dart:32-36` — TODO de 5 líneas sobre que un 400 del backend no distingue "código de otro pedido" de "código mal escrito" cuando hay más de un pedido `on_the_way`.

#### Bloques comentados de más de 5 líneas

El escaneo devuelve 9 bloques de ≥5 líneas consecutivas de comentario. **Ocho de los nueve son documentación válida** (dartdoc de clases y métodos): `firebase_options.dart:7-16` (ejemplo generado por FlutterFire), `create_order_result.dart:3-8`, `payment_outcome.dart:1-5`, `notification_service.dart:11-21`, `app_config.dart:1-6`, `checkout_viewmodel.dart:297-302`, `payment_webview_viewmodel.dart:9-18` y `:51-55`, `qr_scan_viewmodel.dart:29-36` (el TODO de arriba).

**Código realmente comentado — 1 caso, de 2 líneas** (queda bajo el umbral de 5 pero es el único código muerto comentado del repo): `map_viewmodel.dart:14` (`//final _snackbarService = locator<SnackbarService>();`) y `:36` (`//_snackbarService.showSnackbar(message: 'Error al obtener la ubicación.');`).

#### Archivos que ningún import referencia

| Archivo | Situación |
|---|---|
| `lib/domain/business_hours.dart` | Ningún import lo trae. Huérfano total |
| `lib/ui/widgets/common/market/market.dart` + `market_model.dart` | `market.dart` importa a `market_model.dart`, pero nadie importa `market.dart`. Par huérfano |
| `lib/ui/bottom_sheets/notice/notice_sheet.dart` + `notice_sheet_model.dart` | Importados sólo por el código generado (`app.bottomsheets.dart:13`, `app.dart:1`), nunca invocados en runtime |
| `lib/ui/dialogs/info_alert/info_alert_dialog.dart` + `info_alert_dialog_model.dart` | Idem: importados por `app.dialogs.dart:11` y `app.dart:2`, nunca invocados |

---

### TABLA 8 — Configuración

#### ¿Hay `.env` o archivos por flavor?

**No.** `find` de `*.env*` (excluyendo `build/` y `.git/`) no devuelve nada: no hay `.env`, `.env.example`, `.env.dev`, ni `flutter_dotenv` en `pubspec.yaml`. Tampoco hay `productFlavors` en `android/app/build.gradle*` ni schemes/xcconfig por entorno en `ios/`. No existe `.vscode/launch.json` con `--dart-define`; `.vscode/` sólo tiene `settings.json`.

La configuración por entorno se resuelve **sólo con `--dart-define`**, leída en `lib/core/config/app_config.dart` con `String.fromEnvironment` y valores por defecto embebidos.

#### Variables que la app espera

| Variable | Default si no se pasa | Dónde se lee | Dónde se usa |
|---|---|---|---|
| `API_BASE_URL` | `http://localhost:3000` | `app_config.dart:11-14` | `AppConfig.apiUrl` = `$API_BASE_URL/api/` (`:17`) → `baseUrl` de Dio (`api_client.dart:19`) |
| `DISTRIBUTOR` | `jeny-gas` | `app_config.dart:23-26` | Header `X-Distributor` en los 5 verbos (`api_client.dart:41,67,93,113,137`) y query `?distributor=` de franjas (`time_slot_remote_datasource.dart:15`) |
| `MP_SUCCESS_URL` | `https://splg.app/pago/exito` | `app_config.dart:32-35` | Detección de retorno en el WebView (`payment_webview_viewmodel.dart:66`) |
| `MP_FAILURE_URL` | `https://splg.app/pago/error` | `app_config.dart:36-39` | `payment_webview_viewmodel.dart:67` |
| `MP_PENDING_URL` | `https://splg.app/pago/pendiente` | `app_config.dart:40-43` | `payment_webview_viewmodel.dart:68` |

Los tres `MP_*` tienen que coincidir con `MP_SUCCESS_URL` / `MP_FAILURE_URL` / `MP_PENDING_URL` del backend; lo dice el comentario de `app_config.dart:28-31`.

**Variable que falta y no se puede configurar:** la URL del socket. `order_tracking_service.dart:30` la tiene hardcodeada en `http://localhost:3000/customers` y no pasa por `AppConfig`. Contra un backend que no sea `localhost:3000`, el HTTP apunta bien (por `API_BASE_URL`) pero el tiempo real no conecta. En emulador Android, además, `localhost` tampoco resuelve al host (hace falta `10.0.2.2`, según el propio comentario de `:27-28`).

#### Archivos de configuración presentes y versionados

| Archivo | ¿Está? | ¿Versionado? |
|---|---|---|
| `android/app/google-services.json` | Sí | **Sí** (`git ls-files` lo devuelve) |
| `ios/Runner/GoogleService-Info.plist` | Sí | **Sí** |
| `lib/firebase_options.dart` | Sí | **Sí** — proyecto `splg-gas`, `messagingSenderId: 757204810726`, con `apiKey` de Android (`:53`) y de iOS (`:61`) en texto plano |
| `firebase.json` | Sí (540 B, raíz) | Sí |
| `stacked.json` | Sí | Sí |
| `analysis_options.yaml` | Sí (44 B) | Sí |
| Assets | `assets/logo.png` (916 KB), `assets/cylinder_10.png` (875 KB), `legal/*.md` — declarados en `pubspec.yaml:60-62` | Sí |
| `pubspec.lock` | Sí (38 KB) | Sí |

#### API keys embebidas en el repositorio

- **Google Maps Android:** `AIzaSyAvywoBGIhVqoWUn-MhybUea1oXIoKgtp8` en `android/app/src/main/AndroidManifest.xml:37-38`.
- **Google Maps iOS:** la **misma** clave, `AIzaSyAvywoBGIhVqoWUn-MhybUea1oXIoKgtp8`, en `ios/Runner/AppDelegate.swift:11` (`GMSServices.provideAPIKey(...)`).
- **Firebase Android:** `AIzaSyCINEEptz-g3DX_vVkn1RfKftGNHtqwCas` (`lib/firebase_options.dart:53`).
- **Firebase iOS:** `AIzaSyAZE8JBLkpd2PjrdV5lNxwJLLMXinNe7oU` (`lib/firebase_options.dart:61`).

El `.gitignore` (703 B) no excluye `google-services.json`, `GoogleService-Info.plist` ni `firebase_options.dart`.

#### Dependencia local

`pubspec.yaml:41-42` declara `splg_lib` con `path: ../splg-lib`. El directorio existe (`/Users/.../garrafitas/splg-lib`, con `lib/`, `pubspec.yaml`, `test/`) y de ahí salen `Order`, `OrderStatus`, `PaymentMethod`, `Customer`, `Address`, `GasCylinder`, `Discount`, `OrderItem` y el tema (`splg_lib/theme/app_theme.dart`, usado en `main.dart:7,35-36`).

#### Qué hace falta para que la app corra

1. **`flutter pub get`** con `../splg-lib` presente en el disco (dependencia por path, no publicada).
2. **Backend accesible.** Sin `--dart-define`, la app pega a `http://localhost:3000/api/` con `X-Distributor: jeny-gas`. En device físico o emulador Android hay que pasar `--dart-define=API_BASE_URL=...`.
3. **La distribuidora `jeny-gas` tiene que existir en el backend**, o cambiar `DISTRIBUTOR`: el header va en **todas** las requests.
4. **Socket de tracking:** hoy sólo funciona contra `localhost:3000` (simulador iOS o desktop). Para cualquier otro entorno hay que tocar `order_tracking_service.dart:30`; no hay variable.
5. **Firebase:** ya configurado y versionado (proyecto `splg-gas`), Auth por email/password. Para push en iOS falta subir la APNs Auth Key (.p8) a Firebase Console; está documentado en `notification_service.dart:18-21`, que aclara que hasta entonces `getToken()` en iOS puede devolver null o tirar error (todo el flujo está en try/catch para no romper).
6. **Google Maps:** las claves ya están en el manifest y en `AppDelegate.swift`; hay que verificar que esa clave tenga habilitadas Maps SDK for Android/iOS y Geocoding API.
7. **Permisos en runtime:** ubicación (`geolocator`/`permission_handler`), cámara (`mobile_scanner`, para el QR de entrega) y notificaciones.
8. **MercadoPago:** las tres `MP_*` de la app deben coincidir con las del backend, si no el WebView no detecta el retorno y se queda navegando dentro de la página de MP.
9. **Nada más falta del repo:** no hay ningún archivo de configuración ignorado o ausente. Todo lo necesario está versionado; lo que falta es infraestructura (backend levantado y APNs key), no archivos.

---

### Apéndice — Tests presentes

`test/` (no forma parte del pedido, se lista por completitud): `test/golden/home_view_golden_test.dart`, `test/helpers/test_helpers.dart` + `.mocks.dart`, `test/services/` (5: cart, customer, gas_cylinder, history, location), `test/viewmodels/` (9: address_list_sheet_model, checkout, home, info_alert_dialog_model, login, map, notice_sheet_model, profile, signup) y `test/widget_models/` (5: account, history, market, order, profile). Dev deps: `mockito ^5.4.1`, `golden_toolkit ^0.15.0`, `build_runner`, `stacked_generator` (`pubspec.yaml:64-72`).

Nota: hay tests para tres piezas que la app no usa en runtime — `market_model_test.dart`, `notice_sheet_model_test.dart` e `info_alert_dialog_model_test.dart` (ver TABLA 7). Tampoco hay test para las 3 vistas más grandes: order_tracking, qr_scan y payment_webview.

---

## Parte IV — La aplicación del chofer

Repo: `/Users/nahuelwagner/Desktop/myprojects/gearthlogic/projects/garrafitas/splg-app-chofer`
Rama: `develop` · Working tree limpio (`git status --short` sin salida)
38 archivos `.dart` en `lib/`, 5.183 líneas totales.
Verificación de compilación: `flutter analyze` → **12 issues, ninguno error** (10 info + 2 warnings, los 2 warnings en `test/`).

Todas las referencias `archivo:línea` de este informe fueron leídas del archivo.

---

### TABLA 1 — Pantallas (`lib/ui/views/`)

| Pantalla | Archivo | Líneas | ¿ViewModel? | Qué hace | ¿Completa o esqueleto? |
|---|---|---|---|---|---|
| StartupView | `lib/ui/views/startup/startup_view.dart` | 55 | Sí — `startup_viewmodel.dart` (29) | Splash con `assets/logo.png` + "Cargando..." (`startup_view.dart:23-40`); en `onViewModelReady` dispara `runStartupLogic()` (`startup_view.dart:53-54`) que llama `restoreSession()` y redirige a Home o Login (`startup_viewmodel.dart:17-28`) | Cumple el criterio numérico de esqueleto (<60 líneas) pero **es funcionalmente completa**: toda la lógica vive en el VM |
| LoginView | `lib/ui/views/login/login_view.dart` | 175 | Sí — `login_viewmodel.dart` (46) + `login_view.form.dart` (206, generado por `@FormView`, `login_view.dart:10-13`) | Formulario email+password, estado busy, banner de error (`login_view.dart:117-127`), botón que llama `viewModel.onLogin()` (`login_view.dart:141`) | Completa. **Excepción**: "olvidé mi contraseña" es un `onPressed: () {}` vacío (`login_view.dart:107`) |
| HomeView | `lib/ui/views/home/home_view.dart` | 261 | Sí — `home_viewmodel.dart` (381) | Google Map con marcador propio (`home_view.dart:140-150`), drawer con nombre del chofer y accesos legales (`home_view.dart:30-120`), vista alternativa de permisos denegados (`home_view.dart:203-251`), botón Conectarse/Desconectarse (`home_view.dart:181-197`) | Completa. 3 ítems del drawer son TODO sin implementar (`home_view.dart:69`, `:77`, `:88`) y el icono de notificaciones es `onPressed: () {}` (`home_view.dart:25`) |
| DeliveryView | `lib/ui/views/delivery/delivery_view.dart` | 922 | Sí — `delivery_viewmodel.dart` (482) | Entrega en curso: chip de estado (`:140`), tarjeta del pedido (`:171`), alta de envases por serial (`_CylinderAssignCard`, `:748`), botón "En camino" (`:226`), "Navegar" con hoja Waze/Maps (`:264`, `:280`), "Avisar que llegué" (`:250`), QR de entrega (`:318`), reporte de incidencia (`_IncidentSheet`, `:475`), pantalla de entregado + calificación (`:388`, `_CustomerRatingCard`, `:611`) | Completa — es la pantalla más desarrollada de la app |
| LegalView | `lib/ui/views/legal/legal_view.dart` | 101 | Sí — `legal_viewmodel.dart` (32) | Renderiza markdown de `legal/terminos-y-condiciones.md` o `legal/politica-de-privacidad.md` según el enum `LegalDocument` (`legal_view.dart:8-22`); estados busy y error (`:62-77`) | Completa |
| DirectionsView | `lib/ui/views/directions/directions_view.dart` | 29 | Sí, pero vacío — `directions_viewmodel.dart` (3): `class DirectionsViewModel extends BaseViewModel {}` | `Scaffold` con `Center(child: Text("DirectionsView"))` (`directions_view.dart:19`) | **ESQUELETO** (29 líneas + sólo un Scaffold con texto + VM vacío). Además nadie navega a ella (ver Tabla 6) |

Otras superficies de UI (fuera de `views/`):

| Componente | Archivo | Líneas | Estado |
|---|---|---|---|
| OrderOfferDialog | `lib/ui/dialogs/order_offer/order_offer_dialog.dart` | 196 | Completo — dialog de oferta con countdown (`order_offer_dialog_model.dart`, 74) |
| InfoAlertDialog | `lib/ui/dialogs/info_alert/info_alert_dialog.dart` | 107 | Plantilla del scaffold de Stacked; registrado pero nunca invocado (ver Tabla 6) |
| OrderInfoSheet | `lib/ui/bottom_sheets/order_info/order_info_sheet.dart` | 59 | **Esqueleto**: texto por defecto `'Hello Stacked Sheet!!'` (`:38`), modelo vacío; nunca invocado |

---

### TABLA 2 — Arquitectura

**Patrón: MVVM con Stacked** (`stacked: ^3.4.0`, `stacked_services: ^1.1.0` en `pubspec.yaml:11-12`). Declaración única en `lib/app/app.dart:20-51` con `@StackedApp` (rutas, dependencias, bottomsheets, dialogs); el generador produce `app.router.dart` (471), `app.locator.dart` (42), `app.dialogs.dart` (30) y `app.bottomsheets.dart` (26), todos marcados `GENERATED CODE - DO NOT MODIFY BY HAND`.

| Carpeta | Contenido real | Rol |
|---|---|---|
| `lib/app/` | `app.dart` (fuente de verdad) + 4 archivos generados | Wiring: rutas, DI (get_it vía `StackedLocator`), builders de dialogs/sheets |
| `lib/core/` | `core/config/app_config.dart` (31), `core/network/api_client.dart` (128) | Configuración de entorno y cliente HTTP |
| `lib/services/` | 7 servicios: `driver_auth_service.dart` (145), `driver_socket_service.dart` (202), `location_service.dart` (175), `fcm_service.dart` (184), `foreground_service.dart` (110), `order_service.dart` (153), `navigation_launcher.dart` (36) | Acceso a datos + integraciones de plataforma |
| `lib/ui/` | `views/` (6 pantallas), `dialogs/` (2), `bottom_sheets/` (1), `common/` (`app_colors.dart` 9, `app_strings.dart` 22, `ui_helpers.dart` 90) | Presentación |

**Registro en el locator** (`lib/app/app.locator.dart:33-41`): `BottomSheetService`, `DialogService`, `NavigationService`, `OrderService`, `LocationService`, `DriverSocketService`, `DriverAuthService`, `DriverForegroundService`, `FcmService` — todos `LazySingleton`.

#### Cómo resuelve el acceso a datos (no hay `data/` ni `domain/`)

Confirmado: no existen `lib/data/` ni `lib/domain/`. El acceso a datos se resuelve así:

1. **Un único cliente HTTP singleton manual**, no inyectado: `ApiClient` con `static final instance = ApiClient._()` y `factory ApiClient()` (`api_client.dart:9-15`). Expone `get/post/patch/put` genéricos (`:34`, `:53`, `:79`, `:105`) que devuelven el `Response` de Dio crudo. **No está registrado en el locator**; los consumidores lo instancian directamente: `final _apiClient = ApiClient();` en `driver_auth_service.dart:22`, `fcm_service.dart:44`, `home_viewmodel.dart:26` y `delivery_viewmodel.dart:46`.
2. **No hay repositorios ni DTOs propios**. Los ViewModels arman la URL, el body y los headers ellos mismos y parsean el `Map` crudo de la respuesta. Ejemplos: `home_viewmodel.dart:352-357` (aceptar pedido), `delivery_viewmodel.dart:161-174` (traer pedido).
3. **No se usa el modelo compartido para parsear.** `DeliveryViewModel` parsea a mano sobre el `Map` (`delivery_viewmodel.dart:99-143`) y el propio doc-comment explica por qué: `Order.fromJson` de `splg_lib` no calza con `GET /orders/:id` (`gas_cylinder` sin `isActive`, `weight` numérico vs `String`) — `delivery_viewmodel.dart:32-40`.
4. **`splg_lib`** (dependencia por path, `pubspec.yaml:40-41`; el directorio hermano `../splg-lib` existe) se usa sólo para el tema (`AppTheme` en `main.dart:6,36-37`) y para los modelos de `OrderService` (`order_service.dart:1-6`) — que es código muerto (Tabla 6).
5. **Separación real**: se respeta en Home, Delivery, Login, Legal y Startup — las Views no hacen red ni tocan servicios, todo pasa por el VM. **Rupturas verificadas**: `home_viewmodel.dart:26` y `delivery_viewmodel.dart:46` hacen llamadas HTTP directas desde el ViewModel (no hay capa intermedia), y `DriverAuthService` se resuelve lazy con un getter en lugar de campo, a propósito, porque `FirebaseAuth.instance` rompería los tests (`home_viewmodel.dart:29-34`, `delivery_viewmodel.dart:52-54`).

---

### TABLA 3 — El flujo del reparto, paso a paso

| # | Paso | Pantalla / disparador | Código | Endpoint o evento |
|---|---|---|---|---|
| 0 | Arranque | `main.dart:15-27`: Firebase init, handler FCM background, locator, dialogs, sheets. Ruta inicial `Routes.startupView` (`main.dart:35`) | `main.dart:17-26` | — |
| 1 | Restaurar sesión | StartupView → `onViewModelReady` post-frame | `startup_view.dart:53-54` → `startup_viewmodel.dart:17-28` → `driver_auth_service.dart:116-136` | Lee `flutter_secure_storage` (`driver_auth_service.dart:120-125`); si falta el `user_id`, re-trae perfil (`:131`) |
| 2 | Login | LoginView, botón "Continuar" | `login_view.dart:138-143` → `login_viewmodel.dart:20-45` → `driver_auth_service.dart:48-68` | Firebase `signInWithEmailAndPassword` (`driver_auth_service.dart:50`) **+** `GET users/email/{email}` (`driver_auth_service.dart:75`) para obtener el `user_id` real de la base |
| 2b | Validación de rol | — | `driver_auth_service.dart:87-91` | Sólo `delivery` o `super_admin`; si no, `signOut()` y login fallido (`:58`) |
| 2c | Registro push | Tras login OK (y en cada arranque con sesión) | `login_viewmodel.dart:39` / `startup_viewmodel.dart:23` → `fcm_service.dart:117-143` | `POST notifications/token` con `{userId, token, platform}` (`fcm_service.dart:160-168`) |
| 3 | Ponerse en línea | HomeView, botón "Conectarse" | `home_view.dart:182-183` → `home_viewmodel.dart:222-264` | `PATCH delivery/user/{userId}/availability` con `{available: true}` (`home_viewmodel.dart:285-289`) |
| 3b | Keep-alive | — | `home_viewmodel.dart:242-246` → `foreground_service.dart:66-85` | Foreground service Android "Estás en línea" |
| 3c | Abrir socket | — | `home_viewmodel.dart:248` → `driver_socket_service.dart:68-127` | Socket.IO a `AppConfig.driversNamespace` = `{API_BASE_URL}/drivers` (`app_config.dart:30`), token en `auth.token` **y** en header `Authorization` (`driver_socket_service.dart:80-82`) |
| 3d | Unirse a la sala | Al conectar | `driver_socket_service.dart:101-106` | **emite `driver:join`** con `{driverId}` |
| 3e | Primera posición | — | `home_viewmodel.dart:252-260` | **emite `driver:update-location`** `{userId, lat, lng}` (`driver_socket_service.dart:139-143`) |
| 4 | Recibir la oferta | Socket → dialog | `driver_socket_service.dart:91-99` (listener) → `_incomingOrdersController` (`:51-54`) → `home_viewmodel.dart:295-299` (suscripción) → `home_viewmodel.dart:303-320` | **escucha `server:new-order-request`**; payload `{event: NEW_ORDER\|NEW_ORDER_RETRY, orderId, totalAmount, paymentMethod, expiresAt, items}` (`driver_socket_service.dart:43-48`) |
| 4b | Mostrar la oferta | Dialog `DialogType.orderOffer` | `home_viewmodel.dart:310-313` → `order_offer_dialog.dart:21-117` | Countdown hasta `expiresAt`, fallback 30s, tope 120s (`order_offer_dialog_model.dart:26-44`, `:53-67`) |
| 5a | **Aceptar** | Botón "Aceptar (Ns)" | `order_offer_dialog.dart:104-107` → `home_viewmodel.dart:343-374` | `PATCH orders/{orderId}/status` con `{status: 'accepted'}` + header `Idempotency-Key` uuid v4 (`home_viewmodel.dart:352-357`) |
| 5b | Tras aceptar | — | `home_viewmodel.dart:361-366` | `startBroadcasting()`, foreground pasa a "En reparto", `navigateToDeliveryView(orderId: ...)` |
| 5c | **Rechazar** | Botón "Rechazar" o vencimiento del countdown | `order_offer_dialog.dart:91-94` / `:188-193` → `home_viewmodel.dart:318` → `:324-338` | `POST orders/{orderId}/reject` con body `{}` + `Idempotency-Key` (`home_viewmodel.dart:328-333`) |
| 5d | Descarte | Si el dialog se cierra sin respuesta (`response == null`) | `home_viewmodel.dart:315-319` | Se trata como rechazo → mismo `POST .../reject` |
| 6 | Cargar la entrega | DeliveryView `onViewModelReady` | `delivery_view.dart:458-459` → `delivery_viewmodel.dart:145-150` | `GET orders/{orderId}` (`delivery_viewmodel.dart:161`) |
| 6b | Polling | Timer cada 5s mientras no esté `delivered` | `delivery_viewmodel.dart:20` (`_kPollInterval`), `:182-193` | `GET orders/{orderId}` silencioso (`:191`) |
| 7 | Despachar envases (opcional) | Tarjeta "Envases del pedido", botón "Despachar N envase(s)" | `delivery_view.dart:892-916` → `:780-789` → `delivery_viewmodel.dart:288-331` | `POST cylinders/assign` con `{orderId, serials}` + `Idempotency-Key` (`:304-309`) |
| 8 | **En camino** | Botón "En camino" (sólo si `isAccepted`) | `delivery_view.dart:60-63`, `:226-248` → `delivery_viewmodel.dart:384-422` | `PATCH orders/{orderId}/status` con `{status: 'on_the_way'}` + `Idempotency-Key` (`:400-405`). Nota documentada: se **manda** `on_the_way` pero se **lee** `out_for_delivery` (`delivery_viewmodel.dart:24-31`, `:102`) |
| 9 | **Reportar posición** | Automático mientras hay tracking | `location_service.dart:115-127` (stream de Geolocator) → `driver_socket_service.dart:166-174` (suscripción) → `:131-144` | **emite `driver:update-location`** `{userId, lat, lng}`. Segunda vía en paralelo: `home_viewmodel.dart:63-78` (`onData` del `StreamViewModel`) emite lo mismo mientras HomeView siga viva |
| 10 | Navegar al domicilio | Botón "Navegar" → hoja Waze / Google Maps | `delivery_view.dart:264-278`, `:280-316` → `delivery_viewmodel.dart:455-475` → `navigation_launcher.dart:11-22` | `url_launcher` externo: `https://waze.com/ul?ll=...&navigate=yes` / `google.com/maps/dir/?api=1&destination=...` |
| 11 | **Marcar que llegó** | Botón "Avisar que llegué" (sólo si `isOnTheWay && !arrivedNotified`) | `delivery_view.dart:66-69`, `:250-262` → `delivery_viewmodel.dart:210-237` | `PATCH orders/{orderId}/arrived` con body `{}` + `Idempotency-Key` (`:219-224`). No cambia el estado del pedido; `_arrivedNotified` es **flag local** (`:68-71`, `:226`) |
| 12 | Mostrar el QR | Botón "Mostrar QR de entrega" | `delivery_view.dart:325-340` → `delivery_viewmodel.dart:425-453` | `GET orders/{orderId}/delivery-code` (`:435`); se renderiza con `QrImageView` (`delivery_view.dart:363-367`) |
| 13 | **Confirmar la entrega** | **NO la dispara esta app.** El cliente escanea el QR; el chofer se entera por el polling del paso 6b | `delivery_viewmodel.dart:16-19` (comentario), `:163-170` (detección `!wasDelivered && isDelivered`) | `GET orders/{orderId}` devuelve `status: 'delivered'` |
| 13b | Efectos del cierre | — | `delivery_viewmodel.dart:198-205` | Cancela el polling, `stopBroadcasting()` (que **también cierra el socket**, `driver_socket_service.dart:181-187` → `:190-194`) y baja el foreground a "Estás en línea" |
| 13c | Pantalla de éxito | — | `delivery_view.dart:35-36`, `:388-425` | "¡Entrega confirmada!" + tarjeta de calificación |
| 14 | Calificar al cliente | `_CustomerRatingCard`, botón "Enviar calificación" | `delivery_view.dart:715-736` → `:630-641` → `delivery_viewmodel.dart:337-378` | `POST ratings` con `{orderId, stars, comment?}` + `Idempotency-Key` (`:357-362`) |
| 15 | Volver | Botón "Volver al inicio" | `delivery_view.dart:414` → `delivery_viewmodel.dart:479-481` | `clearStackAndShow(Routes.homeView)` |
| 16 | Reportar incidencia (en cualquier momento) | "Reportar un problema" → `_IncidentSheet` | `delivery_view.dart:81-99`, `:101-114`, `:496-523` → `delivery_viewmodel.dart:243-281` | `POST incidents` con `{orderId, type, description}`; `type` ∈ `damaged\|out_of_stock\|no_show\|other` (`delivery_view.dart:466-471`) |
| 17 | Salir de línea | HomeView, botón cuando `isConnected` | `home_view.dart:183` → `home_viewmodel.dart:268-275` | `PATCH delivery/user/{userId}/availability` con `{available: false}`, foreground stop, socket `disconnect()` |

**Inventario de endpoints REST que usa la app** (8): `GET users/email/{email}`, `POST notifications/token`, `PATCH delivery/user/{userId}/availability`, `PATCH orders/{id}/status`, `POST orders/{id}/reject`, `GET orders/{id}`, `PATCH orders/{id}/arrived`, `GET orders/{id}/delivery-code`, `POST cylinders/assign`, `POST incidents`, `POST ratings` (11 en total contando los tres últimos).

**Eventos de socket** (3): escucha `server:new-order-request`; emite `driver:join` y `driver:update-location`.

---

### TABLA 4 — Tiempo real y ubicación (`lib/services/`)

| Aspecto | Hecho verificado | Archivo:línea |
|---|---|---|
| Namespace del socket | `{API_BASE_URL}/drivers` | `app_config.dart:30`, `driver_socket_service.dart:14` |
| Transporte | Sólo `websocket` (sin fallback a polling) | `driver_socket_service.dart:80` |
| Autenticación | Token de Firebase en `auth.token` **y** en `extraHeaders: Authorization: Bearer` | `driver_socket_service.dart:81-82` |
| Eventos que **escucha** | `server:new-order-request` (único). Valida que el payload sea `Map`; si no, sólo loguea | `driver_socket_service.dart:91-99` |
| Eventos que **emite** | `driver:join` `{driverId}` (al conectar y al reconectar) y `driver:update-location` `{userId, lat, lng}` | `driver_socket_service.dart:105`, `:123`, `:139-143` |
| Reconexión | **Sí**: `.enableReconnection()` + `.enableForceNew()`; hay `onReconnect` que **re-emite `driver:join`** | `driver_socket_service.dart:83-84`, `:121-124` |
| Callbacks de socket | `onConnect`, `onDisconnect`, `onConnectError`, `onError`, `onReconnect` — todos registrados | `driver_socket_service.dart:101-124` |
| Guarda de conexión | `connect()` hace early-return si ya hay socket; `sendLocation()` descarta si no está conectado | `driver_socket_service.dart:69-73`, `:132-137` |
| Stream de ofertas | `StreamController.broadcast()` que **sobrevive a reconexiones** (sólo se cierra en `dispose`) | `driver_socket_service.dart:51-54`, `:200` |
| **Frecuencia de reporte de posición** | **No hay intervalo de tiempo**: es por distancia. `LocationSettings(accuracy: high, distanceFilter: 10)` → una posición cada 10 metros recorridos | `location_service.dart:109-112` |
| Emisión de posición | Suscripción al `positionStream` del `LocationService`; cada evento dispara `sendLocation` | `driver_socket_service.dart:165-174` |
| Doble vía de emisión | `HomeViewModel.onData` **también** emite `driver:update-location` por cada posición mientras HomeView esté viva y el chofer conectado — en paralelo a la suscripción del socket service | `home_viewmodel.dart:63-78` |
| Reporte puntual inicial | Al conectar se manda la posición actual sin esperar al próximo tick | `home_viewmodel.dart:252-260` |
| **Permisos de ubicación** | **Sí**: `checkAndRequestLocationPermission()` verifica que el servicio esté habilitado (`Geolocator.isLocationServiceEnabled`), consulta `Permission.location.status`, pide el permiso si está `denied` y detecta `permanentlyDenied` | `location_service.dart:37-68` |
| Permisos: dónde se piden | En `HomeViewModel.initialize()` vía `_checkLocationPermission()` (`home_viewmodel.dart:89-94`, `:111-133`) y también dentro de `startTracking()` / `getCurrentLocation()` | `location_service.dart:95`, `:73` |
| Permisos: UI | Pantalla dedicada con mensaje por caso, botón "Solicitar permisos" y "Abrir configuración" | `home_view.dart:203-251`, `home_viewmodel.dart:118-127` |
| Permiso de notificaciones | FCM: `requestPermission(alert/badge/sound)` (`fcm_service.dart:121-129`); foreground task: `checkNotificationPermission` + `requestNotificationPermission` (`foreground_service.dart:54-63`) | — |
| Manifest Android | `ACCESS_FINE_LOCATION`, `ACCESS_COARSE_LOCATION`, `ACCESS_BACKGROUND_LOCATION`, `INTERNET`, `FOREGROUND_SERVICE`, `FOREGROUND_SERVICE_LOCATION`, `POST_NOTIFICATIONS`, `WAKE_LOCK`; servicio `foregroundServiceType="location"` | `android/app/src/main/AndroidManifest.xml:2-10`, `:48-51` |
| Info.plist iOS | `NSLocationWhenInUseUsageDescription`, `NSLocationAlwaysAndWhenInUseUsageDescription`, `UIBackgroundModes: remote-notification` | `ios/Runner/Info.plist:5`, `:7`, `:9-13` |
| Foreground service | Mantiene vivo el proceso (socket + GPS) en background; el TaskHandler es intencionalmente vacío — socket y GPS viven en el isolate principal | `foreground_service.dart:4-23`, `:26-109` |
| FCM | Handler top-level `@pragma('vm:entry-point')` registrado en `main.dart:22`; sólo loguea (`fcm_service.dart:18-21`). En foreground dispara notificación local (`fcm_service.dart:80-83`, `:87-109`). `onTokenRefresh` re-registra el token (`:137-139`) | — |
| Bloqueo conocido documentado | iOS requiere el certificado APNs `.p8` subido en Firebase Console, **pendiente**; sin eso `getToken()` puede fallar y `onMessage` no dispara | `fcm_service.dart:39-42` |

**Nota de comportamiento verificable (no es opinión, es el flujo del código)**: `_onDeliveryConfirmed()` llama `stopBroadcasting()` (`delivery_viewmodel.dart:200`), que además de cancelar la suscripción de posición ejecuta `disconnect()` y destruye el socket (`driver_socket_service.dart:181-187` → `:190-194`), mientras la disponibilidad en el backend sigue en `true` (el único lugar que la pone en `false` es `HomeViewModel.disconnect()`, `home_viewmodel.dart:269`).

---

### TABLA 5 — Manejo de errores

#### Dónde SÍ se muestra el error al usuario

| Lugar | Mecanismo | archivo:línea |
|---|---|---|
| Login fallido | `errorMessage` del VM pintado bajo el formulario | `login_viewmodel.dart:42` → `login_view.dart:117-127` |
| Campos vacíos en login | `errorMessage` | `login_viewmodel.dart:27` |
| Permisos de ubicación | `permissionMessage` + pantalla completa | `home_viewmodel.dart:118-127` → `home_view.dart:226-227` |
| Carga del pedido / "en camino" / "llegué" / navegación sin coordenadas | `errorMessage` → banner rojo | `delivery_viewmodel.dart:97`, `:173`, `:177`, `:214`, `:229`, `:234`, `:390`, `:412`, `:417`, `:459`, `:470` → `delivery_view.dart:48-51`, `:116-138` |
| QR de entrega | `qrError` bajo el botón | `delivery_viewmodel.dart:440`, `:443`, `:448` → `delivery_view.dart:341-347` |
| Despacho de envases | `cylinderError` (parsea `message` del backend, incluso si viene como lista) | `delivery_viewmodel.dart:293`, `:314-321`, `:325` → `delivery_view.dart:884-890` |
| Calificación | `ratingError` | `delivery_viewmodel.dart:342`, `:367`, `:372` → `delivery_view.dart:707-713` |
| Incidencia | SnackBar verde/rojo según resultado | `delivery_view.dart:514-522`; descripción vacía → SnackBar `:499-501` |
| Documento legal | `hasError` → texto "No pudimos cargar este documento" | `legal_viewmodel.dart:27-28` → `legal_view.dart:66-77` |

#### `catch` vacío o sólo log/print

| Tipo | archivo:línea | Detalle |
|---|---|---|
| `print()` en producción | `order_service.dart:145` | `print('Error fetching orders: $e')` — único `print` del repo; `flutter analyze` lo marca como `avoid_print` |
| `catch (_)` sin variable | `legal_viewmodel.dart:27` | No es silencioso: setea `_hasError = true`, que la View muestra |
| `try/catch` que sólo hace `rethrow` | `api_client.dart:48-50`, `:74-76`, `:100-102`, `:124-126` | Los cuatro métodos envuelven en try/catch para re-lanzar sin agregar nada |
| Sólo `debugPrint` (sin UI) | `location_service.dart:42`, `:59`, `:65`, `:87`, `:97`, `:102`, `:121`, `:125`, `:131` | Servicio de ubicación: todos los fallos van a consola |
| Sólo `debugPrint` (sin UI) | `foreground_service.dart:61`, `:83`, `:97`, `:107` | Los 4 métodos del foreground service son best-effort silencioso |
| Sólo `log()` (sin UI) | `driver_socket_service.dart:70`, `:93`, `:96`, `:110`, `:114`, `:118`, `:134`, `:171` | Incluye `onConnectError` y `onError`: **una caída del socket no produce ningún aviso visual** |
| Sólo `log()` (sin UI) | `driver_auth_service.dart:61`, `:64`, `:88`, `:107`, `:133` | El motivo real del fallo de login (rol equivocado, backend caído, credenciales) se colapsa a un único mensaje genérico en la UI |
| Sólo `log()` (sin UI) | `fcm_service.dart:20`, `:107`, `:128`, `:141`, `:153`, `:175` | Registro de push best-effort; el comentario en `:171-174` deja escrito que el endpoint hoy sólo persiste tokens de Customer, no de Delivery |
| Sólo `log()` (sin UI) | `navigation_launcher.dart:28`, `:32` | Si Waze/Maps no está instalado, devuelve `false` |

#### Pasos del reparto SIN manejo de error visible para el chofer

| Paso | Qué pasa si falla | archivo:línea |
|---|---|---|
| **Ponerse disponible** (`PATCH .../availability` true) | `catch` → `debugPrint`; el comentario dice explícitamente "best-effort: si falla, no bloquea el flujo del socket". El chofer ve el botón en verde "Conectado" aunque el backend nunca lo haya marcado disponible | `home_viewmodel.dart:280-293`, `:277-279` |
| **Conectar sin sesión** | `debugPrint('No se puede conectar: falta la sesión del chofer')` y `return` — la UI no cambia ni avisa | `home_viewmodel.dart:230-233` |
| **Aceptar el pedido** | `catch` → `debugPrint`; HTTP ≠ 200 → `debugPrint`. **No hay navegación ni mensaje**: el dialog ya se cerró y el chofer queda en el mapa sin saber que la aceptación falló | `home_viewmodel.dart:346-348`, `:367-373` |
| **Rechazar el pedido** | `catch` → `debugPrint`; si el token es null hace `return` silencioso | `home_viewmodel.dart:326`, `:334-337` |
| **Oferta sin `orderId`** | Se descarta con `debugPrint`; el chofer nunca ve esa oferta | `home_viewmodel.dart:304-308` |
| **Reporte de posición GPS** | Si `sendLocation` se llama con el socket caído, sólo loguea y descarta la posición (no se encola ni reintenta) | `driver_socket_service.dart:132-137` |
| **Error del stream de posición** | `debugPrint` en el service y `log` en el socket service; `HomeViewModel` tiene el `onError` del `StreamViewModel` **comentado** | `location_service.dart:124-126`, `driver_socket_service.dart:170-173`, `home_viewmodel.dart:81-86` |
| **Polling de la entrega** | Corre con `silent: true`: los fallos de red durante la espera de confirmación no actualizan `errorMessage` ni se ven | `delivery_viewmodel.dart:191`, `:166`, `:171`, `:177` |
| **Abrir Waze / Google Maps** | `NavigationLauncher` devuelve `false` y el VM **descarta el valor de retorno** sin usarlo | `delivery_viewmodel.dart:463`, `:474` vs `navigation_launcher.dart:24-34` |
| **Logout** | `HomeViewModel.logout()` **no llama** a `DriverAuthService.signOut()`, ni a `disconnect()`, ni pone `available: false`: sólo frena el tracking y navega a Login. La sesión de Firebase y el `flutter_secure_storage` quedan intactos (`signOut()` sólo aparece definido en `driver_auth_service.dart:138` y nunca se invoca) | `home_viewmodel.dart:211-217` |
| **Botón "Avisar que llegué"** | No tiene flag de "en curso": el `onPressed` no se deshabilita durante la llamada (a diferencia de "En camino", que usa `isUpdatingStatus`) | `delivery_view.dart:254` vs `:230` |

---

### TABLA 6 — Código muerto y restos

#### Archivos sin referencias funcionales

| Archivo | Líneas | Evidencia |
|---|---|---|
| `lib/services/order_service.dart` | 153 | **Devuelve 6 pedidos hardcodeados tras `Future.delayed(2s)`** (`:16-147`). Referencias en todo `lib/`: sólo `app.dart:34` y `app.locator.dart:36` (registro). Ningún ViewModel lo inyecta. `init()` (`:12`) y `remove()` (`:149`) nunca se llaman |
| `lib/ui/views/directions/directions_view.dart` + `directions_viewmodel.dart` | 29 + 3 | Ruta registrada (`app.dart:25`, `app.router.dart:27`, `:48`, `:81-87`) y helpers generados `navigateToDirectionsView` (`app.router.dart:306`) / `replaceWithDirectionsView` (`:416`), pero **ninguno tiene llamador** fuera del archivo generado |
| `lib/ui/bottom_sheets/order_info/order_info_sheet.dart` + `_model.dart` | 59 + 3 | Registrado (`app.dart:43`, `app.bottomsheets.dart:14`, `:21-22`) pero `showCustomSheet` **no aparece ninguna vez en `lib/`** (0 ocurrencias) y `BottomSheetType.orderInfo` sólo aparece en el archivo generado. Conserva el placeholder `'Hello Stacked Sheet!!'` (`:38`) |
| `lib/ui/dialogs/info_alert/info_alert_dialog.dart` + `_model.dart` | 107 + 3 | Registrado (`app.dart:47`, `app.dialogs.dart:15`, `:23-24`) pero `DialogType.infoAlert` sólo aparece en el generado — nunca se invoca |

#### Métodos / getters públicos sin ningún llamador

| Símbolo | archivo:línea |
|---|---|
| `DriverAuthService.signOut()` | `driver_auth_service.dart:138` (el logout de la app no lo usa) |
| `DriverSocketService.activeOrderId` (getter) | `driver_socket_service.dart:59` |
| `DriverSocketService.dispose()` | `driver_socket_service.dart:197` |
| `LocationService.dispose()` | `location_service.dart:171` |
| `LocationService.calculateDistance()` | `location_service.dart:156` |
| `LocationService.openDeviceSettings()` | `location_service.dart:151` (Home llama directo a `openAppSettings()` de `permission_handler`, `home_viewmodel.dart:186`) |
| `FcmService.dispose()` | `fcm_service.dart:180` |
| `ApiClient.put()` | `api_client.dart:105` |
| `DeliveryViewModel.isPending` | `delivery_viewmodel.dart:100` |
| `DeliveryViewModel.isCancelled` | `delivery_viewmodel.dart:104` |

(Los tres `dispose()` de servicios no se llaman nunca porque están registrados como `LazySingleton` y viven todo el proceso.)

#### Constantes sin uso

`lib/ui/common/app_strings.dart` — 12 de 20 constantes sin referencias fuera de su definición: `homeNoOrders` (:11), `homeOrderSummary` (:12), `homeOrderId` (:13), `homeOrderItems` (:14), `homeOrderTotal` (:15), `homeOrderCancel` (:16), `homeOrderReject` (:17), `homeOrderAccept` (:18), `homeOrderStartDelivery` (:19), `homeOrderReadyForDelivery` (:20), `loginViewNoAccount` (:7), `loginViewSignup` (:8).

`lib/ui/common/app_colors.dart` — sin uso: `kcPrimaryColorDark` (:4), `kcLightGrey` (:7), `kcBackgroundColor` (:9); `kcDarkGreyColor` (:5) sólo se usa para definir `kcBackgroundColor`.

`lib/ui/common/ui_helpers.dart` (90 líneas, plantilla de Stacked) — sin uso: `horizontalSpaceMedium` (:13), `horizontalSpaceLarge` (:14), `verticalSpaceMassive` (:20), `spacedDivider` (:22), `verticalSpace` (:30), `screenWidth` (:32) y `screenHeight` (:33) salvo como internos, `screenHeightFraction` (:35), `halfScreenWidth` (:51), `thirdScreenWidth` (:54), `quarterScreenWidth` (:57), `getResponsiveHorizontalSpaceMedium` (:60) y toda la familia `getResponsive*FontSize` (:62-75).

#### Bloques comentados de más de 5 líneas

| Ubicación | Líneas | Contenido |
|---|---|---|
| `lib/ui/views/home/home_viewmodel.dart:81-86` | 6 | El `@override void onError(error)` del `StreamViewModel` entero, comentado — incluye el `permissionMessage = 'Error al obtener la ubicación'` que nunca se setea |

(Único bloque >5 líneas. `app_strings.dart:21-22` son 2 constantes comentadas: `homeOrderPaymentMethod` y `homeOrderSelectAddress`.)

#### TODO / FIXME

| archivo:línea | Texto |
|---|---|
| `home_view.dart:69` | `// TODO: Navegar a la vista de cuenta` (ListTile "Cuenta" — sólo cierra el drawer) |
| `home_view.dart:77` | `// TODO: Navegar a la vista de historial` |
| `home_view.dart:88` | `// TODO: Navegar a la vista de ayuda` |
| `delivery_viewmodel.dart:39-40` | TODO para alinear `splg_lib` con `OrderResponseDto` (`GasCylinder.isActive` requerido y `weight` tipado `String`) |
| `order_offer_dialog.dart:163-165` | Referencia a ese TODO: el shape de cada item no está confirmado con el backend |

**Cero `FIXME`, `HACK` o `XXX` en `lib/`.**

#### Handlers vacíos (UI sin acción)

| archivo:línea | Elemento |
|---|---|
| `home_view.dart:25` | `IconButton` de notificaciones: `onPressed: () {}` |
| `login_view.dart:107` | "olvidé mi contraseña": `onPressed: viewModel.isBusy ? null : () {}` |

---

### TABLA 7 — Configuración

| Aspecto | Hecho verificado | archivo:línea |
|---|---|---|
| **¿Hay `.env`?** | **No.** `find` por `.env*` / `*.env*` en el repo: cero resultados. No se usa `flutter_dotenv` (no está en `pubspec.yaml`) | — |
| **¿Hay flavors?** | **No.** No hay `main_dev.dart` / `main_prod.dart`, ni `productFlavors` en `android/app/build.gradle.kts`, ni schemes por flavor en iOS | — |
| **Cómo se configura entonces** | Por **`--dart-define` en tiempo de compilación**, con una sola variable | `core/config/app_config.dart:21-24` |
| **Variable que espera la app** | `API_BASE_URL` — host + puerto del backend **sin** el sufijo `/api`. Default: `http://10.0.2.2:3000` (localhost del host visto desde el emulador Android) | `app_config.dart:21-24` |
| Derivadas | `AppConfig.apiUrl` = `{API_BASE_URL}/api/` (REST, base de Dio en `api_client.dart:21`); `AppConfig.driversNamespace` = `{API_BASE_URL}/drivers` (Socket.IO) | `app_config.dart:27`, `:30` |
| Invocación documentada | `flutter run --dart-define=API_BASE_URL=http://192.168.0.20:3000` (dispositivo físico) · `flutter build apk --dart-define=API_BASE_URL=https://api.splg.app` (prod) | `app_config.dart:7-14` |
| Timeouts HTTP | `connectTimeout` y `receiveTimeout` de 10s, hardcodeados | `api_client.dart:22-23` |
| Header fijo de identificación | `X-Client-Source: driver-app` en los 4 verbos | `api_client.dart:42`, `:67`, `:93`, `:118` |
| Logging de requests | `PrettyDioLogger` **siempre activo** (sin guarda por `kDebugMode`), con `requestHeader: true` y `requestBody: true` — imprime el `Authorization: Bearer` en consola también en release | `api_client.dart:25-32` |
| **Firebase** | `lib/firebase_options.dart` (68) con las claves de `splg-gas` **commiteado en el repo**; también están commiteados `android/app/google-services.json` y `ios/Runner/GoogleService-Info.plist` (confirmado con `git ls-files`) | `firebase_options.dart:52-67`, `firebase.json` |
| **Google Maps API key** | **Hardcodeada en el manifest** (no por dart-define ni por `local.properties`), en un archivo versionado: `AIzaSyAO7FzDH4ew11XoVXuZXvjehTkLQS2QxOA` | `android/app/src/main/AndroidManifest.xml:45-46` |
| ¿Falta algo en el repo? | **No falta ningún archivo de configuración.** `.gitignore` no excluye los archivos de Firebase. Lo único no versionado es `android/local.properties` (rutas de SDK, se regenera solo) | `.gitignore` |
| Dependencia local | `splg_lib` por path `../splg-lib`; el directorio hermano **existe** | `pubspec.yaml:40-41` |
| Application id / bundle | Android label `SPLG Chofer`; bundle iOS `com.nahuelwagner.splg.driver` | `AndroidManifest.xml:12`, `firebase_options.dart:66` |
| Versión | `pubspec.yaml:5` → `1.0.0+1`; `android/local.properties` → `flutter.versionName=0.1.0`, `minSdkVersion=23` | — |
| Tests presentes | `test/golden/` (1), `test/helpers/` (2), `test/services/` (2), `test/viewmodels/` (6) | — |
| CI | `.github/workflows/release.yml` + `scripts/release-notes.sh` y `scripts/version.sh` (changelog por commits convencionales) | — |

#### Qué hace falta para que la app corra

1. **Nada que falte en el repo.** `flutter analyze` pasa con 12 issues y **0 errores**; `flutter pub get` resuelve (incluida la dependencia por path `../splg-lib`, presente).
2. **Backend accesible en `API_BASE_URL`.** Sin `--dart-define` apunta a `http://10.0.2.2:3000`, que sólo funciona en emulador Android contra un backend en `localhost:3000` del host. En dispositivo físico o en producción hay que pasar `--dart-define=API_BASE_URL=...` (`app_config.dart:21-24`). Debe exponer REST en `/api/` y el namespace Socket.IO `/drivers`.
3. **Un usuario de chofer real**: existente en Firebase Auth del proyecto `splg-gas` **y** en la tabla de usuarios del backend, con `role.type` = `delivery` o `super_admin`, o el login se revierte (`driver_auth_service.dart:87-91`).
4. **Permisos concedidos en el dispositivo**: ubicación (incl. background para el foreground service) y notificaciones (Android 13+).
5. **Pendiente conocido para iOS**: el certificado APNs `.p8` no está subido en Firebase Console, así que el push real en iOS no funciona (`fcm_service.dart:39-42`). Android no depende de eso.
6. Emulador: `EnableImpeller` está en `false` en el manifest (`AndroidManifest.xml:42-44`).
