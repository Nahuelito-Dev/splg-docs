# Plan — app cliente SPLG con el diseño de Tutu pasajero (tanda 2)

Fecha: 10/10/2026. Es un análisis: no se tocó ningún repo.

**Fuentes**
- Tutu pasajero: `tutu-dev/tutu_app/lib/pages/**` y `tutu-dev/tutu_app_packages/lib/**`.
- Cliente SPLG: `.worktrees/splg-app-cliente/marca-brasa`, con su `.orq/ENTREGA.md` leído.
- Lib: `.worktrees/splg-lib/marca-brasa/lib`.
- Back: `splg-app-backend/src`, probado en vivo en `:3010`.
- Figma: `capturas-apps/referencias-figma/customer/{s1,s3,s4,f1,f6,f8,f17}.png`.
- CU: `splg-docs/Casos-de-Uso.md`.

**Criterio**
- De Tutu se toma la distribución, los componentes, los espaciados y los degradés.
- Colores Brasa (`context.brasa`, `SplgGradients`) y fuente Geist, que ya está en la lib.
- Íconos: `SplgIcons` (Phosphor). Ilustraciones: `SplgIllustration` (3dicons, CC0).
- Tanda 2 es lo básico; tanda 3 es lo complejo (mapa/GPS, QR, MP, envases y push).

## 0. Cómo se verificaron los endpoints

- Base: `http://localhost:3010/api`. Headers: `X-Client-Source: customer-app` y `X-Distributor: demo`. Token: `POST /auth/login` con `cliente@splg.com`.
- Estado de cada endpoint en la tabla:
  - **200/201/302**: responde con datos.
  - **400 val.**: se llamó con un cuerpo vacío y el back devolvió errores de validación. El rol pasa y la ruta existe, pero no se crearon datos.
  - **404 id**: se llamó con un UUID inexistente. El rol pasa.
  - **403**: el cliente no tiene acceso.
- No se creó ni se modificó nada en la base. La única excepción es un `PATCH /users/:id` con `{}`, que no cambia nada.

**Dos trampas que conviene anotar en el brief**
- `GET /orders/customer/:customerId` recibe el **`user_id`**, no el `customer_id`. Con el `customer_id` responde **403** "No autorizado a ver pedidos de otro cliente". La app ya hace lo correcto: `Customer.customerId` mapea `user_id`.
- `PATCH /orders/:id/cancel` exige `Idempotency-Key` en formato **UUID v4**. Si no lo es, responde 400.

## 1. Tabla de pantallas de Tutu pasajero → SPLG

Las rutas de Tutu son relativas a `tutu_app/lib/pages/`. Las de SPLG son relativas a `splg-app-cliente/lib/ui/`. Cuando la pantalla de SPLG dice **nueva**, no existe hoy.

### Arranque, autenticación y alta (Figma s1)

| Tutu (archivo / widget) | SPLG equivalente | CU | Endpoints (verificados) | Tanda |
|---|---|---|---|---|
| `splashscreen/splashscreen.page.dart` (`SplashRoutePage`) | `views/startup/startup_view.dart`: rehacer con `SplgGradients.splash` y `SplgLogo` blanco centrado | CU-091 | `POST /auth` **201** (valida el token) | 2 |
| `splashscreen/widget/welcome_widget.dart` (`WelcomeWidget`, "Subite, te llevamos" + Comenzar) | **nueva** `views/welcome/welcome_view.dart` ("Tu garrafa, sin salir de casa"), sólo la primera vez | — | — | 2 |
| `splashscreen/widget/permissions_widget.dart`, `permissions/expansion_tile_permision.dart`, `item_location_tile.dart` (permiso de ubicación y de llamadas) | Ubicación: ya lo resuelve `PermissionsService.ensure()` de la lib, al entrar al mapa. Llamadas: **descartar** (SPLG no pide permiso de teléfono; el `tel:` no lo necesita) | — | — | 3 |
| `splashscreen/widget/ckack_version_dialog.dart` (versión mínima) | **descartar** por ahora: el back no tiene endpoint de versión | — | — | — |
| `login/login_page.dart` (`LoginPage`, ilustración del sobre + "¡Hola!" + Gmail/iCloud) | `views/login/login_view.dart`: rehacer. Los botones de Google y Apple quedan **afuera** (el back no tiene login social) | CU-001 | `POST /auth/login` **200** | 2 |
| `login/recovery_password_page.dart` (`RecoveryPasswordPage`) | **nueva** `views/recover_password/recover_password_view.dart`. Hoy es un link con un diálogo dentro del login. Usa `SplgIllustration.recoverPassword` | CU-047 | Firebase `sendPasswordResetEmail`, como hoy (`POST /email/password-reset` **400 val.** existe pero la app no lo usa) | 2 |
| `login/password_info_page.dart` ("revisá tu correo") | **nueva** `views/recover_password/mail_sent_view.dart`, con `SplgIllustration.mailSent` | CU-047 | — | 2 |
| `register/register_page.dart` y `register_form.dart` (asistente de 3 pasos con `PageView` y puntos) | `views/signup/signup_view.dart`: rehacer en pasos | CU-002, CU-084 | `POST /users/check-exists` **200**; `POST /auth/registro` **400 val.** (pide `email`, `password` ≥6, `full_name` ≥2, `phone_number` E.164) | 2 |
| `register/widgets/personal_info.dart` (paso 1: nombre, apellido, nacimiento, género, DNI, domicilio) | Paso 1 "Tus datos": nombre completo y teléfono (+54). El DNI, el género y la fecha de nacimiento se **descartan** porque el DTO no los tiene | CU-002 | — | 2 |
| `register/widgets/account_info.dart` (paso 2: email, contraseña ×2, términos y privacidad) | Paso 2 "Tu cuenta": email, `SplgPasswordField` ×2, `CheckboxWithLink` ×2 | CU-002 | — | 2 |
| `register/widgets/location_info.dart` (domicilio, localidad, provincia) | Paso 3 opcional "Tu dirección": hace el alta de la primera dirección (ver §2.2). Si no se puede geocodificar, se saltea | CU-116, CU-058 | `POST /user-address` **400 val.** (`latitude`/`longitude` son obligatorios); `GET /coverage-zones/check?lat&lng` **200** | 2 (formulario) / 3 (con mapa) |
| `register/widgets/phone_verification.dart`, `profile/widgets/phone_otp.dart` (OTP) | **descartar**: no hay verificación de teléfono en el back | — | — | — |
| `register/widgets/header_image.dart` (cabecera con ilustración del escudo) | Usar la cabecera de ilustración de la lib (`SplgIllustrationHeader`, que falta; ver §5) | — | — | 2 |
| `approval/approval_page.dart` ("¡Registro completado!" sobre el degradé) | **nueva** `views/signup/signup_done_view.dart`. El cliente SPLG no espera aprobación: el texto es "¡Listo! Ya podés pedir". Va con `SplgIllustration.success` y "Ir al inicio" | CU-002 | — | 2 |
| `documents_info/documentation_personal.dart` y sus widgets (DNI y selfie) | **descartar**: el cliente no valida identidad. Es un flujo del chofer | — | — | — |
| `login/logout_page.dart` (confirmación de cierre de sesión sobre el degradé) | **nueva** `views/logout/logout_view.dart`, o un diálogo con el mismo estilo. Hoy es un diálogo Material | CU-001 | — (Firebase `signOut`) | 2 |
| `network/no_network.dart` (`NoNetworkPage`) | **nueva** `views/no_network/no_network_view.dart`. Cubre el pendiente "Sin red" de la ENTREGA | — | — | 2 |
| `loading_page/loading_page.dart` | Reemplazar por un `SplgLoader` dentro de cada vista | — | — | 2 |

