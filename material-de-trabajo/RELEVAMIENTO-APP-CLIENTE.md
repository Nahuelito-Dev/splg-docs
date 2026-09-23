# Relevamiento factual — app cliente (Flutter)

Repositorio: `/Users/nahuelwagner/Desktop/myprojects/gearthlogic/projects/garrafitas/splg-app-cliente`
Rama: `develop` — último commit `5793d87 ci: la version se calcula sola en cada merge a main`
Paquete: `splg_customer` (`pubspec.yaml:1`), SDK Dart `>=3.0.3 <4.0.0`
Volumen: 98 archivos `.dart` en `lib/`, 10.922 líneas.

Todo dato de abajo está verificado abriendo el archivo indicado. Este informe no modificó ningún archivo del repositorio.

---

## TABLA 1 — Pantallas (`lib/ui/views/`)

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

## TABLA 2 — Arquitectura

### Patrón

**MVVM sobre el framework Stacked**, con una capa Clean parcial (`domain/repository` + `domain/usecases` + `data/repository` + `data/datasource`) que sólo cubre una parte de los flujos.

- Stacked es la base: `pubspec.yaml:11-12` (`stacked ^3.4.0`, `stacked_services ^1.1.0`), configuración en `stacked.json`, y el árbol declarativo en `lib/app/app.dart:32-75` (`@StackedApp` con `routes`, `dependencies`, `bottomsheets`, `dialogs`).
- Código generado por `stacked_generator`: `lib/app/app.locator.dart` (50), `lib/app/app.router.dart` (912), `lib/app/app.bottomsheets.dart` (38), `lib/app/app.dialogs.dart` (26), más los `*_view.form.dart` de login y signup.
- Cada vista es un `StackedView<TViewModel>` y cada VM extiende `BaseViewModel`, `ReactiveViewModel` o `FormViewModel`.

### Qué hay en cada capa

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

### Cómo se relacionan

El camino "canónico" que sí existe es:

```
View (StackedView) → ViewModel → Service (locator) → UseCase → Repository (interface)
  → RepositoryImp → RemoteDatasource → ApiClient (Dio) → backend
```

Verificado punta a punta en dos flujos:
- Pedidos: `checkout_viewmodel.dart:267` → `history_service.dart:59` (`_createOrderUseCase`) → `create_order_usecases.dart:13` → `order_repository_imp.dart:15-43` → `order_remote_datasource.dart:8-22` → `api_client.dart:52`.
- Garrafas: `order_model.dart:36` → `gas_cylinder_service.dart:21` → `fetch_gascylinders_usecases.dart:9` → `gascylinder_repository_imp.dart:13` → `gascylinder_remote_datasource.dart:8`.

### Dónde NO se respeta la separación

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

## TABLA 3 — Estado y navegación

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

## TABLA 4 — Capa de datos (`lib/data/datasource/`)

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

## TABLA 5 — Manejo de errores

### Dónde se le muestra el error al usuario

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

### `catch` vacíos, silenciosos o sólo con log

- **No hay ni un `print(`** en todo `lib/` (grep sin resultados). El logging es `log()` de `dart:developer`.
- **`catch` con el cuerpo vacío — 1 caso, y es el peor:** `map_viewmodel.dart:35-37`. Si falla la geolocalización, el `catch` está vacío y arriba, en `:14` y `:36`, quedan comentados el `_snackbarService` y su `showSnackbar('Error al obtener la ubicación.')`. El usuario ve el mapa centrado en el fallback de Buenos Aires (`map_view.dart:24`) sin ningún aviso de que no se pudo ubicar.
- **`catch (_)` que devuelven null/flag, sin avisar:** `profile_viewmodel.dart:28-30` (no hay dirección primaria), `order_api_mapper.dart:10-12` y `:22-24` (un pedido que no parsea se descarta en silencio: `continue`), `legal_viewmodel.dart:27-29` (este sí se refleja en la UI).
- **`catch` con sólo `log()` — 22 ocurrencias**, en los 8 datasources (ver TABLA 4), en los 4 repositorios (`customer_repository_imp.dart:21-23,37-39`, `gascylinder_repository_imp.dart:23-25`, `order_repository_imp.dart:38-40,66-68,90-92,105-107`), en `location_service.dart:38-40`, en `customer_service.dart:35`, `:108`, y en los 6 `catch` de `notification_service.dart` (`:40-42, :56-58, :67-70, :76-78, :88-90, :117-119`).
- **`api_client.dart` tiene cinco `try { … } catch (e) { rethrow; }`** (`:47-49, :74-76, :99-101, :119-121, :144-146`): son no-ops, no agregan nada sobre no escribir el try.

### Flujos sin ningún manejo de error visible para el usuario

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

