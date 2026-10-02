# Tracking en vivo: ¿desarrollarlo o usar un servicio externo? — 26/09/2026

Análisis, no implementación. Parte de dos preguntas: si conviene sacar el
seguimiento del chofer a un servicio externo (Rappi, Mercado Libre, DiDi, etc.)
y qué tomar del "prompt maestro" que llegó de otra IA. Lo del código se
verificó leyendo los repos el 26/09; lo de terceros sale de las fuentes
citadas al final de cada sección. Donde algo no se pudo verificar, se dice.

---

## 1. Resumen ejecutivo

- **Rappi, Mercado Libre, DiDi, PedidosYa y Uber no venden "tracking para tu
  flota"**. Venden su red de repartidores (Uber Direct, PedidosYa Courier API,
  Rappi Cargo, DiDi Entrega) o sirven sólo para ventas hechas en su marketplace
  (Mercado Envíos Flex). Ninguno sirve para seguir camionetas propias de una
  distribuidora con pedidos propios, y Uber prohíbe de forma explícita
  inflamables y materiales peligrosos: una garrafa lo es.
- Los SaaS para flota propia (Onfleet, Shipday, Tookan, Google Fleet Engine,
  HyperTrack) reemplazan **la app del chofer, el despacho y el panel**, no una
  pieza suelta. Ya está hecho todo eso, así que pagaría por tirar trabajo y
  perdería el despacho secuencial, que es el módulo que se defiende.
- El tracking actual (socket + Redis GEO) **ya funciona y no toca Postgres**: la
  "sobrecarga extrema de IOPS" del prompt maestro no existe.
- **Recomendación: camino A.** Quedarse con socket + Redis, cerrar H-86 y H-87 y
  tomar del prompt maestro sólo lo que suma: la coordenada de confirmación de
  entrega como dato de auditoría (en un campo nuevo, no en `deliveryPoint`),
  interpolar el marcador en el cliente y acumular los km por viaje para M1.
  Firebase RTDB queda documentada como alternativa evaluada y descartada, que
  en la defensa suma más que haberla adoptado.

---

## 2. Qué hay hoy (verificado en el código)

| Pieza | Dónde | Estado |
|---|---|---|
| Emisión de posición | `splg-app-chofer/lib/services/location_service.dart:109-112` | `geolocator` con `distanceFilter: 10`: emite cada 10 m, no cada N segundos. Servicio en primer plano (`flutter_foreground_task`) |
| Envío | `splg-app-chofer/lib/services/driver_socket_service.dart:130-143` | `driver:update-location` con `lat`/`lng`. **Si el socket está caído, la posición se descarta** (no hay cola). No manda rumbo (`heading`) |
| Recepción | `splg-app-backend/src/gateways/drivers.gateway.ts:117-160` | La identidad sale del token del handshake, no del cuerpo. Escribe en Redis GEO y, si hay pedido en curso, reenvía `order:driver-location` al cliente y al panel |
| Radar | `RedisService.updateDriverLocation` / `removeDriver` al desconectar | Redis GEO `drivers:locations`. Postgres no se toca |
| Despacho | `src/order/application/dispatch-orchestrator.service.ts` | Secuencial, radios 5→10→15→20 km, ofertas con vencimiento, cron de reintento |
| Cliente | `splg-app-cliente/lib/ui/views/order_tracking/order_tracking_viewmodel.dart:423-431` | Mueve el marcador **de golpe** a cada posición (sin interpolar). Usa `rotation: _driverHeading`, pero el back nunca manda rumbo: queda en 0 |
| Panel | `splg-app-admin/src/pages/Tracking/Tracking.tsx` | Escucha el mismo evento |
| Navegación | `splg-app-chofer/lib/services/navigation_launcher.dart` | **Ya existe** el deep link a Waze (`waze.com/ul?ll=…&navigate=yes`) y a Google Maps |
| Destino | `order.deliveryPoint` (`order.entity.ts:211`, copiado en `create-order.use-case.ts:251`) | Punto PostGIS = destino |
| Resto | `delivery.actual_location` | Sigue vivo: se escribe en `registro.service.ts:136` y `delivery.service.ts:292-299` |