### Inicio, menú y pedido (Figma f1, f6, s3)

| Tutu (archivo / widget) | SPLG equivalente | CU | Endpoints (verificados) | Tanda |
|---|---|---|---|---|
| `home/home_page.dart`, `home/widgets/home_map.dart`, `buttons_home.dart`, `home_button.dart` (mapa de fondo, botón de menú cuadrado con degradé arriba a la izquierda y panel inferior "Tu ubicación / ¿A dónde vamos?") | `views/home/home_view.dart`: rehacer. Se **saca el `BottomNavigationBar`** y se usa el botón de menú de Tutu (`SplgIconButton`) con un `Drawer`. En la tanda 2, sin mapa: el fondo es el **catálogo** (§2.1) y el panel inferior es "Entregar en: `<dirección predeterminada>` ×". En la tanda 3 vuelve el mapa de fondo, como en f1 | CU-041, CU-121 | `GET /gascylinder` **200** (`gasCylinders[]` con `promotions[]`); `GET /user-address/user/:userId/default` **200** | 2 (sin mapa) / 3 (mapa) |
| `home/widgets/drawer_passenger_widget.dart`, `home_drawer.dart`, `menu_widget.dart` (menú lateral sobre el degradé: Mi perfil, Mis viajes, Reservas, Destinos frecuentes, Estadísticas, Tu calificación, Ayuda, Términos, Privacidad, Acerca de, Cerrar sesión) | **nueva** `widgets/common/app_drawer/app_drawer.dart`. Ítems: Mi perfil · Mis pedidos · Mis direcciones · Pedidos programados · Mis reclamos · Notificaciones · Ayuda · Términos · Privacidad · Acerca de · Cerrar sesión. Usa `SplgGradientBackground`, `SplgMenuItem(dark: true)` y `SplgHeader(onGradient)` | — | — | 2 |
| `home/widgets/fare_confirm_banner.dart` (`FareDetailsBanner`, `OriginStopEndAddress`) | Banner del pedido en curso en el inicio ("Tu pedido está en camino → Ver"). Reemplaza a `_ActiveOrderCard` de `widgets/common/order/order.dart` | CU-006 | `GET /orders/customer/:userId` **200** (se filtra por estado en la app) | 2 |
| `fare/fare_page.dart`, `fare_draggable.dart`, `fare_estimate_draggable.dart` (Confirmación f6: direcciones con punto y ×, tarifa y tiempo, filas de opciones, filtros con radio, "Buscar conductor" / Cancelar / Reservar) | `views/checkout/checkout_view.dart`: rehacer como la **Confirmación** de f6, con el degradé oscuro de la superficie. Filas: Entregar en · Cuándo (ahora o franja) · Forma de pago · Notas. Botones: "Confirmar pedido" y "Cancelar" | CU-005, CU-044, CU-045 | `POST /orders` **400 val.** (`customerId`, `addressId`, `items[]`, `paymentMethod` cash/mercadopago/transfer; opcionales `timeSlotId`, `scheduledDate`, `notes`); `GET /time-slot/availability?date&distributor` **200** | 2 |
| `fare/widgets/fare_origin.dart`, `fare_destination_list.dart`, `fare_order.dart` | Fila de dirección de entrega (`SplgAddressPill`) que abre `bottom_sheets/address_list/address_list_sheet.dart`, rehecho | CU-127 (planificado), CU-046 | `GET /user-address/user/:userId` **200** | 2 |
| `fare/widgets/payment_selector.dart` | `views/checkout/widgets/payment_method_selector.dart`: rehacer como `SplgOptionRow` + hoja de opciones. En la tanda 2 sólo **efectivo** y **transferencia**; MercadoPago va en la 3 | CU-005 | `POST /orders` (`paymentMethod`) | 2 (MP: 3) |
| `fare/widgets/filter_radio_tile.dart` (`FilterCheckboxTile`) | Se reutiliza como `SplgRadioRow` para elegir la franja y el medio de pago | CU-044 | — | 2 |
| `fare/widgets/route_info.dart` (tarifa y tiempo) | Bloque "Total $ · Llega hoy entre 12 y 16". Incluye el recargo por zona (`zone_surcharge`) cuando lo hay | CU-005 | — | 2 |
| `adress_trip_page/address_list_page.dart`, `widgets/adress_list.dart`, `adress_origin.dart`, `select_favs.dart`, `confirm_adress_button.dart` (elegir origen y destino entre favoritos) | Selector de la dirección de entrega del pedido: `bottom_sheets/address_list/` | CU-046, CU-121 | `GET /user-address/user/:userId` **200** | 2 |
| `adress_trip_page/widgets/map_selecion_destination.dart` (elegir en el mapa) | `views/map/map_view.dart`: rehacer con el mapa | CU-116 | `POST /user-address`; `GET /coverage-zones/check` | 3 |
| `favorite/favorite_page.dart`, `favorite_item.dart`, `icon_selector.dart` (favoritos con ícono: casa, trabajo…) | `views/addresses/addresses_view.dart` → **Mis direcciones** (§2.2). El selector de ícono se **descarta** porque el back no guarda una etiqueta | CU-046, CU-117–CU-121 | `GET /user-address/user/:userId` **200**; `PATCH /user-address/:id` **404 id**; `PATCH /user-address/:id/set-default` **404 id**; `DELETE /user-address/:id` **404 id** | 2 |
| `frequent_trips/frequent_trips_page.dart`, `frequent_trip_card.dart` | **descartar**. Si nahue lo quiere, se podría convertir en "Repetir pedido" desde el detalle, pero no hay CU | — | — | — |
| `mercadopago/mp_webview_payment.dart`, `checkout/dialog/pay_success_dialog.dart` | `views/payment_webview/payment_webview_view.dart`: rehacer. Más un diálogo nuevo "Pago aprobado" | CU-005 (MP), SS-14 | (crea la preferencia `POST /orders` con `mercadopago`) | 3 |
| `wallet_connect/wallet_connect_page.dart` (vincular billetera) | **descartar** | — | — | — |

