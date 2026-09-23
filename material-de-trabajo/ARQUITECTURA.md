# Arquitectura del backend — qué tenemos y qué refactorizar

Documento interno. No es para presentar: es para decidir en qué orden tocamos el
código. Todo lo que dice está verificado contra el repositorio y contra la API
corriendo el 23/09/2026, con la batería de los 131 endpoints.

La pregunta que contesta es una sola: **¿la API está armada como para sostenerse,
mantenerse y crecer?** La respuesta corta es que los cimientos están bien puestos
y el problema está en el borde de entrada: la capa que recibe los datos del mundo.

---

## 1. Qué hay

| Pieza | Cantidad |
|---|---|
| Módulos (`*.module.ts`) | 26 |
| Controladores | 22 (131 endpoints) |
| Servicios | 27 · Casos de uso 5 |
| DTOs | 52 archivos |
| Entidades TypeORM | 22 (20 reales + 2 archivos vacíos) |
| Puertos (`abstract class *Port`) | 9 · Adaptadores 8 |
| Guards | 5 · Interceptores 4 · Filtros 1 · Decoradores propios 5 |
| **Pipes propios** | **0** |
| Archivos de prueba | 18 |

Stack: NestJS + TypeORM + PostgreSQL/PostGIS + Redis · Firebase para identidad ·
MercadoPago para cobros · Socket.io sobre Redis para tiempo real.

Sólo `order` y `payments` tienen la estructura completa
`domain/ · application/ · infrastructure/`. Los otros 24 módulos son
controlador → servicio → repositorio, planos.

---

## 2. Qué nos da Nest y cuánto lo estamos usando

| Lo que Nest ofrece | Para qué sirve | Cómo estamos |
|---|---|---|
| Módulos e inyección de dependencias | Aislar, sustituir y testear | **Bien.** 26 módulos, 9 puertos con token de DI |
| Guards | Autorizar antes de entrar al controlador | **Bien.** 3 globales: throttle, auth, roles |
| Interceptores | Atravesar todas las peticiones | **Bien**, con una duplicación a corregir |
| Filtros de excepción | Una sola forma de contestar un error | **Bien.** Un filtro global |
| **DTOs + class-validator** | Que no entre basura al dominio | **Mal. Es el agujero principal** |
| **Pipes** | Transformar y validar en el borde | **A medias.** El `ValidationPipe` global está bien configurado, pero no hay ninguno propio |
| Decoradores propios | Sacar ruido repetido del controlador | **Bien.** 5, incluido uno de idempotencia |
| Puertos y adaptadores | No atarse a un proveedor | **Bien**, con tres inconsistencias |

**El resumen:** todo lo transversal está bien resuelto. Lo que falla es lo
específico de cada endpoint, que es justamente lo que no se puede resolver de
forma global y hay que escribir uno por uno.

---

## 3. El camino de una petición

```
petición
  → AppThrottlerGuard    limita llamadas por IP
  → AuthGuard            valida el token de Firebase y arma request.user
  → RolesGuard           compara el rol contra @Roles
  → LoggingInterceptor   registra método, ruta, código y duración
  → TimeoutInterceptor   corta si tarda de más
  → IdempotencyInterceptor  evita procesar dos veces la misma petición
  → ValidationPipe       valida y transforma el cuerpo contra el DTO
  → Controlador → Servicio / caso de uso → Repositorio o Puerto → Postgres
  → GlobalExceptionFilter  traduce la excepción a una respuesta uniforme
```

Los guards e interceptores están registrados **globalmente** en `app.module.ts`
con los tokens de Nest, no colgados controlador por controlador:

```ts
{ provide: APP_GUARD, useClass: AppThrottlerGuard },
{ provide: APP_GUARD, useClass: AuthGuard },
{ provide: APP_GUARD, useClass: RolesGuard },
{ provide: APP_INTERCEPTOR, useClass: LoggingInterceptor },
{ provide: APP_INTERCEPTOR, useClass: TimeoutInterceptor },
```

Esto está bien y conviene mantenerlo: un controlador nuevo **nace protegido**, y
para abrirlo hay que escribir `@Public()` a propósito. La seguridad es
*opt-out*, no *opt-in*. Medido contra la API: de 131 endpoints, **115 exigen
token**. Los 16 restantes son los `@Public()`.

### Refactor pendiente acá
`TimeoutInterceptor` se registra **dos veces**: en `main.ts:37` con
`useGlobalInterceptors` y en `app.module.ts:171` como `APP_INTERCEPTOR`. Se
aplica dos veces a cada petición. Sacar el de `main.ts`.

---

## 4. DTOs, pipes y validación — acá está el problema