Dos detalles que salen de esta lectura y no estaban anotados:

1. **CU-017 está desactualizado** en un punto: sus "Comentarios" dicen que el
   identificador del chofer viaja en el mensaje y no se contrasta con la
   conexión. El gateway ya lo toma del token (`drivers.gateway.ts:111-115`). La
   app sigue mandando `userId` en el cuerpo, pero el back lo ignora.
2. **La rotación del marcador no funciona**: el cliente lee `heading`/`bearing`
   (`order_tracking_service.dart:177`), pero ni la app del chofer lo manda ni el
   back lo reenvía. Siempre vale 0.

---

## 3. Rappi, Mercado Libre, DiDi, PedidosYa, Uber: ¿qué venden de verdad?

Todos tienen API, pero ninguna es una API de *tracking de tu flota*. Hay dos
modelos y ninguno le sirve a SPLG:

- **Delivery como servicio**: les pasás origen y destino, ellos mandan un
  repartidor suyo y te devuelven estado y link de seguimiento. Cobran por envío.
- **Logística del marketplace**: sólo para lo que se vende en su plataforma.

| Servicio | Modelo | ¿Sirve con la flota de la distribuidora? | Posadas | Garrafas (GLP) |
|---|---|---|---|---|
| **Uber Direct** | Delivery como servicio, marca blanca. La API crea envíos que hacen repartidores de Uber | No. El repartidor es de Uber | La página de courier nombra Buenos Aires. **Posadas: no verificado** | **Prohibido**: la política de Uber Direct excluye "hazardous materials" y "flammable and combustible substances and products" |
| **PedidosYa Envíos (Courier API)** | Delivery como servicio: "automatizar el uso de la red logística de PedidosYa". Estimación, alta de envío, estados | No | Sin dato público verificado para Envíos en Posadas | **Sin política pública encontrada**. Es moto/auto de terceros: muy improbable que acepte cilindros de 10-45 kg de GLP |
| **Rappi (Cargo / RappiEntrega)** | B2B sobre la red de repartidores independientes de Rappi. Tiene API, link de seguimiento y agrupación de pedidos. Hay dominio `cargo.rappi.com.ar` | No | Rappi opera en Posadas desde enero de 2023 (zona centro); **Cargo en Posadas: no verificado** | Sin política pública de Cargo encontrada. Mismo problema que PedidosYa |
| **DiDi Entrega / Business** | Delivery como servicio. XL: hasta 10 kg y 40×30×45 cm | No | En Argentina hay señales informales de que funciona; **sin API pública para empresas encontrada** | Una garrafa de 10 kg ya excede el límite de peso de XL (que es "menos de 10 kg") |
| **Mercado Envíos Flex** | El vendedor entrega con su flota o un tercero, **pero sólo ventas de Mercado Libre**. Requisitos: envíos activos en las publicaciones, reputación amarilla o verde, entregas en el día o al siguiente | No: exige vender por ML. Los pedidos de SPLG no son órdenes de ML | Argentina sí; zonas según el domicilio del vendedor | Venta de gas en garrafas por ML: no verificado; ML tiene sus propias restricciones de productos |

### Lo que implica tercerizar la entrega (aunque se pudiera)

- **Comisión por envío** en cada pedido. Uber: "precio por entrega" según tipo,
  velocidad y región, sin tarifa pública para Argentina.
- **Se pierde el despacho propio**: la asignación la hace la plataforma. El
  despacho secuencial con radios y ofertas que vencen, que es uno de los
  módulos que se defienden, desaparece.
- **La flota deja de ser de la distribuidora**. En SPLG la flota es de la
  distribuidora: los vehículos y su documentación los carga el admin en el
  panel, y M1 y M4 dependen de eso. Con un repartidor de
  Rappi no hay vehículo que planificar ni envase vacío que recuperar en la
  misma visita.
- **Normativa**: el transporte comercial de garrafas en vehículos se rige por la
  norma GL-42 de la Secretaría de Energía y el Reglamento General para el
  Transporte de Mercancías Peligrosas por Carretera (Decreto 779/95, Anexo S).
  Un repartidor de app en moto no cumple eso. **No es un tema de API: es legal.**