### Seguimiento, entrega y calificación (Figma f8, f17, s4)

| Tutu (archivo / widget) | SPLG equivalente | CU | Endpoints (verificados) | Tanda |
|---|---|---|---|---|
| `trip/trip_view.dart`, `trip/widgets/ride_widget.dart`, `widgets/ride_info_widget.dart`, `widgets/driver_profile.dart` (f8: mapa, barra "Llegando en", tarjeta con patente, conductor, chat y llamada, tarifa y pago) | `views/order_tracking/order_tracking_view.dart`. En la tanda 2 se rehace **la hoja inferior sin mapa**: estado (`_TrackingStepper`), tarjeta del repartidor (`_DriverCard` → `SplgDriverCard`, con patente de `vehicle`, nombre y botón llamar `tel:`), total y forma de pago. Se mantiene el socket que ya existe. Tanda 3: mapa en vivo con la ruta | CU-006, CU-021 | `GET /orders/:id` **200** (`status`, `delivery_name`, `vehicle`, `on_the_way_at`, `order_items`, `total_amount`…) | 2 (hoja) / 3 (mapa) |
| `trip/dialogs/searching_driver.dart` ("Buscando conductor…" sobre el degradé) | Estado `pending` del seguimiento: "Buscando repartidor…" con el mismo modal | CU-013 (lo hace el sistema) | `GET /orders/:id` | 2 |
| `trip/dialogs/search_empty_no_drivers.dart`, `trip/widgets/reintent_find_driver.dart`, `find_driver.dart` | **descartar**: en SPLG el pedido sigue pendiente y lo despacha el sistema; no hay "reintentar" | — | — | — |
| `trip/dialogs/menu_trip.dart` (s4 "Detalles del viaje": Compartir ubicación, Mensaje al conductor, Cancelar viaje) | Menú "⋯" del seguimiento: **Cancelar pedido** · **Hacer un reclamo** · **Llamar a la distribuidora**. Compartir ubicación y el chat se **descartan** | CU-008, CU-023 | `PATCH /orders/:id/cancel` **404 id** (rol OK, pide `Idempotency-Key` v4); `POST /claims` **400 val.** | 2 |
| `trip/address_status_widget.dart`, `trip/dialogs/dialog_status_trip.dart`, `dialog.dart` | Píldora de estado con la dirección (como f8 arriba). Diálogos de cambio de estado ("Tu pedido fue aceptado", "Llegó el repartidor"); el `ArrivingBanner` ya existe | CU-019, CU-021 | (socket `/customers`) | 2 (diálogos) / 3 (push) |
| `trip/widgets/follow_button.dart` (seguir al vehículo en el mapa) | Va con el mapa en vivo | CU-017 | — | 3 |
| `trip/widgets/remainder.dart`, `details_remainder.dart` (recordatorio de reserva) | Recordatorio de un pedido programado (push) | CU-021 | — | 3 |
| `incident_travel/cancel_travel_page.dart` (s4 "Cancelar viaje": lista de motivos + Confirmar) | **nueva** `views/cancel_order/cancel_order_view.dart`: motivos con `SplgRadioRow` + "Otro" con texto → `reason`. Hoy se cancela sin motivo | CU-008 | `PATCH /orders/:id/cancel` con `{reason?}` | 2 |
| `incident_travel/incident_travel_modal.dart`, `widgets/incident_widget.dart` | Hoja de reclamo: `bottom_sheets/claim/claim_sheet.dart`, rehecha (§2.3) | CU-023 | `POST /claims` **400 val.** | 2 |
| `checkout/checkout_page.dart`, `checkout/ride_over_page.dart` (fin del viaje: resumen y pago) | **nueva** `views/order_delivered/order_delivered_view.dart`: "¡Entregado!", resumen e invitación a calificar | CU-020/079 (resultado) | `GET /orders/:id` | 2 |
| `checkout/rate_trip_dialog.dart`, `ratings/widgets/start_rating.dart`, `rate_comments.dart` (f17 "Calificá al conductor") | `bottom_sheets/rate_driver/rate_driver_sheet.dart`: rehacer como en f17, con `SplgRatingInput` y `SplgTextArea` de máximo 300 caracteres | CU-064 | `POST /ratings` **400 val.** (`orderId`, `stars` 1..5; 409 "Ya calificaste este pedido") | 2 |
| `trip/dialogs/show_rate_pending.dart` (calificación pendiente al abrir) | Al entrar al inicio: si el último pedido está `delivered` y no tiene calificación, abrir la hoja. **Falta saber si está calificado** (§4) | CU-064 | — | 2 (con el endpoint de §4) |
| `chat/chat_page.dart`, `message_bubble.dart`, `recommended_messages.dart` | **descartar**: SPLG no tiene chat. Se reemplaza por "Llamar" (`tel:`) | — | — | — |

### Historial, reservas y cuenta (Figma s3, s4)