El `ValidationPipe` global está bien configurado:

```ts
// main.ts:39
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,            // descarta campos no declarados
  forbidNonWhitelisted: true, // y si vienen, rechaza con 400
  transform: true,            // convierte el JSON en la clase del DTO
}));
```

`whitelist` + `forbidNonWhitelisted` frenan el *mass assignment*: mandar un
`role_id` en un registro muere en el pipe. Eso está resuelto.

**El problema es que el pipe no puede hacer nada donde no hay DTO.** Un tipo de
TypeScript no existe en tiempo de ejecución: sin una clase con decoradores,
`class-validator` no tiene contra qué validar y deja pasar cualquier cosa.

Hay **11 endpoints así**, verificados uno por uno:

| Archivo y línea | Cuerpo declarado |
|---|---|
| `users.controller.ts:152` | `{ email?: string; phoneNumber?: string }` |
| `users.controller.ts:222` | `{ block: boolean }` |
| `delivery.controller.ts:119` | `{ latLng: string; actualLocation?: string }` |
| `delivery.controller.ts:136` | `{ amount: number }` |
| `delivery.controller.ts:149` | `{ isActive: boolean }` |
| `delivery.controller.ts:170` | `{ available: boolean }` |
| `gascylinder.controller.ts:108` | `{ quantity: number }` |
| `notifications.controller.ts:32` | `{ token, title, body }` |
| `notifications.controller.ts:48` | `{ customerId, orderId, token? }` |
| `notifications.controller.ts:74` | `{ userId, token, platform }` |
| `customer.controller.ts:118` | `{ latLng: string }` |

### Qué provoca esto, medido

- **`PATCH /gascylinder/{id}/stock`** con un valor no numérico llega hasta
  Postgres y revienta: `invalid input syntax for type integer: "NaN"`. **500.**
- **`POST /users/check-exists`** con `{"email": 12345}` responde **201**, no 400.
- **`PATCH /customers/{id}/location`** acepta el campo mal escrito
  (`lat_lang` en vez de `latLng`) y devuelve **200** sin actualizar nada. El
  peor de los tres: no falla, miente.

No es una objeción de estilo. Sin DTO, **la validación queda en manos de la base
de datos, y la base contesta con 500 o con silencio.**

### El refactor
Un DTO por cada uno de los 11, con el decorador que corresponda
(`@IsInt()`, `@Min(0)`, `@IsBoolean()`, `@IsUUID()`, `@IsLatLong()`). Son clases
de cinco líneas. Es el refactor con mejor relación entre esfuerzo y resultado de
toda la lista.

Además hay **9 DTOs que no se usan en ningún lado** (`UpdateOrderDto`,
`UpdateClaimDto`, `UpdateEmailDto`, `UpdateNotificationDto`, `UpdatePositionDto`,
`UserUniqueFieldsDto` y los tres del catálogo público): o se usan o se borran.

### Pipes propios: cero
No hay ninguno. Hay dos lugares donde uno se justifica:
- Un `ParseLatLngPipe`, porque la latitud y la longitud se repiten en varios
  módulos con formatos distintos (string `"lat,lng"` en unos, campos separados
  en otros).
- Un pipe de paginación, hoy resuelto a mano en los 9 controladores que paginan.

---

## 5. SOLID, con evidencia

| Principio | Dónde se cumple | Dónde no, y qué hacer |
|---|---|---|
| **S** · Responsabilidad única | Los 5 casos de uso de `order/application` hacen una cosa cada uno | `OrderController` tiene **447 líneas y 19 endpoints**, con lógica propia: un `switch` en `:51`, un 403 a mano en `:94`, `withTransactionRetry` en `:106`, cuatro `.map`. **`CreateOrderUseCase` recibe 15 dependencias.** Extraer la reserva de stock y el cálculo de precio a colaboradores propios |
| **O** · Abierto/cerrado | Sumar una pasarela de pago es un adaptador nuevo sin tocar el caso de uso | El despacho tiene `OFFER_TTL_SECONDS` y `RADIUS_STEPS_KM` como constantes de clase: cambiar el comportamiento exige recompilar. Llevarlas a configuración |
| **L** · Sustitución | Los adaptadores respetan la firma de su puerto | Sin casos problemáticos |
| **I** · Segregación | Los puertos son chicos y de un propósito (`FcmPort` sólo manda push) | `OrderRepositoryPort` es el más grande; conviene partirlo cuando se toque |
| **D** · Inversión | 9 puertos, **los 9 registrados** con token de DI | Tres inconsistencias, abajo |

### Las tres inconsistencias de inversión de dependencias