## TABLA 6 — Tiempo real (`lib/services/order_tracking_service.dart`, 260 líneas)

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

### Qué pantallas lo consumen

`OrderTrackingService` está registrado como `LazySingleton` (`app.locator.dart:45`) y lo referencian **dos** archivos:

| Consumidor | Qué usa | Línea |
|---|---|---|
| `lib/ui/views/order_tracking/order_tracking_viewmodel.dart` | Único consumidor de los streams. En `_startRealtimeTracking` se suscribe a `driverLocationUpdates` (mueve el marcador, recalcula ETA, redibuja la ruta, reencuadra el mapa) y a `orderStatusUpdates` (actualiza el stage) y luego llama a `subscribeToOrder` | `:33`, `:417-448`; cancelación de ambas suscripciones + `disconnect()` en `dispose()` (`:821-828`); también usa `fetchOrderById` (`:396`) y `disconnect()` en cancelar/confirmar (`:343`, `:362`) |
| `lib/ui/views/qr_scan/qr_scan_viewmodel.dart` | Sólo `confirmDelivery` (HTTP), no el socket | `:18`, `:66-70` |

**No hay reconexión de aplicación**: si el VM se destruye (salir de la pantalla de tracking) el socket se cierra, y el estado del pedido fuera de esa pantalla se actualiza por **polling HTTP cada 10 segundos** desde `history_model.dart:107-113`, no por socket.

---

## TABLA 7 — Código muerto y restos

### Clases y widgets que nadie usa

| Elemento | Archivo | Verificación |
|---|---|---|
| `Market` (widget) | `lib/ui/widgets/common/market/market.dart` (23) | `builder` devuelve `const SizedBox.shrink()` (`:15`). Grep de `Market` fuera de su carpeta: **0 resultados**. No está en `home_view.dart` |
| `MarketModel` | `lib/ui/widgets/common/market/market_model.dart` (3) | Clase vacía, sólo usada por `Market` |
| `BusinessHours` + `_BusinessHours` | `lib/domain/business_hours.dart` (66) | Grep de `BusinessHours` fuera del archivo: **0 resultados**. Es el modelo del selector de rango horario libre, reemplazado por las franjas fijas (`TimeSlotAvailability`) |
| `NoticeSheet` / `NoticeSheetModel` | `lib/ui/bottom_sheets/notice/notice_sheet.dart` (53) + `notice_sheet_model.dart` (3, clase vacía) | Registrado en `app.dart:65` y `app.bottomsheets.dart:27-28`, pero `BottomSheetType.notice` **nunca se invoca**: los 3 `showCustomSheet` del repo usan `addressList` (`checkout_viewmodel.dart:62`), `rateDriver` (`order_tracking_viewmodel.dart:375`) y `claim` (`history_model.dart:75`) |
| `InfoAlertDialog` / `InfoAlertDialogModel` | `lib/ui/dialogs/info_alert/info_alert_dialog.dart` (107) + `info_alert_dialog_model.dart` (3, clase vacía) | Registrado en `app.dart:72` y `app.dialogs.dart:21-22`, pero **`showCustomDialog` no se llama nunca** (grep: 0 resultados). Todos los diálogos usan `showDialog`/`showConfirmationDialog` genéricos |

### Métodos y campos sin uso

| Elemento | Archivo:línea | Verificación |
|---|---|---|
| `HistoryService.addOrder(Order)` | `history_service.dart:45-47` | Wrapper de `createOrder`. Grep de `addOrder`: sólo la definición |
| `HistoryService.hasPendingOrder` (getter) | `history_service.dart:35` | `_hasPendingOrder` se escribe en `:70, :101, :138, :153`, pero el getter no se lee desde ningún otro archivo |
| `GasCylinderService.gasCylinder` (getter) | `gas_cylinder_service.dart:18` | La caché `_gasCylinder` se usa internamente; el getter no lo lee nadie fuera del servicio |
| `AddressesViewModel.actionError` | `addresses_viewmodel.dart:16` | Se escribe en `:31, :39, :46` y no se lee en ninguna parte (ver TABLA 5) |
| `OrderTrackingViewModel._arrivingNotified` | `order_tracking_viewmodel.dart:60` | Sólo se escribe (`:578-580`); nunca se lee. Es el resto de una notificación de llegada que no se implementó |
| `MapViewModel._controllerComparer` | `map_viewmodel.dart:18` | Se completa en `:44` y nunca se hace `.future`. El controller real se guarda aparte en `_mapController` (`:19, :45`) |
| `PaymentMethod.online` vs `PaymentMethod.mercadoPago` | `checkout_viewmodel.dart:172` vs `:276` | El recargo del 10% se aplica cuando el método es `online` (`:171-176`), pero el checkout de MercadoPago se dispara cuando es `mercadoPago` (`:276`). Son dos valores distintos del enum de `splg_lib` (`../splg-lib/lib/domain/order.dart:127-137`) |