**Conclusión:** ninguna de estas empresas resuelve "no quiero desarrollar el
tracking". Lo que ofrecen es "no quiero tener choferes", que es otro negocio y
contradice el dominio de la tesis.

Fuentes:
- Uber Direct API: https://developer.uber.com/docs/deliveries/overview
- Uber, ítems prohibidos en Direct: https://help.uber.com/en/merchants-and-restaurants/article/items-prohibited-and-restricted-through-uber-direct?nodeId=63024079-3274-4259-8c7c-96724b882da5
- Uber courier Buenos Aires: https://www.uber.com/ar/en/b/courier-services/capital-federal-ciudad-autonomade-buenos-aires-ar/
- PedidosYa Courier API: https://developers.pedidosya.com/courier-api/v1
- PedidosYa Envíos: https://envios.pedidosya.com/
- Rappi Developer Portal: https://dev-portal.rappi.com/es/
- RappiCargo (lanzamiento B2B): https://about.rappi.com/es/rappi-lanza-su-nuevo-servicio-b2b-rappicargo
- Cargo Argentina: https://cargo.rappi.com.ar/auth/login
- Rappi en Posadas: https://misionesonline.net/2023/01/13/rappi-llego-a-posadas/
- DiDi Entrega (modalidades): https://web.didiglobal.com/cl/entrega/
- DiDi Entrega Business: https://www.didi-food.com/es-MX/entrega-business/home
- Mercado Envíos Flex (developers): https://developers.mercadolibre.com.ar/en_us/mercado-envios-flex
- Requisitos Flex: https://vendedores.mercadolibre.com.mx/nota/envios-flex-requisitos
- GLP Grupo 3 (transporte de garrafas): https://www.argentina.gob.ar/economia/energia/hidrocarburos/gas-licuado-de-petroleo/normativa/normas-tecnicas-de-glp-por-tipo-de-operador/grupo-3

---

## 4. Servicios para flota propia

Esta es la categoría que sí apunta a lo que nahue pensaba. Se separan en dos:
**plataformas completas** (traen app de chofer, despacho y panel) e
**infraestructura** (sólo el caño de tiempo real o de ubicación).

### 4.1 Plataformas completas

| Servicio | Qué resuelve | Precio (verificado en su web el 26/09) | Flutter | Lock-in | Cuánto de SPLG reemplaza |
|---|---|---|---|---|---|
| **Google Fleet Engine — Last Mile Fleet Solution** | Tareas de entrega, posición del vehículo, ETA, seguimiento compartido con el cliente, eventos | **Sin precio público**. Se factura por tarea terminada con éxito y **exige contrato con Google o un partner** antes de producción. Terceros citan USD 0,10-0,15 por viaje, no confirmado | **Driver SDK sólo nativo** (Java/Swift). Existe el plugin `google_navigation_flutter` (beta) para navegación, pero el Driver SDK habría que puentearlo con canales de plataforma | Alto: modelo de tareas y vehículos de Google | Tracking, ETA (el paso 6-7 pendiente de CU-017) y seguimiento. No el despacho secuencial |
| **Onfleet** | Todo: app de chofer, prueba de entrega, rutas, notificaciones, panel | Launch USD 619/mes (2.500 tareas), Scale USD 1.349/mes (5.000), Enterprise desde USD 3.099. En su página, la API figura en Scale y Enterprise | Sin SDK Flutter: la app del chofer es la de ellos | Muy alto | Casi todo lo del chofer y el despacho |
| **Shipday** | Todo, orientado a comercios chicos | Gratis hasta 300 pedidos/mes y 10 choferes; Professional USD 39/mes sin límite de pedidos; con marca propia USD 79-99; Business AI USD 349 | Sin SDK: app de chofer propia de Shipday | Muy alto | Casi todo |
| **Tookan (Jungleworks)** | Todo | Según una reseña de terceros (no se pudo abrir la página oficial): gratis 100 tareas / 2 agentes; USD 99/mes 1.000 tareas; USD 249/mes 3.000 | App propia | Muy alto | Casi todo |
| **HyperTrack** | Hoy se orienta a fuerza de trabajo de campo (turnos, visitas), no a delivery | USD 10 por usuario/mes, **mínimo USD 300/mes facturado anual** | SDK Flutter existe | Alto | Sólo la captura de ubicación |

