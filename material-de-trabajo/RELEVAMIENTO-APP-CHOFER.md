# Relevamiento factual — App del chofer (Flutter)

Repo: `/Users/nahuelwagner/Desktop/myprojects/gearthlogic/projects/garrafitas/splg-app-chofer`
Rama: `develop` · Working tree limpio (`git status --short` sin salida)
38 archivos `.dart` en `lib/`, 5.183 líneas totales.
Verificación de compilación: `flutter analyze` → **12 issues, ninguno error** (10 info + 2 warnings, los 2 warnings en `test/`).

Todas las referencias `archivo:línea` de este informe fueron leídas del archivo.

---

## TABLA 1 — Pantallas (`lib/ui/views/`)

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

## TABLA 2 — Arquitectura

**Patrón: MVVM con Stacked** (`stacked: ^3.4.0`, `stacked_services: ^1.1.0` en `pubspec.yaml:11-12`). Declaración única en `lib/app/app.dart:20-51` con `@StackedApp` (rutas, dependencias, bottomsheets, dialogs); el generador produce `app.router.dart` (471), `app.locator.dart` (42), `app.dialogs.dart` (30) y `app.bottomsheets.dart` (26), todos marcados `GENERATED CODE - DO NOT MODIFY BY HAND`.

| Carpeta | Contenido real | Rol |
|---|---|---|
| `lib/app/` | `app.dart` (fuente de verdad) + 4 archivos generados | Wiring: rutas, DI (get_it vía `StackedLocator`), builders de dialogs/sheets |
| `lib/core/` | `core/config/app_config.dart` (31), `core/network/api_client.dart` (128) | Configuración de entorno y cliente HTTP |
| `lib/services/` | 7 servicios: `driver_auth_service.dart` (145), `driver_socket_service.dart` (202), `location_service.dart` (175), `fcm_service.dart` (184), `foreground_service.dart` (110), `order_service.dart` (153), `navigation_launcher.dart` (36) | Acceso a datos + integraciones de plataforma |
| `lib/ui/` | `views/` (6 pantallas), `dialogs/` (2), `bottom_sheets/` (1), `common/` (`app_colors.dart` 9, `app_strings.dart` 22, `ui_helpers.dart` 90) | Presentación |

**Registro en el locator** (`lib/app/app.locator.dart:33-41`): `BottomSheetService`, `DialogService`, `NavigationService`, `OrderService`, `LocationService`, `DriverSocketService`, `DriverAuthService`, `DriverForegroundService`, `FcmService` — todos `LazySingleton`.

### Cómo resuelve el acceso a datos (no hay `data/` ni `domain/`)

Confirmado: no existen `lib/data/` ni `lib/domain/`. El acceso a datos se resuelve así:

1. **Un único cliente HTTP singleton manual**, no inyectado: `ApiClient` con `static final instance = ApiClient._()` y `factory ApiClient()` (`api_client.dart:9-15`). Expone `get/post/patch/put` genéricos (`:34`, `:53`, `:79`, `:105`) que devuelven el `Response` de Dio crudo. **No está registrado en el locator**; los consumidores lo instancian directamente: `final _apiClient = ApiClient();` en `driver_auth_service.dart:22`, `fcm_service.dart:44`, `home_viewmodel.dart:26` y `delivery_viewmodel.dart:46`.
2. **No hay repositorios ni DTOs propios**. Los ViewModels arman la URL, el body y los headers ellos mismos y parsean el `Map` crudo de la respuesta. Ejemplos: `home_viewmodel.dart:352-357` (aceptar pedido), `delivery_viewmodel.dart:161-174` (traer pedido).
3. **No se usa el modelo compartido para parsear.** `DeliveryViewModel` parsea a mano sobre el `Map` (`delivery_viewmodel.dart:99-143`) y el propio doc-comment explica por qué: `Order.fromJson` de `splg_lib` no calza con `GET /orders/:id` (`gas_cylinder` sin `isActive`, `weight` numérico vs `String`) — `delivery_viewmodel.dart:32-40`.
4. **`splg_lib`** (dependencia por path, `pubspec.yaml:40-41`; el directorio hermano `../splg-lib` existe) se usa sólo para el tema (`AppTheme` en `main.dart:6,36-37`) y para los modelos de `OrderService` (`order_service.dart:1-6`) — que es código muerto (Tabla 6).
5. **Separación real**: se respeta en Home, Delivery, Login, Legal y Startup — las Views no hacen red ni tocan servicios, todo pasa por el VM. **Rupturas verificadas**: `home_viewmodel.dart:26` y `delivery_viewmodel.dart:46` hacen llamadas HTTP directas desde el ViewModel (no hay capa intermedia), y `DriverAuthService` se resuelve lazy con un getter en lugar de campo, a propósito, porque `FirebaseAuth.instance` rompería los tests (`home_viewmodel.dart:29-34`, `delivery_viewmodel.dart:52-54`).

---

## TABLA 3 — El flujo del reparto, paso a paso

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

## TABLA 4 — Tiempo real y ubicación (`lib/services/`)

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

## TABLA 5 — Manejo de errores

### Dónde SÍ se muestra el error al usuario

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

### `catch` vacío o sólo log/print

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

### Pasos del reparto SIN manejo de error visible para el chofer

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

## TABLA 6 — Código muerto y restos

### Archivos sin referencias funcionales