### Constantes sin uso — `lib/ui/common/app_strings.dart`

16 de 32 constantes no se referencian en ninguna parte fuera del propio archivo: `signupViewRepeatPassword`, `signupViewPhone`, `signupViewAddress`, `signupViewVerificationCode`, `signupViewResendCode`, `signupViewAddressHint`, `signupViewFinishButton`, `signupViewBack`, `signupViewSendCode`, `signupViewVerifyCode`, `signupViewVaildPasswordError`, `signupViewVaildRepeatPasswordError`, `signupViewVaildPasswordNotEqualError`, `signupViewDialogOtpTitle`, `signupViewDialogOtpDescription`, `signupViewDialogOtpConfirm`, `signupViewDialogOtpCancel`. El grupo OTP (5 constantes, `:33-37`) es el resto de un flujo de verificación por SMS que no existe en el código.

### Helpers sin uso — `lib/ui/common/ui_helpers.dart` (90 líneas, plantilla de Stacked)

Sin ninguna referencia fuera del archivo: `horizontalSpaceTiny`, `horizontalSpaceMedium`, `horizontalSpaceLarge`, `verticalSpaceMassive`, `spacedDivider`, `verticalSpace()`, `screenWidth()`, `screenHeight()`, `screenHeightFraction()`, `screenWidthFraction()`, `halfScreenWidth()`, `thirdScreenWidth()`, `quarterScreenWidth()`, `getResponsiveHorizontalSpaceMedium()` y las 6 funciones `getResponsive*FontSize()`. Los únicos usados son `horizontalSpaceSmall` (3), `verticalSpaceTiny` (4), `verticalSpaceSmall` (4), `verticalSpaceMedium` (7) y `verticalSpaceLarge` (1), todos en los 4 bottom sheets, el dialog y `startup_view.dart`.

### TODO / FIXME

Sólo **2** en todo `lib/` (no hay ningún `FIXME`, `HACK` ni `XXX`):

1. `lib/services/order_tracking_service.dart:29` — `// TODO(config): centralizar esta base junto a la de ApiClient por entorno.` Es la causa de que la URL del socket esté fija en `localhost:3000`.
2. `lib/ui/views/qr_scan/qr_scan_viewmodel.dart:32-36` — TODO de 5 líneas sobre que un 400 del backend no distingue "código de otro pedido" de "código mal escrito" cuando hay más de un pedido `on_the_way`.

### Bloques comentados de más de 5 líneas

El escaneo devuelve 9 bloques de ≥5 líneas consecutivas de comentario. **Ocho de los nueve son documentación válida** (dartdoc de clases y métodos): `firebase_options.dart:7-16` (ejemplo generado por FlutterFire), `create_order_result.dart:3-8`, `payment_outcome.dart:1-5`, `notification_service.dart:11-21`, `app_config.dart:1-6`, `checkout_viewmodel.dart:297-302`, `payment_webview_viewmodel.dart:9-18` y `:51-55`, `qr_scan_viewmodel.dart:29-36` (el TODO de arriba).

**Código realmente comentado — 1 caso, de 2 líneas** (queda bajo el umbral de 5 pero es el único código muerto comentado del repo): `map_viewmodel.dart:14` (`//final _snackbarService = locator<SnackbarService>();`) y `:36` (`//_snackbarService.showSnackbar(message: 'Error al obtener la ubicación.');`).

### Archivos que ningún import referencia

| Archivo | Situación |
|---|---|
| `lib/domain/business_hours.dart` | Ningún import lo trae. Huérfano total |
| `lib/ui/widgets/common/market/market.dart` + `market_model.dart` | `market.dart` importa a `market_model.dart`, pero nadie importa `market.dart`. Par huérfano |
| `lib/ui/bottom_sheets/notice/notice_sheet.dart` + `notice_sheet_model.dart` | Importados sólo por el código generado (`app.bottomsheets.dart:13`, `app.dart:1`), nunca invocados en runtime |
| `lib/ui/dialogs/info_alert/info_alert_dialog.dart` + `info_alert_dialog_model.dart` | Idem: importados por `app.dialogs.dart:11` y `app.dart:2`, nunca invocados |

---

## TABLA 8 — Configuración

### ¿Hay `.env` o archivos por flavor?

**No.** `find` de `*.env*` (excluyendo `build/` y `.git/`) no devuelve nada: no hay `.env`, `.env.example`, `.env.dev`, ni `flutter_dotenv` en `pubspec.yaml`. Tampoco hay `productFlavors` en `android/app/build.gradle*` ni schemes/xcconfig por entorno en `ios/`. No existe `.vscode/launch.json` con `--dart-define`; `.vscode/` sólo tiene `settings.json`.