| Tutu (archivo / widget) | SPLG equivalente | CU | Endpoints (verificados) | Tanda |
|---|---|---|---|---|
| `travels/travels_page.dart`, `widgets/trip_card.dart` (s3 "Mis viajes": tarjeta con borde, pin, fecha, insignia, valor y método) | `widgets/common/history/history.dart` → **nueva vista** `views/orders/orders_view.dart` "Mis pedidos" (`SplgOrderCard` + `SplgStatusBadge`). Vacío: `SplgEmptyState(emptyList)` | CU-007 | `GET /orders/customer/:userId?limit&offset` **200** (`{orders,total,limit,offset}`) | 2 |
| `travels/travels_details_page.dart` (s3: barra con la fecha, monto grande, conductor, direcciones, distancia) | **nueva** `views/order_detail/order_detail_view.dart`: `SplgSectionBar` con la fecha, `SplgSoftCard` con el total, ítems, dirección, repartidor y acciones (Ver seguimiento si está activo · Calificar · Reclamar · Cancelar si se puede). Hoy tocar un pedido abre directamente el seguimiento | CU-006 | `GET /orders/:id` **200** | 2 |
| `booking/booking_page.dart`, `widgets/booking_tile/*`, `new_booking_button.dart`, `booking_filter.dart` (s3/s4 "Reservas": lista + "Nueva reserva +") | **nueva** `views/scheduled/scheduled_orders_view.dart` "Pedidos programados": los pedidos con `scheduledDate` o con estado `reserved`, filtrados en la app (§2.5) | CU-044, CU-072 | `GET /orders/customer/:userId` **200** (`GET /orders/reservations` → **403**, es del admin) | 2 (por franja) / 3 (reserva con seña) |
| `booking/booking_create.dart`, `widgets/booking_form.dart`, `bookin_create_item.dart`, `booking_button_create.dart` (fecha, hora, origen y destino, filtros, Confirmar) | Formulario "Programar pedido": fecha (`SplgDateField`), franja (`SplgSelectField` con disponibilidad), dirección y producto | CU-044, CU-045 | `GET /time-slot/availability?date=YYYY-MM-DD&distributor=demo` **200** (`timeSlotId`, `name`, `startTime`, `endTime`, `remaining`); `POST /orders` con `scheduledDate`+`timeSlotId` | 2 |
| `booking/booking_summary.dart`, `widgets/booking_summary/booking_driver_profile.dart`, `bookin_cancel_button.dart` (s4 "Reserva confirmada" sobre el degradé oscuro + "Cancelar viaje") | Detalle del pedido programado = `order_detail_view` con la variante oscura (`SplgDarkCard`) + "Cancelar pedido" | CU-008 | `PATCH /orders/:id/cancel` | 2 |
| Seña de la reserva (`depositAmount`, `isReservation`) | Reserva con seña por MP | CU-072 | `POST /orders` (`isReservation`, `depositAmount`) | 3 |
| `profile/profile_page.dart`, `profile_info.dart`, `widgets/profile_title_text.dart`, `subtitule_category_widget.dart` (s3 "Mi perfil": avatar, nombre, teléfono, "Editar perfil" + lista) | `views/profile/profile_view.dart`: rehacer con `SplgProfileHeader` + `SplgMenuItem`: Información personal · Cambiar contraseña · Mis direcciones · Eliminar cuenta | CU-004 | `GET /users/email/:email` **200** (trae `customer`, `addresses`); `GET /customers/user/:userId` **200** | 2 |
| `profile/pages/personal_info_page.dart` (s3 "Información personal": `SplgInfoSection`) | **nueva** `views/profile/personal_info_view.dart`: datos personales y de la cuenta. Sin documentación (se descarta) | CU-004 | `GET /users/:id` **200** | 2 |
| `profile/pages/edit_phone_view.dart`, `widgets/suffix_validator.dart` | **nueva** `views/profile/edit_profile_view.dart`: nombre y teléfono. Reemplaza al `_ProfileField` en línea | CU-251 | `PATCH /users/:id` **200** (`full_name`, `phone_number`; `password` y `blocked` → 403 para el cliente) | 2 |
| `profile/pages/change_password_page.dart` (s3: actual, nueva, repetir; borde verde/rojo) | **nueva** `views/profile/change_password_view.dart` con `SplgPasswordField` ×3. Se hace en el cliente con Firebase (`reauthenticateWithCredential` + `updatePassword`); el back no lo permite | CU-251 | — (`PATCH /users/:id` con `password` lo rechaza para el cliente) | 2 |
| `profile/profile_picture.dart`, `widgets/catch_images/cached_profile_pic.dart` | Foto de perfil: `SplgAvatar` con iniciales en la tanda 2; subirla en la 3 (usa el permiso de fotos o de cámara) | CU-251 | `GET /users/me/photo` **404** "No tiene foto" (rol OK); `PUT /users/me/photo` **400** "Falta la foto" (rol OK) | 2 (ver) / 3 (subir) |
| "Eliminar cuenta" (s3, en Mi perfil) | Hoy `ProfileViewModel.deleteAccount()` **sólo cierra la sesión**: no borra nada | CU-085 | `DELETE /users/:id` **403** (sólo admin); `DELETE /users/me` **403** → **falta** (§4) | 2 (con el endpoint) |
| `ratings/ratings_page.dart`, `widgets/info_passenger.dart` (s3 "Mi calificación": promedio, barras y reseñas) | Se **simplifica**: en `SplgProfileHeader` va "N pedidos · ★ 4,8". La pantalla con barras y reseñas se descarta porque el detalle es del admin | CU-065 | `GET /ratings/user/:userId/summary` **200** (`{average,count}`); `GET /ratings/user/:userId` **403** | 2 (resumen) |
| `statistics/statistics_page.dart`, `components/*`, `controller/*` (gráfico de gastos) | **descartar** en la 2: no hay CU de estadísticas del cliente. Más adelante podría ser "Mi consumo" + la recompra estimada (CU-146, planificado) | — | — | — |
| Puntos / Canje de puntos (s4: "Puntos acumulados", canje con regalo) | **descartar**: no hay CU ni modelo de puntos | — | — | — |
| `notifications/notifications_page.dart`, `widgets/notification_empty.dart` (s3: degradé, "¡Nada por aquí!" y lista agrupada por Hoy, Ayer, Hace 2 días) | **nueva** `views/notifications/notifications_view.dart`. Tutu guarda las notificaciones **en local** (`services/notification_cache.dart`, con Hive). SPLG hace lo mismo: el back no tiene bandeja (`GET /notifications/user/:id` sólo devuelve `{tokens:[]}`). En la tanda 2: pantalla + vacío + bandeja local; en la 3 se llena con las push | CU-021 | `GET /notifications/user/:userId` **200** (sólo tokens); `POST /notifications/token` **400 val.** | 2 (pantalla) / 3 (push) |
| `help/help_page.dart`, `widget/expansion_help.dart`, `sub_pages/have_problem_help_sub_page.dart`, `my_account_sub_page.dart` (s3 "Ayuda": buscador, categorías y acordeones) | **nueva** `views/help/help_view.dart` + `help_topic_view.dart`. Contenido estático en `assets/help.json`: Pedidos, Pagos, Entregas y envases, Mi cuenta, Tengo un problema (→ reclamo). Usa `SplgAccordion` | — | — | 2 |
| `about/about_us_page.dart` (acordeón "¿Quiénes somos?") | **nueva** `views/about/about_view.dart` (estático, `SplgAccordion`) | — | — | 2 |
| `terms/terms_page.dart`, `privacy_politycs/privacy_policy_page.dart` | `views/legal/legal_view.dart`: rehacer con `SplgHeader` y `SplgBulletList` | — | — | 2 |