| Archivo | Líneas | Evidencia |
|---|---|---|
| `lib/services/order_service.dart` | 153 | **Devuelve 6 pedidos hardcodeados tras `Future.delayed(2s)`** (`:16-147`). Referencias en todo `lib/`: sólo `app.dart:34` y `app.locator.dart:36` (registro). Ningún ViewModel lo inyecta. `init()` (`:12`) y `remove()` (`:149`) nunca se llaman |
| `lib/ui/views/directions/directions_view.dart` + `directions_viewmodel.dart` | 29 + 3 | Ruta registrada (`app.dart:25`, `app.router.dart:27`, `:48`, `:81-87`) y helpers generados `navigateToDirectionsView` (`app.router.dart:306`) / `replaceWithDirectionsView` (`:416`), pero **ninguno tiene llamador** fuera del archivo generado |
| `lib/ui/bottom_sheets/order_info/order_info_sheet.dart` + `_model.dart` | 59 + 3 | Registrado (`app.dart:43`, `app.bottomsheets.dart:14`, `:21-22`) pero `showCustomSheet` **no aparece ninguna vez en `lib/`** (0 ocurrencias) y `BottomSheetType.orderInfo` sólo aparece en el archivo generado. Conserva el placeholder `'Hello Stacked Sheet!!'` (`:38`) |
| `lib/ui/dialogs/info_alert/info_alert_dialog.dart` + `_model.dart` | 107 + 3 | Registrado (`app.dart:47`, `app.dialogs.dart:15`, `:23-24`) pero `DialogType.infoAlert` sólo aparece en el generado — nunca se invoca |

### Métodos / getters públicos sin ningún llamador

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

### Constantes sin uso

`lib/ui/common/app_strings.dart` — 12 de 20 constantes sin referencias fuera de su definición: `homeNoOrders` (:11), `homeOrderSummary` (:12), `homeOrderId` (:13), `homeOrderItems` (:14), `homeOrderTotal` (:15), `homeOrderCancel` (:16), `homeOrderReject` (:17), `homeOrderAccept` (:18), `homeOrderStartDelivery` (:19), `homeOrderReadyForDelivery` (:20), `loginViewNoAccount` (:7), `loginViewSignup` (:8).

`lib/ui/common/app_colors.dart` — sin uso: `kcPrimaryColorDark` (:4), `kcLightGrey` (:7), `kcBackgroundColor` (:9); `kcDarkGreyColor` (:5) sólo se usa para definir `kcBackgroundColor`.

`lib/ui/common/ui_helpers.dart` (90 líneas, plantilla de Stacked) — sin uso: `horizontalSpaceMedium` (:13), `horizontalSpaceLarge` (:14), `verticalSpaceMassive` (:20), `spacedDivider` (:22), `verticalSpace` (:30), `screenWidth` (:32) y `screenHeight` (:33) salvo como internos, `screenHeightFraction` (:35), `halfScreenWidth` (:51), `thirdScreenWidth` (:54), `quarterScreenWidth` (:57), `getResponsiveHorizontalSpaceMedium` (:60) y toda la familia `getResponsive*FontSize` (:62-75).

### Bloques comentados de más de 5 líneas

| Ubicación | Líneas | Contenido |
|---|---|---|
| `lib/ui/views/home/home_viewmodel.dart:81-86` | 6 | El `@override void onError(error)` del `StreamViewModel` entero, comentado — incluye el `permissionMessage = 'Error al obtener la ubicación'` que nunca se setea |

(Único bloque >5 líneas. `app_strings.dart:21-22` son 2 constantes comentadas: `homeOrderPaymentMethod` y `homeOrderSelectAddress`.)

### TODO / FIXME

| archivo:línea | Texto |
|---|---|
| `home_view.dart:69` | `// TODO: Navegar a la vista de cuenta` (ListTile "Cuenta" — sólo cierra el drawer) |
| `home_view.dart:77` | `// TODO: Navegar a la vista de historial` |
| `home_view.dart:88` | `// TODO: Navegar a la vista de ayuda` |
| `delivery_viewmodel.dart:39-40` | TODO para alinear `splg_lib` con `OrderResponseDto` (`GasCylinder.isActive` requerido y `weight` tipado `String`) |
| `order_offer_dialog.dart:163-165` | Referencia a ese TODO: el shape de cada item no está confirmado con el backend |

**Cero `FIXME`, `HACK` o `XXX` en `lib/`.**

### Handlers vacíos (UI sin acción)

| archivo:línea | Elemento |
|---|---|
| `home_view.dart:25` | `IconButton` de notificaciones: `onPressed: () {}` |
| `login_view.dart:107` | "olvidé mi contraseña": `onPressed: viewModel.isBusy ? null : () {}` |

---

## TABLA 7 — Configuración

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

### Qué hace falta para que la app corra

1. **Nada que falte en el repo.** `flutter analyze` pasa con 12 issues y **0 errores**; `flutter pub get` resuelve (incluida la dependencia por path `../splg-lib`, presente).
2. **Backend accesible en `API_BASE_URL`.** Sin `--dart-define` apunta a `http://10.0.2.2:3000`, que sólo funciona en emulador Android contra un backend en `localhost:3000` del host. En dispositivo físico o en producción hay que pasar `--dart-define=API_BASE_URL=...` (`app_config.dart:21-24`). Debe exponer REST en `/api/` y el namespace Socket.IO `/drivers`.
3. **Un usuario de chofer real**: existente en Firebase Auth del proyecto `splg-gas` **y** en la tabla de usuarios del backend, con `role.type` = `delivery` o `super_admin`, o el login se revierte (`driver_auth_service.dart:87-91`).
4. **Permisos concedidos en el dispositivo**: ubicación (incl. background para el foreground service) y notificaciones (Android 13+).
5. **Pendiente conocido para iOS**: el certificado APNs `.p8` no está subido en Firebase Console, así que el push real en iOS no funciona (`fcm_service.dart:39-42`). Android no depende de eso.
6. Emulador: `EnableImpeller` está en `false` en el manifest (`AndroidManifest.xml:42-44`).