La configuración por entorno se resuelve **sólo con `--dart-define`**, leída en `lib/core/config/app_config.dart` con `String.fromEnvironment` y valores por defecto embebidos.

### Variables que la app espera

| Variable | Default si no se pasa | Dónde se lee | Dónde se usa |
|---|---|---|---|
| `API_BASE_URL` | `http://localhost:3000` | `app_config.dart:11-14` | `AppConfig.apiUrl` = `$API_BASE_URL/api/` (`:17`) → `baseUrl` de Dio (`api_client.dart:19`) |
| `DISTRIBUTOR` | `jeny-gas` | `app_config.dart:23-26` | Header `X-Distributor` en los 5 verbos (`api_client.dart:41,67,93,113,137`) y query `?distributor=` de franjas (`time_slot_remote_datasource.dart:15`) |
| `MP_SUCCESS_URL` | `https://splg.app/pago/exito` | `app_config.dart:32-35` | Detección de retorno en el WebView (`payment_webview_viewmodel.dart:66`) |
| `MP_FAILURE_URL` | `https://splg.app/pago/error` | `app_config.dart:36-39` | `payment_webview_viewmodel.dart:67` |
| `MP_PENDING_URL` | `https://splg.app/pago/pendiente` | `app_config.dart:40-43` | `payment_webview_viewmodel.dart:68` |

Los tres `MP_*` tienen que coincidir con `MP_SUCCESS_URL` / `MP_FAILURE_URL` / `MP_PENDING_URL` del backend; lo dice el comentario de `app_config.dart:28-31`.

**Variable que falta y no se puede configurar:** la URL del socket. `order_tracking_service.dart:30` la tiene hardcodeada en `http://localhost:3000/customers` y no pasa por `AppConfig`. Contra un backend que no sea `localhost:3000`, el HTTP apunta bien (por `API_BASE_URL`) pero el tiempo real no conecta. En emulador Android, además, `localhost` tampoco resuelve al host (hace falta `10.0.2.2`, según el propio comentario de `:27-28`).

### Archivos de configuración presentes y versionados

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

### API keys embebidas en el repositorio

- **Google Maps Android:** `AIzaSyAvywoBGIhVqoWUn-MhybUea1oXIoKgtp8` en `android/app/src/main/AndroidManifest.xml:37-38`.
- **Google Maps iOS:** la **misma** clave, `AIzaSyAvywoBGIhVqoWUn-MhybUea1oXIoKgtp8`, en `ios/Runner/AppDelegate.swift:11` (`GMSServices.provideAPIKey(...)`).
- **Firebase Android:** `AIzaSyCINEEptz-g3DX_vVkn1RfKftGNHtqwCas` (`lib/firebase_options.dart:53`).
- **Firebase iOS:** `AIzaSyAZE8JBLkpd2PjrdV5lNxwJLLMXinNe7oU` (`lib/firebase_options.dart:61`).

El `.gitignore` (703 B) no excluye `google-services.json`, `GoogleService-Info.plist` ni `firebase_options.dart`.

### Dependencia local

`pubspec.yaml:41-42` declara `splg_lib` con `path: ../splg-lib`. El directorio existe (`/Users/.../garrafitas/splg-lib`, con `lib/`, `pubspec.yaml`, `test/`) y de ahí salen `Order`, `OrderStatus`, `PaymentMethod`, `Customer`, `Address`, `GasCylinder`, `Discount`, `OrderItem` y el tema (`splg_lib/theme/app_theme.dart`, usado en `main.dart:7,35-36`).

### Qué hace falta para que la app corra

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

## Apéndice — Tests presentes

`test/` (no forma parte del pedido, se lista por completitud): `test/golden/home_view_golden_test.dart`, `test/helpers/test_helpers.dart` + `.mocks.dart`, `test/services/` (5: cart, customer, gas_cylinder, history, location), `test/viewmodels/` (9: address_list_sheet_model, checkout, home, info_alert_dialog_model, login, map, notice_sheet_model, profile, signup) y `test/widget_models/` (5: account, history, market, order, profile). Dev deps: `mockito ^5.4.1`, `golden_toolkit ^0.15.0`, `build_runner`, `stacked_generator` (`pubspec.yaml:64-72`).

Nota: hay tests para tres piezas que la app no usa en runtime — `market_model_test.dart`, `notice_sheet_model_test.dart` e `info_alert_dialog_model_test.dart` (ver TABLA 7). Tampoco hay test para las 3 vistas más grandes: order_tracking, qr_scan y payment_webview.
