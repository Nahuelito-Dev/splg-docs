# Relevamiento del panel y las dos apps

Los tres clientes por dentro: arquitectura, pantallas, manejo de errores, código
muerto y qué hace falta para que corran. Todo verificado contra el código y
contra lo que compila; los hallazgos que se citan acá se comprobaron uno por
uno abriendo el archivo.

---

## Resumen

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

## 1. Lo que ningún usuario ve: los errores invisibles

Es el patrón que comparten los tres, y el más caro de arreglar después.

### Panel — seis tablas que mienten

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

### App cliente — la excepción muere en el datasource

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

### App chofer — pasos críticos sin aviso

Aceptar un pedido: si la llamada falla, sólo se escribe en consola. **El diálogo
ya se cerró y el chofer cree que aceptó.** Lo mismo al ponerse disponible, al
rechazar, y en el reporte de posición: si el socket está caído, la posición se
descarta sin reintento.

---

## 2. Los tres hallazgos que afectan una demostración

### El seguimiento en vivo sólo funciona en localhost

La app cliente configura la API por `--dart-define`, pero la URL del socket está
fija:

```dart
static const String _socketBaseUrl = 'http://localhost:3000/customers';
```

No pasa por `AppConfig`. En un teléfono real, el cliente **nunca ve moverse al
chofer**.

### La entrega no la marca el chofer

La app del chofer **no llama nunca** a `confirm-delivery`. Muestra un QR, **lo
escanea el cliente**, y el chofer se entera porque consulta el pedido cada cinco
segundos hasta ver `delivered`.

Para mostrar el recorrido completo hacen falta **las dos apps funcionando a la
vez**, no sólo la del chofer.

### "Cerrar sesión" no cierra la sesión

En la app del chofer, el `logout()` sólo frena el GPS y navega al login. No llama
a `signOut()` de Firebase, no desconecta el socket y **no marca al chofer como no
disponible**: sigue recibiendo ofertas de pedidos.

---

## 3. Seguridad

### El token queda escrito en el log del dispositivo

App del chofer: `PrettyDioLogger` con `requestHeader: true` y
`requestBody: true`, **sin guarda de `kDebugMode`** —que no aparece en ninguna
parte del código—. En una compilación de producción, cada `Authorization:
Bearer` y cada contraseña del login quedan en el log.

### Un archivo entero sin verificación de tipos

`src/firebase/providers.ts` empieza con `// @ts-nocheck`. Es el archivo que
maneja el inicio de sesión del panel.

### Claves versionadas

La clave de Google Maps está en `AndroidManifest.xml` y en `AppDelegate.swift`,
y las de Firebase en `firebase_options.dart`. Son claves que por diseño viajan
en el cliente, pero conviene saber que están en el repositorio.

---

## 4. Arquitectura

### Panel — siete mecanismos de estado conviviendo

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

### App cliente — MVVM sobre Stacked, con la separación a medias

Cero `setState` en todo el código, lo cual es consistente. El camino completo
(vista → viewmodel → servicio → caso de uso → repositorio → datasource) se
respeta **sólo para pedidos, clientes, garrafas y direcciones**.

Cinco servicios instancian el datasource directo sin repositorio ni caso de uso,
y `OrderTrackingService` usa el cliente HTTP crudo salteándose toda la capa de
datos. Los siete casos de uso son un `call()` de una línea: hoy no agregan nada.

### App chofer — la más simple y la más sólida en su flujo

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

## 5. Código muerto

| | Qué hay |
|---|---|
| **Panel** | 5 archivos de 0 bytes · 8 componentes inalcanzables · 10 barrels sin importador · 31 exports sin usar · 7 endpoints implementados que ninguna pantalla llama · `chart.js` y `react-chartjs-2` instalados con **cero importaciones** |
| **App cliente** | `BusinessHours` (66 líneas, huérfano) · `Market`, `NoticeSheet` e `InfoAlertDialog` registrados y nunca invocados · un cliente inventado hardcodeado (`customerId: '1234'`) como valor inicial |
| **App chofer** | `order_service.dart`: **153 líneas con 6 pedidos falsos** tras un `Future.delayed(2s)`, referenciado sólo por el locator · `DirectionsView` registrada sin llamadores · botones vacíos en notificaciones y "olvidé mi contraseña" |

---

## 6. Qué hace falta para correr cada uno

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

## 7. Las pruebas

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