Lectura: **ninguna se enchufa como pieza**. O te dan su app de chofer (y la de
SPLG sobra), o, como Fleet Engine, piden contrato comercial y SDK nativo. Para
una tesis con apps propias ya construidas, reemplazan justo lo que ya está
hecho. Y Onfleet sola cuesta más por mes que todo el resto de la
infraestructura de SPLG junta.

### 4.2 Infraestructura de tiempo real / ubicación

| Servicio | Qué resuelve | Precio | Flutter | Lock-in | Qué reemplazaría |
|---|---|---|---|---|---|
| **Firebase Realtime Database** | Sincroniza un árbol JSON; cola de escrituras offline, `onDisconnect`, reconexión y refresco de token automáticos | Spark: 100 conexiones simultáneas, 1 GB guardado, 10 GB/mes bajados. Blaze: 1 GB y ~360 MB/día gratis, después USD 5/GB guardado y USD 1/GB bajado | Sí (`firebase_database`, FlutterFire) | Medio. SPLG ya usa Firebase para identidad y push | El reenvío chofer→cliente/panel (unas 20 líneas de `drivers.gateway.ts`) |
| **Firestore** | Igual, documental, se cobra por operación | Por lectura/escritura (no se buscó tarifa: para posición cada pocos segundos RTDB es la opción que Firebase recomienda) | Sí | Medio | Lo mismo |
| **Ably** | Pub/sub gestionado | Gratis: 200 conexiones y 6 M mensajes/mes. Pagos desde USD 29/mes + USD 2,50 por millón de mensajes | SDK Flutter: no confirmado en la página de precios | Medio | Lo que hoy hace Socket.IO + adaptador Redis |
| **Pusher Channels** | Pub/sub gestionado | Gratis: 200 k mensajes/día y 100 conexiones. Startup USD 49/mes | Hay clientes comunitarios | Medio | Lo mismo |
| **Radar** | Geofencing, viajes, ETA | **Sin plan gratis**, cotización por uso; desde USD 0,04 por usuario rastreado/mes en algunos productos | No confirmado | Medio | Aviso de llegada por geocerca (hoy es un botón: `notifyDriverArrived`) |

Lectura: esto sí se puede enchufar, pero **reemplaza la parte más barata del
sistema**. El socket, el adaptador Redis y el reenvío ya están hechos y
probados; lo que falta (reconexión, token, interpolación) es poco.

Fuentes:
- Fleet Engine, facturación de Mobility: https://developers.google.com/maps/architecture/mvi-mobility-billing
- Fleet Engine: https://developers.google.com/maps/documentation/mobility/fleet-engine/essentials
- Last Mile Fleet Solution (anuncio): https://mapsplatform.google.com/resources/blog/introducing-last-mile-fleet-solution-maximize-what-your-fleet-can-do-start-finish/
- Navigation SDK para Flutter: https://github.com/googlemaps/flutter-navigation-sdk
- Driver SDK en Flutter (limitación): https://forum.itsallwidgets.com/t/how-to-integrate-google-fleet-engine-driver-sdk-with-flutter/1175
- Precio por viaje citado por terceros: https://blog.afi.io/blog/google-mobility-an-introduction-to-google-odrd-lmfs-and-cloud-fleet-routing-apis/
- Onfleet: https://onfleet.com/pricing
- Shipday: https://www.shipday.com/pricing
- Tookan (reseña de terceros): https://www.upperinc.com/blog/tookan-pricing/
- HyperTrack: https://www.hypertrack.com/pricing — SDK Flutter: https://developer.hypertrack.com/docs/install-sdk-flutter
- Firebase: https://firebase.google.com/pricing
- Ably: https://ably.com/pricing
- Pusher: https://pusher.com/channels/pricing/
- Radar: https://radar.com/pricing

---

## 5. La propuesta de Firebase RTDB frente a lo que hay

La propuesta: el chofer escribe su GPS cada 3-5 s en `/viajes/{order_id}` sin
pasar por NestJS; el cliente escucha ese nodo; el back crea el nodo al pasar a
`on_the_way` y lo borra al entregar; Redis GEO sigue para la flota.