1. **`DispatchOrchestratorService` mezcla los tres niveles en un constructor:**
   tres puertos, un `Repository<Delivery>` crudo de TypeORM, y la clase concreta
   `NotificationsService` — teniendo `NotificationPort` registrado **en su propio
   módulo**. Lo revelador: `UpdateOrderStatusUseCase`, al lado, **sí** usa
   `NotificationPort`. No es una decisión de diseño, es una inconsistencia entre
   hermanos. Cambiar la dependencia al puerto es una línea.
2. **`OrderService` inyecta a la vez `OrderRepositoryPort` y los repositorios
   crudos** de `Order` y `Delivery`. El puerto deja de ser la única puerta a los
   datos, que era lo que le daba sentido. Pasa lo mismo en
   `create-order.use-case.ts`, `update-order-status.use-case.ts`,
   `reservation.service.ts` y `confirm-payment.use-case.ts`.
3. **`OwnershipGuard` existe y no se usa en ningún lado.** La pertenencia se
   controla a mano dentro de los servicios (`assertOwnership` en
   `user-addres.service.ts` y duplicado en `customer.service.ts`). **Funciona**
   —lo verifiqué contra la API—, pero está resuelto servicio por servicio en vez
   de estar en el guard que ya está escrito. O se usa el guard, o se borra.

Sobre los 24 módulos planos: **no hay que convertirlos todos a hexagonal.** La
separación se justifica donde hay reglas de negocio que la paguen. Meter
`domain/application/infrastructure` en un CRUD de franjas horarias agrega
carpetas y no agrega nada.

---

## 6. Duplicación que hay que atacar

- **`registerWithUser`** — unas 40 líneas casi idénticas entre
  `delivery.service.ts:40-118` y `customer.service.ts:44-123`. Y las dos versiones
  **no se comportan igual**: la de clientes resuelve la distribuidora por defecto
  y la de choferes no, lo que produce un 500 (ver abajo).
- **`handleDBExceptions`** — repetido en 6 servicios; entre `car.service.ts` y
  `user-addres.service.ts` es idéntico byte a byte.
- **`assertOwnership`** — duplicado, existiendo `OwnershipGuard`.
- Los tres helpers de registro, duplicados entre `admin/helpers/` y `users/helpers/`.
- Dos entidades **vacías**, de una línea y sin `@Entity`: `email.entity.ts` y
  `notification.entity.ts`. Borrarlas.

---

## 7. Estabilidad: cómo se comporta cuando algo sale mal

Esto es lo que define si la API se puede operar.

### El manejo de errores tapa la causa
`handleDBExceptions` sólo contempla dos códigos de Postgres:

```ts
if (error.code === '23505') → 400 'Duplicate entry'
if (error.code === '23503') → 400 'Foreign key constraint failed'
// cualquier otra cosa:
throw new InternalServerErrorException('Unexpected error, check server logs');
```

**Nunca registra el error original.** El mensaje manda a mirar unos logs donde la
causa no está. Es lo que hizo que tardáramos en encontrar el 500 del registro de
choferes.

Refactor: un único helper compartido que (a) registre el error antes de
convertirlo, y (b) contemple `23502` (NOT NULL) y `22P02` (sintaxis inválida).
Con eso, dos de los tres 500 pasan a ser 400 con mensaje.

### Los tres 500 encontrados en 131 endpoints

| Endpoint | Causa | Debería ser |
|---|---|---|
| `DELETE /role/{id}` | Borra un rol con usuarios: violación de FK sin atrapar | 409 "el rol está en uso" |
| `POST /users/delivery-registration` | `distributor_id` es NOT NULL pero el DTO lo marca opcional | 400 diciendo qué falta |
| `PATCH /gascylinder/{id}/stock` | Sin DTO: un no-numérico llega a la base | 400 de validación |

Tres de 131 es un número bajo, y los tres tienen la misma raíz: **el borde de
entrada no valida, y el manejo de errores no traduce.**

### Transacciones e idempotencia
12 archivos usan `queryRunner` o `withTransactionRetry`, y hay un
`IdempotencyInterceptor` con su decorador. Esto está bien resuelto y es
importante que siga así: el alta de pedido reserva stock y cupo de franja de
forma atómica, y el webhook de MercadoPago no puede procesarse dos veces.

---

## 8. Escalabilidad

Lo que está bien y conviene no romper:

- **Índices declarados en 15 de 20 entidades** (`order` tiene 8, `dispatch-offer`
  6, `cylinder` 4). No es un esquema sin índices.
- **`eager: true` no aparece ni una vez** en todo `src/`. Eso evita el problema
  clásico de TypeORM de traer medio grafo en cada consulta.