## 2. Pantallas de SPLG sin equivalente en Tutu

### 2.1 Catálogo de garrafas (inicio de la tanda 2)
- Archivo: hoy `widgets/common/order/order.dart` (`Order`, `_CylinderItemTile`, `_CylinderDetailSheet`, `_OrderSummary`). Pasa a `views/home/widgets/catalog.dart`.
- Endpoint: `GET /gascylinder` **200**. Cada `gasCylinders[]` trae `type`, `weight`, `price`, `stock`, `description`, `photoUrl` y `promotions[{quantity, discountPercentage}]`. Además, `GET /gascylinder/:id/photo` **302** redirige a S3.
- CU: CU-041 (y CU-122–126, el carrito, que está planificado).
- Qué se reutiliza de Tutu:
  - La tarjeta con borde de `travels/widgets/trip_card.dart` para `SplgProductCard`: foto, nombre, peso, precio y la insignia "−12 % x4".
  - `DraggableSheet` (`tutu_app_packages/lib/widgets/dragable_sheet.dart`) para el resumen del carrito abajo, como el panel de f1. Va con "Entregar en" + "Continuar · $ total".
  - El `FareDetailsBanner` para el pedido en curso.
  - La hoja de detalle sigue el estilo de f17 (hoja blanca con asa y `SplgButton`).
- Pendiente de la ENTREGA: el descuento asume que la lista viene ordenada (`break`). Hay que ordenar `promotions` por `quantity` al mapear.

### 2.2 Mis direcciones
- Archivos: `views/addresses/addresses_view.dart` (`_AddressCard`) y `bottom_sheets/address_list/`.
- Endpoints: `GET /user-address/user/:userId` · `GET /user-address/:id` · `PATCH /user-address/:id` · `PATCH /user-address/:id/set-default` · `DELETE /user-address/:id` (todos con el rol verificado) · `POST /user-address` (exige `latitude`/`longitude`) · `GET /coverage-zones/check?lat&lng` **200** `{covered,surcharge,zone}`.
- CU: CU-046, CU-116 a CU-121, CU-058.
- Qué se reutiliza de Tutu:
  - `favorite/widgets/favorite_item.dart` para la fila: ícono de pin, calle y "Predeterminada", con el menú Editar / Predeterminar / Eliminar.
  - `fare/widgets/fare_origin.dart`: la píldora con punto y × (`SplgAddressPill`).
  - "Nueva dirección +" con el estilo de `booking/widgets/new_booking_button.dart`.
- **Editar** (CU-118, la ENTREGA dice que no existe): formulario de `floor`, `apartment`, `additionalInstructions` y `street`, sin mover las coordenadas → tanda 2.
- **Alta**: el back **no geocodifica**. Hay dos opciones:
  - (a) Formulario calle/número/ciudad + `geocoding` del dispositivo (`locationFromAddress`) + chequeo de cobertura. No necesita mapa y entra en la **tanda 2**.
  - (b) La `MapView` actual. Hay que rehacerla en la **tanda 3**.
  - Recomiendo (a) en la 2 y dejar la `MapView` actual tal cual, como alternativa "Elegir en el mapa", sin rediseño. **Decisión de nahue.**

### 2.3 Reclamo
- Archivos: `bottom_sheets/claim/claim_sheet.dart` y `services/claim_service.dart`.
- Endpoints: `POST /claims` **400 val.** (`orderId`, `customerId` = user_id, `reason`, `description`) · `POST /claims/:id/photo` **404 id** (rol OK) · `GET /claims/:id/photo` **404 id** (rol OK). `GET /claims` y `GET /claims/:id` dan **403**: el cliente no puede ver sus reclamos (§4).
- CU: CU-023, CU-174, CU-175.
- Qué se reutiliza de Tutu:
  - `incident_travel/cancel_travel_page.dart` (motivos con radio y "Otro") para elegir el `reason`.
  - `ratings/widgets/rate_comments.dart` (área de texto con contador) para `description`.
  - `pay_success_dialog.dart` para el "Reclamo enviado".
- Adjuntar una foto va en la **tanda 3**: usa cámara o fotos, y el permiso de fotos todavía no lo usa ninguna pantalla.
- "Mis reclamos" (lista y estado) depende del endpoint de §4; con él, se reutiliza `trip_card`.

### 2.4 QR de la entrega
- **Ojo con el brief:** según CU-079, el **chofer** muestra el QR y el **cliente lo escanea**. `GET /orders/:id/delivery-code` da **403** al cliente (es del chofer o el admin); el cliente envía `POST /orders/:id/confirm-delivery {code}` (**400 val.**, con el rol OK).
- La pantalla que existe, `views/qr_scan/qr_scan_view.dart`, es de **escaneo**, no de mostrar el QR.
- Si nahue quiere que el cliente **muestre** un QR, cambia el CU y el back: haría falta un código del cliente y que el chofer escanee. **A decidir.**
- Qué se reutiliza de Tutu:
  - El modal con degradé de `trip/dialogs/searching_driver.dart` para el marco del escáner y el resultado.
  - `camera_access_popup.dart` para el permiso, que ya está resuelto con `PermissionsService`.