### 5.1 Ventajas reales

- **Reconexión y estado**: un listener de RTDB recibe el último valor al volver
  a conectarse. Eso resuelve H-86 **para la posición**, pero no para el estado
  del pedido: los `order:*` (aceptado, en camino, cancelado, llegó) siguen
  viajando por socket, salvo que también se espejen en RTDB.
- **Token**: FlutterFire refresca el token de Firebase solo. Resuelve H-87
  **para el stream de posición**, pero no para el socket del chofer, que sigue
  siendo imprescindible para recibir ofertas (`server:new-order-request`).
- **Cola offline**: RTDB encola las escrituras sin conexión y las manda al
  volver. Para tracking en vivo es **un arma de doble filo**: al reconectar
  llegan de golpe posiciones viejas y el marcador "rebobina". Para contar km
  sirve, pero se resuelve mejor acumulando en la app (ver §6).
- **Menos carga en el back**: cierto en abstracto, irrelevante a esta escala
  (ver §6, punto de IOPS).

### 5.2 Costos

Cuenta gruesa, a confirmar midiendo: 10 choferes en ruta 8 h/día, una escritura
cada 5 s de unos 150-200 bytes con overhead, dos oyentes por viaje (cliente y
panel) → del orden de **20-50 MB/día bajados**. Entra holgado en los ~360
MB/día gratis de Blaze. **Costo ≈ USD 0/mes** para una distribuidora de
Posadas. El plan Spark (100 conexiones simultáneas) queda corto si se suman
varias distribuidoras; en Blaze el límite es 200 k por base.

### 5.3 Seguridad

Hoy la identidad del socket se resuelve **por email contra Postgres**
(`socket-identity.service.ts:42-70`); SPLG **no usa custom claims** (no hay un
`setCustomUserClaims` en todo el back). Además, el id interno del chofer no es
el uid de Firebase (lo aclara `driver_auth_service.dart:14`). Para que RTDB
aplique "un cliente sólo lee su viaje" hay dos caminos:

1. **ACL escrita por el back en el nodo** — al pasar a `on_the_way`, el back
   crea `/viajes/{distribuidoraId}/{orderId}/acl` con los uid de Firebase del
   cliente y del chofer, y las reglas lo leen con `root.child(...)`:

   ```json
   "viajes": { "$dist": { "$orderId": {
     "pos": {
       ".read":  "auth != null && (data.parent().child('acl/cliente').val() === auth.uid || data.parent().child('acl/chofer').val() === auth.uid || auth.token.adminDe === $dist)",
       ".write": "auth != null && data.parent().child('acl/chofer').val() === auth.uid",
       ".validate": "newData.hasChildren(['lat','lng','t']) && newData.child('lat').isNumber() && newData.child('lat').val() >= -90 && newData.child('lat').val() <= 90"
     },
     "acl": { ".read": false, ".write": false }
   }}}
   ```
2. **Custom claims** (`rol`, `distribuidoraId`) sincronizados desde Postgres en
   cada alta, cambio de rol o bloqueo. Es otra fuente de verdad que mantener:
   bloquear a un usuario en SPLG no lo saca de RTDB hasta que venza su token
   (hasta una hora).

Cualquiera de los dos duplica una autorización que hoy vive en un solo lugar.
Un error en las reglas expone la ubicación de choferes en vivo, que es un dato
sensible.

### 5.4 Qué se rompe: ¿quién alimenta Redis GEO?

El despacho necesita la posición de **choferes libres**, que no tienen
`order_id`. La propuesta sólo escribe en `/viajes/{order_id}` durante la
entrega, así que el chofer **igual tiene que seguir mandando su posición por
socket** cuando está libre. Opciones:

| Opción | Problema |
|---|---|
| El chofer escribe en los dos (socket siempre + RTDB en viaje) | Doble canal, doble batería, doble manejo de reconexión. H-86/H-87 siguen en el socket |
| El back escucha RTDB con el Admin SDK y actualiza Redis | Un listener por instancia: con varias instancias se duplica, con una sola vuelve el punto único de falla que el adaptador Redis resolvió |
| Cloud Function en cada escritura → Redis | Latencia, costo por invocación, una pieza más desplegada y el VPC/Redis tiene que quedar alcanzable desde Google |