- **Socket.io con adaptador de Redis**, así que las salas sobreviven a tener más
  de una instancia. Sin eso, el despacho y el seguimiento se romperían en
  silencio al escalar horizontalmente.
- **Lock distribuido en el cron de despacho** (`dispatch:tick`, TTL 12 s < 15 s
  del cron), para que dos instancias no procesen el mismo tick.

Lo que hay que mirar:

- **Paginación resuelta a mano en 9 controladores**, cada uno a su manera. Un
  DTO de paginación compartido, o un pipe.
- **12 servicios cargan `relations:`**, que es donde suele aparecer el N+1.
  Conviene medirlo con el log de SQL encendido (`DB_LOGGING=true`) sobre los
  listados del panel antes de que crezcan los datos.
- `cascade: true` en 5 lugares (`order.entity.ts` y `user.entity.ts`). Está
  acotado, pero conviene saber que está.

---

## 9. En qué orden lo haría

Ordenado por lo que rinde contra lo que cuesta:

1. **Los 11 DTOs faltantes.** Clases de cinco líneas. Cierran dos de los tres 500
   y el caso peor, el del update que miente. Sin esto, la API no es confiable
   en el borde.
2. **El helper de errores unificado**, que registre la causa y contemple `23502`
   y `22P02`. Convierte 500 opacos en 400 con mensaje.
3. **Seguridad del acceso** — es lo que más importa y no es refactor, es defecto:
   `GET /users/email/{email}` expone el usuario completo sin token; el login le
   da token a un usuario dado de baja; el login devuelve el `refreshToken` y el
   `apiKey` de Firebase por no tener DTO de respuesta.
4. **`TimeoutInterceptor` duplicado** y **las dos entidades vacías**. Cinco
   minutos.
5. **`OwnershipGuard`:** usarlo o borrarlo, y sacar el `assertOwnership`
   duplicado.
6. **La dependencia concreta del orquestador de despacho** al puerto. Una línea.
7. **Unificar `registerWithUser`** entre clientes y choferes, que hoy se
   comportan distinto.
8. **Partir `OrderController` y `CreateOrderUseCase`.** Es el más grande y el que
   más cuesta; conviene hacerlo cuando haya que tocar pedidos por otra razón.

Lo que **no** haría: convertir los 24 módulos planos a hexagonal. Es mucho
trabajo, rompe lo que hoy anda, y no resuelve ninguno de los problemas reales
que tiene la API.

---

## Lo que viene de la revisión de arquitectura de julio

Aquella revisión (SOLID, DDD y escalabilidad) se resolvió **entera**: los diez
puntos P0, los seis P1 y todos los P2 salvo un renombre cosmético. Lo que sigue
valiendo de ella no son los hallazgos —ya cerrados— sino estas tres cosas.

### Lo que NO hay que romper al refactorizar

Es el núcleo transaccional, y es de calidad de producción:

Reserva de stock atómica (`SELECT FOR UPDATE` en la tx del use-case) · webhook MP idempotente (lock + índice único parcial + carrera pago-vs-expiración) · despacho secuencial durable (tabla de ofertas + lock distribuido + radio progresivo) · cupo de franjas con lock transaccional · `StockReservationService` recibiendo el `EntityManager` del caller · state machines puras y testeadas · GEO en Redis · PostGIS con GIST + corto-circuito "sin zonas = cubierto" · precios de servidor en checkout · puertos abstractos como token DI.

Cualquier refactor que toque estas piezas necesita, antes, entender por qué
están así. La mayoría resuelve una carrera o un problema de concurrencia que no
se ve leyendo el camino feliz.

### Lo que NO conviene hacer, aunque se vea prolijo
- Hexagonalizar `car`/`time-slot`/`claims`/`incident`/`rating`/`gascylinder` — es CRUD legítimo.
- Forzar un `Money` VO en el catálogo (sí vale en `payments`, que ya usa `decimal.js`).
- Unificar YA los dos modelos de inventario (`GasCylinder.stock` vs unidades `Cylinder`) — para MVP es defendible, documentarlo como decisión.
- Mover enums de dominio fuera del `.entity.ts` — idiomático NestJS, baja prioridad.

---

### Pendientes menores que quedaron abiertos

**Follow-ups menores pendientes** (no bloqueantes): rename de entidades GasCylinder/Cylinder; `GET /users/email|:id|phone` permiten enumeración básica (se usan en el login de las apps); mapear a 409 finito si algún flujo dependía de hard-delete de usuarios; y los diferidos de prod en `../PENDIENTES-PROD.md` (AFIP, iOS APNs, rename de package a wagnerlabs, hosting de legales, rotar secretos, MP Fase 2).

_El detalle completo de aquella revisión está en `historico/`._