- Tanda **3**.

### 2.5 Pedido programado por franja
- Archivos: `views/checkout/widgets/time_range_selector.dart` (`TimeRangeSelector`) y `services/time_slot_service.dart`. Ya envía `scheduledDate` + `timeSlotId` (`history_service.dart`).
- Endpoints: `GET /time-slot/availability?date&distributor` **200** · `POST /orders` (`scheduledDate`, `timeSlotId`). La lista sale de `GET /orders/customer/:userId`, filtrada en la app.
- CU: CU-044, CU-045. CU-072 (seña) va en la tanda 3.
- Qué se reutiliza de Tutu:
  - El formulario de `booking/widgets/booking_form.dart`: fecha con calendario y hora con desplegable → `SplgDateField` + franjas como `SplgRadioRow` con "quedan N".
  - `booking_tile/*` para la lista: `booking_date`, `booking_status` y `booking_route`.
  - `booking_summary.dart` para el detalle oscuro con "Cancelar".

## 3. Qué existe hoy en la app cliente y qué es nuevo

**Se rehace (la lógica y los servicios se mantienen; cambia la vista)**

| Archivo actual | Destino |
|---|---|
| `views/startup/startup_view.dart` | splash con degradé |
| `views/login/login_view.dart` (+ `.form.dart`) | login de Tutu; la recuperación sale a una vista propia |
| `views/signup/signup_view.dart` (+ `.form.dart`) | asistente de 3 pasos + "Registro completado" |
| `views/home/home_view.dart` | sin `BottomNavigationBar`: botón de menú + `Drawer` + catálogo + panel inferior |
| `widgets/common/order/order.dart` (`Order`, `_CylinderItemTile`, `_CylinderDetailSheet`, `_OrderSummary`, `_ActiveOrderCard`) | catálogo y banner del pedido en curso |
| `widgets/common/history/history.dart` (`History`, `_OrderItemTile`) | `views/orders/orders_view.dart` |
| `widgets/common/account/account.dart` (`Account`) | se reemplaza por el `Drawer` (§1) |
| `widgets/common/input/text_input.dart` (`TextInput`) | `SplgTextField` de la lib |
| `views/checkout/checkout_view.dart` + `widgets/*` | Confirmación (f6) |
| `views/order_tracking/order_tracking_view.dart` (`_TrackingStepper`, `_DriverCard`, `_HeaderIconButton`, `ArrivingBanner`) | hoja inferior de f8 sin mapa |
| `views/profile/profile_view.dart` (`_ProfileField`, `_LegalLink`) | Mi perfil (s3) + subpantallas |
| `views/addresses/addresses_view.dart` (`_AddressCard`) | Mis direcciones |
| `views/legal/legal_view.dart` | con encabezado y viñetas |
| `bottom_sheets/address_list/` | selector de dirección |
| `bottom_sheets/claim/` | reclamo |
| `bottom_sheets/rate_driver/` | calificar (f17) |
| `bottom_sheets/notice/` | aviso |
| `dialogs/info_alert/` | diálogo de marca (`SplgDialog`) |
| `views/map/map_view.dart`, `views/qr_scan/qr_scan_view.dart`, `views/payment_webview/payment_webview_view.dart` | **tanda 3** (en la 2 no se tocan) |

Dos notas:
- `widgets/common/market/market.dart` (`Market`) parece **código muerto**: sólo aparece su definición. Confirmarlo y borrarlo en el lote 1.
- `ui/common/app_strings.dart` y `ui_helpers.dart` se mantienen. Los textos nuevos van ahí.

**Nuevo en la tanda 2** (las rutas Stacked van en `app/app.dart`)
- `views/welcome/` · `views/recover_password/` (+ `mail_sent_view`) · `views/signup/signup_done_view.dart` · `views/logout/` · `views/no_network/`
- `widgets/common/app_drawer/`
- `views/orders/` · `views/order_detail/` · `views/order_delivered/` · `views/cancel_order/`
- `views/scheduled/` (lista y formulario)
- `views/profile/personal_info_view.dart` · `edit_profile_view.dart` · `change_password_view.dart`
- `views/notifications/` (+ `services/notification_inbox_service.dart`, local, con `shared_preferences`)
- `views/help/` (+ `assets/help.json`) · `views/about/`
- Editar dirección (en `addresses/`) y el alta por formulario con `geocoding`, si nahue elige la opción (a)

**Ya está y no se toca:** `PermissionsService`/`AppPermissions`, `NotificationService` (push), `OrderTrackingService` (socket), la capa `data/`, `domain/` y los servicios.

## 4. Endpoints que faltan en el back para la tanda 2

| # | Para qué | Propuesta | Hoy | Prioridad |
|---|---|---|---|---|
| 1 | **Eliminar mi cuenta** (s3, Mi perfil; también lo exigen las tiendas) | `DELETE /users/me` (rol CUSTOMER): baja lógica del usuario y del cliente + deshabilitar en Firebase, reutilizando lo de CU-085 | `DELETE /users/:id` y `/users/me` → **403** (sólo admin). La app hoy **simula** el borrado con `signOut()` | **Obligatorio** |
| 2 | **Mis reclamos** y el estado del reclamo en el detalle del pedido | `GET /claims/mine` (o permitir `GET /claims` a CUSTOMER filtrando por `customerId = user`) | `GET /claims`, `GET /claims/:id` → **403** | Alta, si entra "Mis reclamos" |
| 3 | Saber si un pedido **ya está calificado** (botón "Calificar" y `show_rate_pending`) | Agregar `ratedByCustomer: boolean` a `OrderResponseDto` en `GET /orders/:id` y en `GET /orders/customer/:userId` | No existe; sólo se entera por el **409** del `POST /ratings` | Media (sin esto, se intenta y se maneja el 409) |
| 4 | Contacto y horario de la distribuidora para Ayuda ("Llamar a la distribuidora") | `GET /distributor/public` (público o CUSTOMER): nombre, teléfono, horario, logo | `GET /distributor/current` → **403** | Media (alternativa: texto fijo en `help.json`) |
| 5 | Filtro por estado en el historial (en curso, programados) | `GET /orders/customer/:userId?status=pending,accepted,on_the_way&scheduled=true` | Sólo paginación; se filtra en la app | Baja |