En los tres casos, **lo único que se saca del back son las ~20 líneas de
reenvío** de `handleDriverLocation`. Todo lo demás se mantiene y se agrega
Firebase RTDB, reglas y un segundo canal.

### 5.5 Multi-tenencia

Hoy las salas y consultas van por distribuidora en el back. En RTDB habría que
poner la distribuidora en la ruta (`/viajes/{distribuidoraId}/{orderId}`) y
replicar el aislamiento en las reglas. Los hallazgos H-77..H-84 (aislamiento)
se trabajaron en el back; con RTDB aparece una segunda superficie que también
hay que probar contra la API. Además, un proyecto de Firebase compartido entre
distribuidoras concentra el límite de conexiones y la factura.

### 5.6 Veredicto sobre RTDB

Resuelve bien dos problemas chicos (estado al reconectar y token vencido)
**sólo para la posición**, a cambio de un canal más, una autorización duplicada
y sin sacar el socket. Los mismos dos problemas se resuelven en el canal
actual con menos código (§8, camino A). **No conviene adoptarlo**; conviene
documentarlo como alternativa evaluada.

Fuentes:
- Reglas con `auth` y `root`: https://firebase.google.com/docs/database/security/rules-conditions
- Offline, `onDisconnect`, token al reconectar: https://firebase.google.com/docs/database/flutter/offline-capabilities
- Precios y límites: https://firebase.google.com/pricing

---

## 6. El prompt maestro, punto por punto

| # | Afirmación o propuesta | Estado real | Veredicto |
|---|---|---|---|
| 1 | Socket.IO + Redis genera "sobrecarga extrema de IOPS" en Postgres | **Falso.** La posición va a Redis GEO (`GEOADD`, O(log N)) y al socket; Postgres no se toca (CU-017 lo dice explícitamente). 10 choferes emitiendo cada 10 m son unos pocos mensajes por segundo; Redis maneja decenas de miles | Descartar el argumento |
| 2 | Llevar el stream a Firebase RTDB sin pasar por NestJS | Posible, pero no saca el socket (ver §5.4) | No adoptar; documentar como alternativa |
| 3 | Frecuencia fija de 3-5 s | Hoy es por distancia (10 m). Por distancia ahorra batería y no manda nada con el vehículo parado | Mejorar combinando: 10 m **o** cada 15-20 s como máximo, para que el cliente vea que la app está viva aunque el chofer esté frenado |
| 4 | Redis GEO sigue para la flota activa | Ya es así | Hecho |
| 5 | Eliminar `customer.lat_lang` | Hecho (punto PostGIS `location`) | Hecho |
| 6 | Eliminar `delivery.latLng` | Hecho | Hecho |
| 7 | Eliminar `delivery.isTraveling` | Hecho | Hecho |
| 8 | Eliminar `delivery.actual_location` | Sigue vivo: se escribe en el registro y en `delivery.service.ts:292-299`, y está en el DTO | **Adoptar**: es una copia vieja de un dato que vive en Redis. Borrarlo pide revisar el alta del chofer y el panel |
| 9 | Usar `order.deliveryLatitude/Longitude` para la coordenada donde el chofer tocó "Confirmar entrega" | **Choca** con la decisión del 26/09: esas columnas pasaron a `order.deliveryPoint` y significan el **destino** (lo usan el despacho y el mapper) | **No adoptar tal cual.** La idea es buena como auditoría, pero va en un campo aparte: `order.delivered_point` (punto PostGIS) + `delivered_at`, o en el registro de auditoría del cambio de estado. Permite medir la distancia real entre destino y confirmación y detectar entregas "confirmadas desde la base" |
| 10 | Deep link a Waze / Google Maps para el chofer | **Ya existe** (`navigation_launcher.dart`) | Hecho. Detalle menor: el de Google Maps no fuerza la navegación; se puede agregar `&dir_action=navigate` |
| 11 | Interpolar el marcador en el cliente | No existe: el marcador salta | **Adoptar**: animar entre la posición anterior y la nueva durante el intervalo esperado. Es sólo del cliente |
| 12 | Rotar el marcador | El cliente ya lo intenta, pero el rumbo nunca llega (§2) | **Adoptar**: que la app del chofer mande `heading` (`Position.heading` de geolocator) y que el back lo reenvíe; o calcularlo en el cliente entre dos posiciones |
| 13 | Negociación secuencial de asignación | Ya implementada | Hecho. Pendiente propio: parametrizar TTL y radios (C4) |
| 14 | M1 planificación de flota con "telemetría histórica GPS consolidada al finalizar los viajes" | Tablas creadas (`vehicle_usage_log` con `km`, `orders`, `route_hours` por vehículo y día); sin servicio. Hoy **no queda histórico de recorridos** | **Adoptar la idea, no la forma.** No guardar la traza cruda: acumular la distancia del viaje (suma de haversine entre posiciones consecutivas) en Redis o en la app, y al entregar sumarla a `vehicle_usage_log` del día. Es lo que ya prevé MODULOS-INTELIGENTES.md (evento `order.delivered` acumula km). Ojo: hoy las posiciones con el socket caído se pierden, así que el km se subestima; conviene acumular en la app y mandar el total al confirmar |
| 15 | M2, M3, M4 | Especificados, tablas creadas, sin servicios | Sin cambios: el prompt no agrega nada que no esté en MODULOS-INTELIGENTES.md |
| 16 | "Cinco procesos autónomos" | La cátedra evalúa contra C1-C5; el despacho y el reintento son el mismo pipeline (MODULOS-INTELIGENTES.md §3) | No presentar cinco: mantener el conteo de MODULOS-INTELIGENTES.md |