**No hacen falta:**
- Cambiar la contraseña: se hace con Firebase.
- Bandeja de notificaciones: local, como Tutu.
- Recuperar la contraseña: Firebase.
- Catálogo, direcciones, franjas, crear, cancelar o calificar un pedido, y crear un reclamo: ya están.

Si se agrega alguno, por regla del workspace se actualiza la doc de `splg-docs` y `npm run api:types` en el panel.

## 5. Componentes de splg-lib que el cliente necesita y no existen

**Ya están:** `SplgHeader`, `SplgMenuItem`, `SplgEmptyState`, `SplgAccordion`, `SplgPasswordField`, `SplgTextField`, `SplgButton` (degradé, contorno, blanco, peligro), `SplgDarkCard`, `SplgSoftCard`, `SplgSectionBar`, `SplgListRow`, `SplgInfoSection`/`SplgInfoRow`, `SplgAvatar`, `SplgStarRating` (sólo muestra), `SplgChoiceChips`, `SplgGradientBackground`, `SplgBarChartCard`, `SplgLogo`, `SplgIllustration`, `SplgIcons`, `SplgGradients`, `SplgScale`/`SplgType`.

**Faltan** (el origen en Tutu va entre paréntesis):

| Componente | Origen en Tutu | Uso en el cliente |
|---|---|---|
| `SplgIconButton` (cuadrado redondeado con degradé) | `widgets/buttons/icon_home_button.dart`, `icon_gradient_button.dart`, `pages/home/widgets/home_button.dart` | botón de menú del inicio (f1), llamar o chatear en la tarjeta del repartidor |
| `SplgBottomPanel` (hoja con asa, arrastrable) | `widgets/dragable_sheet.dart` | panel del inicio, resumen del carrito, hoja del seguimiento (f8), calificar (f17) |
| `SplgAddressPill` (punto de color + texto + ×) | `fare/widgets/fare_origin.dart`, `widgets/trips_to_from_input.dart` | dirección de entrega en el inicio, la confirmación y el detalle |
| `SplgOptionRow` (ícono + título + valor a la derecha + flecha o desplegable) | filas "Tipo de vehículo / Forma de pago" de f6 (`fare/widgets/payment_selector.dart`) | forma de pago, cuándo, dirección en la confirmación |
| `SplgRadioRow` | `fare/widgets/filter_radio_tile.dart` (`FilterCheckboxTile`) | franjas, medios de pago, motivos de cancelación y de reclamo |
| `SplgCheckboxLink` | `widgets/check_box_link.dart` (`CheckboxWithLink`) | aceptar términos y privacidad en el registro |
| `SplgStepDots` + `SplgStepNav` | `register/widgets/navigation_buttons.dart` (`NavigationButtonsStep`) | asistente de registro |
| `SplgIllustrationHeader` (cabecera con ilustración y curva) | `register/widgets/header_image.dart` | registro, recuperar contraseña |
| `SplgPhoneField` (+54, E.164) | `widgets/textfield/phone_input_field.dart` | registro, editar perfil (el back exige E.164) |
| `SplgDateField` | `widgets/textfield/date_input_field.dart`, `cupertino_date_input_field.dart` | pedido programado |
| `SplgSelectField` | `widgets/textfield/drop_down_field.dart` | franja, ciudad |
| `SplgSearchField` | buscador de Ayuda (s3) | Ayuda |
| `SplgTextArea` con contador | `ratings/widgets/rate_comments.dart` | calificar (300), reclamo, notas del pedido |
| `SplgRatingInput` (estrellas tocables) | `widgets/rating_widget.dart`, `ratings/widgets/start_rating.dart` | calificar (f17) |
| `SplgProfileHeader` (avatar + nombre + teléfono + enlace + "N pedidos · ★") | `widgets/user_info_widgets/user_info_profile_pic.dart`, `userrate_widget.dart` | Mi perfil, cabecera del menú |
| `SplgOrderCard` (tarjeta con borde: ícono, fecha, insignia, total, forma de pago, flecha) | `travels/widgets/trip_card.dart`, `booking/widgets/bookin_tile/booking_tile.dart` | Mis pedidos, programados, reclamos |
| `SplgStatusBadge` (píldora de estado, con colores `brasa.*Soft`) | insignia de `trip_card` y `booking_status.dart` | estados del pedido y del reclamo |
| `SplgProductCard` + `SplgQuantityStepper` | (no está en Tutu; se arma con el estilo de `trip_card`) | catálogo |
| `SplgDriverCard` (vehículo y patente + repartidor + botones) | `widgets/driver_profile.dart`, `booking_driver_profile.dart` | seguimiento, detalle |
| `SplgDialog` / `SplgModalCard` (modal con degradé, ilustración, título, texto y botón blanco) | `widgets/dialogs.dart` (`DialogService`), `trip/dialogs/searching_driver.dart`, `pay_success_dialog.dart` | buscando repartidor, cerrar sesión, reclamo enviado, confirmar cancelación |
| `SplgLoader` / `SplgSkeletonRow` | `widgets/loading_widget.dart`, `widgets/loaders/row_text_loader.dart` | cargas de listas |
| `SplgBulletList` | `widgets/bullet_list_widget.dart`, `unorderedList.widget.dart` | Términos, Privacidad, Ayuda |
| `SplgNotificationTile` + agrupado por día | `notifications/notifications_page.dart` (`_NotificationView`) | Notificaciones |

**Íconos que hay que sumar a `SplgIcons`** (Phosphor):
- `cylinder`: no hay garrafa en Phosphor; usar `flame` o un SVG propio.
- `calendar`, `clock`, `truck`, `cart`, `plus`, `minus`, `close`, `trash`, `pencil`, `house`, `chatWarning` (reclamo), `bellSlash`, `bank` (transferencia), `qr` (tanda 3), `phoneCall`, `notes`.