---

## 7. Impacto en la tesis

**Qué conviene defender: desarrollar, no integrar.** Tres razones:

1. **El dominio lo exige.** Flota propia, vehículos habilitados para mercancía
   peligrosa, recupero de envases en la misma visita: ninguna plataforma de
   delivery lo cubre, y las SaaS de flota imponen su propia app de chofer.
2. **Es trabajo evaluable.** El tracking con identidad por token, Redis GEO,
   adaptador para escalar horizontalmente y despacho secuencial con ofertas
   que vencen es diseño propio. Tercerizarlo deja a la tesis sin su parte
   técnica más visible.
3. **Haber evaluado alternativas es un plus.** Una sección "Alternativas
   evaluadas" con este análisis (tercerización, SaaS de flota, Firebase RTDB)
   y el porqué de la decisión es exactamente lo que un tribunal pregunta.

**Impacto en la documentación, según el camino:**

| Camino | CU | DSS / DSD | Modelo |
|---|---|---|---|
| A (recomendado) | CU-017: corregir el comentario sobre el `userId` y agregar el rumbo. CU-020 / CU-079: agregar que se guarda la coordenada de confirmación. H-86/H-87 como excepciones de reconexión | DSS de CU-017 casi igual; agregar `order:snapshot` al reconectar | `order.delivered_point` (+ `delivered_at` si no está); borrar `delivery.actual_location` |
| B (RTDB) | Reescribir CU-017, CU-018 (crear nodo), CU-020 (borrar nodo). Aparece un actor externo (Firebase RTDB) | DSD nuevo con tres canales (socket, RTDB, Redis) | Reglas de RTDB como artefacto aparte |
| C (SaaS) | Casi todos los CU del chofer pasan a ser "el sistema externo hace…" | Los DSD pierden detalle propio | El vehículo y la tarea pasan a vivir afuera |
| D (tercerizar) | Desaparecen los CU del chofer, la flota, M1 y M4 | — | Se cae media base |

**Módulos inteligentes:** el camino A no toca M2 ni M3, y le da a M1 su insumo
(km por vehículo y día) con muy poco código. M3 (agrupar por recorrido) puede
usar la misma posición en Redis. Con C o D, M1 y M4 pierden sentido.

**Qué queda como trabajo propio evaluable (camino A):** gateway con identidad
por token, radar GEO, despacho secuencial parametrizable, recuperación de
estado al reconectar, auditoría de la entrega por coordenada y consolidación de
km para M1.

---

## 8. Opciones

| | A. Socket + Redis, cerrar huecos | B. Híbrido RTDB para el stream | C. SaaS de flota propia | D. Tercerizar la entrega |
|---|---|---|---|---|
| **Qué es** | Mantener lo que hay; cerrar H-86/H-87; rumbo, interpolación, cadencia mixta, `delivered_point`, km para M1 | Chofer escribe en RTDB durante la entrega; socket sigue para ofertas y flota libre | Onfleet / Shipday / Fleet Engine hacen chofer, tracking y seguimiento | Uber Direct / PedidosYa / Rappi Cargo entregan |
| **Esfuerzo** | 4-6 días: H-86 (`order:snapshot` al reconectar o `GET /orders/:id`) 1 día; H-87 (`getIdToken(true)` al reintentar) 0,5 día + reproducirlo; rumbo + interpolación 1-1,5 días; `delivered_point` + migración 0,5 día; km acumulados 1 día; pruebas contra la API y docs el resto | 6-10 días: reglas, ACL, alta y baja de nodos, pruebas de aislamiento, doble canal en la app, docs. Y además hay que hacer igual H-87 en el socket | 3-6 semanas de integración, y se descartan la app del chofer y el despacho | Integración 1-2 semanas; en la práctica **inviable** |
| **Costo mensual** | USD 0 adicional (misma infraestructura) | ≈ USD 0 a esta escala (Blaze, dentro del cupo gratis); crece con choferes × frecuencia | Shipday USD 0-99; Onfleet desde USD 619; HyperTrack mínimo USD 300; Fleet Engine sin precio público y con contrato | Comisión por envío, sin tarifa pública para Posadas |
| **Riesgos** | Bajos. Conocido y probado | Autorización duplicada, error de reglas = ubicación expuesta, dos canales que fallan distinto, más superficie de multi-tenencia | Lock-in fuerte, se pierde el módulo de despacho, costo en USD por tarea, SDK sin Flutter (Fleet Engine) | Prohibición de inflamables (Uber explícito), normativa GL-42 / Decreto 779/95, sin flota propia no hay M1/M4, cobertura en Posadas sin verificar |
| **Para la tesis** | Máximo trabajo propio | Defendible, pero agrega complejidad sin un problema que la justifique | Se debilita mucho | Se cae el dominio |

### Recomendación

**Camino A.** Es el más barato, el único que no rompe nada y el que deja más
trabajo propio para mostrar. El orden sugerido:

1. H-87 primero (es ALTO): reproducirlo con la app y refrescar el token antes de
   cada reintento de conexión.
2. H-86: al reconectar, el servidor emite `order:snapshot` con el estado y la
   última posición conocida (que ya está en Redis).
3. Rumbo en el mensaje + interpolación del marcador en el cliente.
4. `order.delivered_point` en la confirmación de entrega (CU-020 / CU-079),
   separado de `deliveryPoint`.
5. Acumular km por viaje y volcarlos a `vehicle_usage_log` al entregar (insumo
   de M1).
6. Borrar `delivery.actual_location`.
7. Agregar a la tesis una sección "Alternativas evaluadas" con este análisis.

B queda como plan de contingencia **sólo** si en producción aparece un problema
medido de escala en el socket que el adaptador Redis no resuelva, cosa que a la
escala de una distribuidora de Posadas no es esperable.

---

## 9. Lo que no se pudo verificar

- Cobertura de Uber Direct, PedidosYa Envíos y Rappi Cargo en Posadas.
- Política de PedidosYa, Rappi Cargo y DiDi sobre GLP / garrafas (la de Uber sí
  es explícita).
- Si existe una API pública de DiDi Entrega Business para Argentina.
- Precio de Fleet Engine: sólo por contrato. El rango USD 0,10-0,15 por viaje es
  de un blog de terceros.
- Precio de Tookan: sale de una reseña de terceros, no de la página oficial.
- SDK Flutter oficial de Ably y Radar.
- La cuenta de consumo de RTDB (§5.2) es una estimación, no una medición.
- H-87 sigue **sin reproducir**; la recomendación de atacarlo primero se basa
  en su severidad declarada.