**Ilustraciones que hay que sumar a `SplgIllustration`** (3dicons, CC0):
- `emptyOrders`: camión o caja. Hoy `emptyList` dice "deliveries".
- `location`: pin, para "sin direcciones".
- `calendar`: programados.
- `cylinderDelivered` o `success`: entregado.
- `support`: auriculares, para Ayuda.
- `noNetwork`.
- `claim`: escudo o chat.

## 6. Orden de implementación sugerido (tanda 2, en lotes chicos)

Cada lote va en su worktree, con su gate (`flutter analyze --no-fatal-infos && flutter test`), capturas en el simulador contra `:3010` y revisión cruzada. Los lotes de la lib van **antes** de los del cliente que los usan.

1. **L1 · lib: piezas base**
   - Qué: `SplgIconButton`, `SplgBottomPanel`, `SplgAddressPill`, `SplgOptionRow`, `SplgRadioRow`, `SplgStatusBadge`, `SplgOrderCard`, `SplgDialog`, `SplgLoader`, más los íconos y las ilustraciones nuevas.
   - Tests: widget, claro y oscuro, y contraste AA.
2. **L2 · cliente: esqueleto de navegación**
   - Qué: `HomeView` sin `BottomNavigationBar`, con `SplgIconButton` + `AppDrawer` (rutas vacías donde falte la pantalla), `StartupView` con degradé y `NoNetworkView`. Borrar `Market` si se confirma muerto y reemplazar `TextInput` por `SplgTextField`.
   - Actualizar el `integration_test/flujo_basico_test.dart` a la navegación nueva.
3. **L3 · lib + cliente: autenticación**
   - Lib: `SplgCheckboxLink`, `SplgStepDots`/`SplgStepNav`, `SplgIllustrationHeader`, `SplgPhoneField`.
   - Cliente: `WelcomeView`, `LoginView`, `RecoverPasswordView` + `MailSentView`, `SignupView` en 2 pasos (el paso 3 de dirección queda para L7), `SignupDoneView`, `LogoutView`.
   - Endpoints: `POST /auth/login`, `POST /users/check-exists`, `POST /auth/registro`.
4. **L4 · cliente: catálogo e inicio**
   - Lib: `SplgProductCard` + `SplgQuantityStepper`.
   - Cliente: catálogo con promociones ordenadas, panel inferior "Entregar en" + carrito, y el banner del pedido en curso.
   - Endpoints: `GET /gascylinder`, `GET /user-address/user/:id/default`, `GET /orders/customer/:userId`.
5. **L5 · cliente: confirmación (f6)**
   - Qué: `CheckoutView` con `SplgAddressPill`, `SplgOptionRow` (dirección, cuándo, pago efectivo/transferencia), franjas con `SplgRadioRow` y notas.
   - Endpoints: `POST /orders` con `Idempotency-Key` v4 y `GET /time-slot/availability`.
6. **L6 · cliente: Mis pedidos, detalle y cancelar**
   - Qué: `OrdersView`, `OrderDetailView`, `CancelOrderView` con motivos, y la hoja de seguimiento sin mapa (`SplgDriverCard`, estado "Buscando repartidor…").
   - Endpoints: `GET /orders/customer/:userId`, `GET /orders/:id`, `PATCH /orders/:id/cancel`.
7. **L7 · cliente: Mis direcciones**
   - Qué: lista, predeterminar, eliminar, **editar** (nuevo), y el alta por formulario + `geocoding` + `GET /coverage-zones/check` si nahue elige la opción (a). Paso 3 opcional del registro.
8. **L8 · lib + cliente: calificar y reclamo**
   - Lib: `SplgRatingInput`, `SplgTextArea`.
   - Cliente: hoja de f17, `OrderDeliveredView` y la hoja de reclamo (sin foto).
   - Endpoints: `POST /ratings` (manejar el 409) y `POST /claims`.
9. **L9 · back (en paralelo desde L2): endpoints de §4**
   - `DELETE /users/me` (obligatorio).
   - `GET /claims/mine` y `ratedByCustomer` (si entran).
   - Con tests, `api:types` del panel y la doc.
10. **L10 · lib + cliente: perfil**
    - Lib: `SplgProfileHeader`.
    - Cliente: `ProfileView`, `PersonalInfoView`, `EditProfileView` (`PATCH /users/:id`), `ChangePasswordView` (Firebase), eliminar cuenta (con L9) y el resumen de calificación (`GET /ratings/user/:userId/summary`).
11. **L11 · cliente: programados**
    - Lib: `SplgDateField`, `SplgSelectField`.
    - Cliente: `ScheduledOrdersView` (lista filtrada) y el formulario "Programar pedido".
12. **L12 · cliente: contenido estático y notificaciones**
    - Lib: `SplgSearchField`, `SplgBulletList`, `SplgNotificationTile`.
    - Cliente: `HelpView` + `HelpTopicView` (`help.json`), `AboutView`, `LegalView` rehecha y `NotificationsView` con bandeja local vacía.
    - Si entra L9: "Mis reclamos".
13. **L13 · cierre**
    - `integration_test` completo con la navegación nueva y los goldens regenerados.
    - Barrido de colores (`test/brand/brand_colors_test.dart`) y de fuente.
    - Recorrido en el simulador contra `:3010`: alta → pedido → cancelación → calificación → baja de la cuenta.

**Tanda 3 (para el registro):**
- Mapa en el inicio (f1) y en el seguimiento en vivo (f8, `follow_button`).
- `MapView` para el alta de direcciones.
- QR: decidir antes quién lo muestra.
- MercadoPago (webview + "Pago aprobado") y reserva con seña (CU-072).
- Foto del reclamo y del perfil.
- Push: llenar la bandeja y los recordatorios de programados.
- Envases (SS-13).

**Decisiones abiertas para nahue:**
1. Alta de dirección sin mapa (formulario + geocodificación del dispositivo) en la tanda 2: ¿sí o no?
2. QR: ¿el cliente escanea (como dice CU-079) o muestra?
3. ¿Se saca la barra inferior y se usa el menú lateral como Tutu? Es lo que asume este plan.
4. ¿Entra "Mis reclamos" en la tanda 2? Requiere el endpoint 2 de §4.
