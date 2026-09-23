# Auditoría adversarial de fidelidad documentación ↔ código — CU-031 a CU-060

**Documento auditado:** `docs/1-Requisitos.md`, sección 7 (Casos de Uso Expandidos).
**Código auditado:** rama de trabajo actual de `jennygas-app-backend`, directorio `src/`.
**Método:** para cada CU se contrastó actor (`@Roles` / `@Public` + `RolesGuard`), precondición,
cada paso de la secuencia normal, postcondición, excepciones, existencia real de la ruta y
aislamiento por `distributor_id`. Toda afirmación sobre el código está anclada a `archivo:línea`.

## Nota previa aplicable a todos los CU

1. **Prefijo global `api`.** `src/main.ts:18` ejecuta `app.setGlobalPrefix('api')`, de modo que
   toda ruta citada en la documentación sin ese prefijo (`POST /time-slots`, `PATCH /delivery/:id`)
   es, en el sistema real, `/api/...`. No se computa como discrepancia por CU; se señala una vez.
2. **El `RolesGuard` deja pasar sin `@Roles`.** `src/common/guards/roles.guard.ts:40-42`: si el
   handler y su controlador no declaran `@Roles(...)`, el guard retorna `true`. Un endpoint sin ese
   decorador queda abierto a **cualquier usuario autenticado**, cualquiera sea su rol.
3. **`ValidationPipe` con `forbidNonWhitelisted: true`** (`src/main.ts:39-42`): un query string o un
   body con una propiedad no declarada en el DTO devuelve **400**, no la ignora. Esto convierte
   varios "filtros" documentados en errores reales.

---

## Resumen

| CU | Veredicto | Una línea |
|----|-----------|-----------|
| CU-031 Registrar Chofer | **DISCREPANCIA GRAVE** | El código crea el chofer con `isActive = true` y acepta `validated` desde el body; la postcondición "no puede operar hasta ser validado" no la sostiene ningún control. |
| CU-032 Validar / Invalidar Chofer | **DISCREPANCIA GRAVE** | No hay `ZREM`, no hay control de pedido en curso, y `validated` no se lee ni en el radar ni al aceptar un pedido: invalidar no impide operar. |
| CU-033 Activar / Desactivar Chofer (Admin) | **DISCREPANCIA GRAVE** | La ruta `PATCH /delivery/:id/toggle-active` no existe; la real es `/status`, no invierte el flag, no toca Redis y no valida entrega en curso. |
| CU-034 Registrar Vehículo | DISCREPANCIA MENOR | Ruta `POST /cars` inexistente (es `/car`), la patente duplicada devuelve 400 y no 409, y los campos "requeridos" son todos opcionales salvo `user_id`, que el CU no menciona. |
| CU-035 Consultar Listado de Choferes | **DISCREPANCIA GRAVE** | La query documentada devuelve 400, no existen los filtros `validated`/`isActive`, no hay join con el vehículo ni respuesta paginada. |
| CU-036 Crear Producto | DISCREPANCIA MENOR | No se valida `precio > 0` ni `stock ≥ 0`; falta el campo obligatorio `weight`; el control de duplicado no distingue producto activo de inactivo. |
| CU-037 Actualizar Precio | DISCREPANCIA MENOR | El paso 3 ("valida que el nuevo precio sea mayor a cero") no existe: el DTO solo exige que sea numérico. |
| CU-038 Actualizar Stock | **DISCREPANCIA GRAVE** | El código **suma** el valor recibido al stock existente; la documentación afirma que es el valor absoluto resultante. |
| CU-039 Configurar Promociones | **DISCREPANCIA GRAVE** | Ruta inexistente y ninguna validación de las reglas: se puede cargar un descuento de 200 % y el checkout lo aplica. |
| CU-040 Activar / Desactivar Producto | DISCREPANCIA MENOR *(residual)* | Ya declarado como parcial; además la ruta documentada `PATCH /gas-cylinders/:id/toggle-active` no existe ni para desactivar (es `DELETE /gascylinder/:id`). |
| CU-041 Consultar Catálogo | **DISCREPANCIA GRAVE** | El listado es público (sin autenticación) y la vista de administrador —catálogo completo con inactivos y stock 0— no existe en ningún endpoint. |
| CU-042 Crear Franja Horaria | **DISCREPANCIA GRAVE** | Ni `endTime > startTime` ni `capacity > 0` se validan: las dos excepciones documentadas son inventadas y `capacity` es opcional. |
| CU-043 Modificar Capacidad de Franja | **DISCREPANCIA GRAVE** *(ya declarada)* | Confirmado: no existe `@Patch`/`@Put` en `time-slot.controller.ts`. |
| CU-044 Seleccionar Franja al Crear Pedido | DISCREPANCIA MENOR | `timeSlotId` es opcional en el DTO (no "debe elegir") y el conflicto de capacidad devuelve 400, no 409. |
| CU-045 Consultar Franjas Disponibles | **DISCREPANCIA GRAVE** | El endpoint es `@Public()`, no valida la fecha pasada (excepción inventada) y los campos de la respuesta tienen otros nombres. |
| CU-046 Gestionar Direcciones | DISCREPANCIA MENOR | Los once pasos y todas las excepciones se verifican; solo la postcondición "siempre hay una predeterminada" no se sostiene. |
| CU-047 Recuperar Contraseña | FIEL | Rate limit 10/hora en Redis, caché de 30 min, mensaje genérico ante email inexistente y envío best-effort: todo verificado. |
| CU-048 Procesar Pago con MercadoPago | FIEL | Los 14 pasos, las excepciones y las limitaciones declaradas (rechazo sin acción, `TODO` explícito) coinciden con el código. |
| CU-049 Balance del Chofer | FIEL | Suma acumulativa, ausencia de DTO, lectura sin restricción de rol: la documentación lo declara y el código lo confirma. |
| CU-050 Bloquear / Desbloquear Usuario | FIEL | El comportamiento y su limitación (el bloqueo no bloquea) están correctamente declarados en el propio CU. |
| CU-051 Gestionar Vehículos | FIEL | Aislamiento por distribuidora, 404 indistinto, baja física y búsqueda por patente con cuerpo vacío: todo verificado. |
| CU-052 Registrar Distribuidora | FIEL | `@Roles(SUPER_ADMIN)` a nivel de clase, slug único con 409, validación de formato en el DTO. |
| CU-053 Consultar Distribuidoras | DISCREPANCIA MENOR | El CU promete consulta "por ID **o slug**"; el controlador solo expone la consulta por ID. |
| CU-054 Modificar Distribuidora | FIEL | Actualización parcial con 404 previo, verificado. |
| CU-055 Dar de Baja Distribuidora | FIEL | `softRemove` con verificación previa de existencia. |
| CU-056 Definir Zona de Cobertura | FIEL | Tenant tomado del contexto, 400 ante DTO inválido o falta de distribuidora. |
| CU-057 Consultar Zonas | FIEL | Consulta restringida al tenant, con `{ required: true }` que bloquea si no hay contexto. |
| CU-058 Validar Cobertura | FIEL | `ST_Contains`, cobertura total con recargo 0 si no hay zonas, `covered: false` sin error HTTP. |
| CU-059 Eliminar Zona | FIEL | Borrado físico previa verificación de pertenencia al tenant, 404 indistinto. |
| CU-060 Registrar Incidencia | **DISCREPANCIA GRAVE** | El paso 3 promete verificar que el pedido "incumba a la organización" y el código no lo hace: se puede reportar sobre un pedido de otra distribuidora. |

**Conteo:** 12 FIEL · 7 DISCREPANCIA MENOR · 11 DISCREPANCIA GRAVE (dos de ellas —CU-040 residual
no, CU-043— ya declaradas en el documento) · 0 NO VERIFICABLE.

---

## Discrepancias encontradas

### CU-031 — Registrar Chofer · GRAVE

**Qué dice la documentación**

> Paso 5: "El sistema registra el usuario en la base de datos con rol `CHOFER` y crea el perfil
> `Delivery` con `validated = false` e `isActive = false`."
>
> Postcondición: "El perfil Delivery está creado con `validated = false`. El chofer no puede aceptar
> pedidos ni aparecer en el radar hasta ser validado mediante CU-032."

**Qué hace el código**

- `src/delivery/delivery.service.ts:90-93` — `isActive: createDeliveryDto.isActive !== undefined ? createDeliveryDto.isActive : true`.
  El valor por defecto es **`true`**, no `false`.
- `src/delivery/delivery.service.ts:89` — `validated: createDeliveryDto.validated || false`, pero
  `src/delivery/dto/create-delivery.dto.ts:50-56` expone `validated?: boolean` e `isActive?: boolean`
  como campos aceptados del body: el administrador puede crear un chofer ya validado y activo en la
  misma llamada, sin pasar por CU-032.
- El radar de despacho (`src/order/application/dispatch-orchestrator.service.ts:158-171` y
  `filterByDistributor`, líneas 178-189) filtra **solo por distribuidora**; nunca consulta `validated`.
- La aceptación de un pedido (`src/order/application/update-order-status.use-case.ts:115`) verifica
  `if (!delivery.isActive)` y **nada más**: no consulta `validated`.
- La única lectura de `validated` en todo `src/` fuera de las escrituras es un contador de dashboard
  (`src/order/order.service.ts:265`).
- Paso 3, "contraseña mínimo 6 caracteres": `src/delivery/dto/create-delivery.dto.ts:28-31` declara
  solo `@IsString()` y `@IsNotEmpty()`. La regla de longitud queda delegada a Firebase.
- Excepción del paso 4: el mensaje real ante email duplicado es
  `'User with this email already exists'` (`src/delivery/delivery.service.ts:51`), en inglés y
  emitido por el chequeo contra la base local, no por Firebase.

**Gravedad:** grave. La postcondición afirma una garantía de seguridad operativa que ningún control
del backend aplica.

**Corrección propuesta**

> Paso 5: "El sistema registra el usuario en la base de datos con rol `CHOFER` y crea el perfil
> `Delivery`. Si el body no especifica lo contrario, `validated` queda en `false` e `isActive` en
> **`true`**. Ambos campos son aceptados en el alta, de modo que el administrador puede crear un
> chofer ya validado y activo sin ejecutar CU-032."
>
> Postcondición: "Existe un nuevo usuario con rol CHOFER y su perfil `Delivery`. **`validated` es hoy
> un dato informativo: el sistema no lo consulta ni al armar el radar de asignación ni al aceptar un
> pedido, de modo que un chofer no validado que se ponga en línea puede recibir y aceptar pedidos.**
> El único control efectivo sobre la operación del chofer es `isActive` (ver CU-033)."
>
> Excepción del paso 3: "La longitud mínima de la contraseña no la valida el backend; la rechaza
> Firebase Authentication al crear el usuario."
>
> Excepción del paso 4: "Si el email ya está registrado en la base del sistema, se informa
> `User with this email already exists` antes de llamar a Firebase."

---

### CU-032 — Validar / Invalidar Chofer · GRAVE

**Qué dice la documentación**

> Descripción: "Un chofer con `validated = false` no puede aceptar pedidos ni aparecer en el radar de
> asignación, independientemente de su estado de disponibilidad."
>
> Paso 4: "Si se invalida y el chofer tiene su ubicación en Redis: el sistema ejecuta
> `ZREM drivers:locations driverId` para eliminarlo del radar."
>
> Excepción paso 3: "Si el chofer tiene un pedido activo en estado ACCEPTED u ON_THE_WAY y se intenta
> invalidar, el sistema informa 'El chofer tiene una entrega en curso...'"

**Qué hace el código**

- `src/delivery/delivery.service.ts:213-218` — `invalidateDelivery` es tres líneas: busca, pone
  `validated = false`, guarda. **No hay llamada a Redis** (comparar con
  `src/delivery/delivery.service.ts:266`, `this.redisService.removeDriver(userId)`, que sí existe pero
  solo dentro de `toggleAvailability`).
- **No hay ninguna consulta de pedidos** en `validateDelivery`/`invalidateDelivery`
  (`src/delivery/delivery.service.ts:206-218`): la excepción por entrega en curso no existe.
- La premisa de la descripción es falsa por lo ya detallado en CU-031: `validated` no se lee ni en
  `dispatch-orchestrator.service.ts:158-189` ni en `update-order-status.use-case.ts:115`.
- **Ruta alternativa sin protección:** `src/delivery/delivery.controller.ts:77-87` expone
  `@Patch(':id')` **sin `@Roles`**, y `src/delivery/dto/update-delivery.dto.ts:4` define
  `UpdateDeliveryDto extends PartialType(CreateDeliveryDto)`, que incluye `validated`, `isActive`,
  `calification` y `distributorId`. Por el comportamiento del `RolesGuard`
  (`src/common/guards/roles.guard.ts:40-42`), **cualquier usuario autenticado —un cliente, otro
  chofer— puede autovalidarse o invalidar a un tercero** con
  `PATCH /api/delivery/:id { "validated": true }`. El actor declarado del CU (solo administrador) es
  falso en la práctica.

**Gravedad:** grave. Combina una promesa funcional no implementada (Redis, control de entrega en
curso), una premisa de seguridad falsa y un actor incorrecto por una ruta desprotegida.

**Corrección propuesta**

> Descripción: "El administrador cambia el flag `Delivery.validated` mediante dos endpoints
> dedicados. **⚠️ El flag es hoy meramente declarativo: ningún punto del backend lo consulta.** El
> radar de asignación filtra por distribuidora y por presencia en Redis, y la aceptación de un pedido
> verifica únicamente `isActive`. Invalidar a un chofer no le impide seguir recibiendo ni aceptando
> pedidos."
>
> Paso 4: eliminar. La invalidación **no** ejecuta `ZREM` sobre `drivers:locations`; el chofer
> invalidado permanece en el radar hasta que él mismo se ponga fuera de línea (CU-022).
>
> Excepción paso 3 (entrega en curso): eliminar. El sistema no consulta los pedidos del chofer antes
> de invalidarlo.
>
> Agregar a Comentarios: "Además de los endpoints dedicados, `PATCH /delivery/:id` acepta `validated`
> e `isActive` en el cuerpo y **no declara `@Roles`**, por lo que cualquier usuario autenticado puede
> modificar el estado de validación de cualquier chofer. Corregir esa ruta es requisito para que el
> actor declarado en este CU sea real."

---

### CU-033 — Activar / Desactivar Chofer (Admin) · GRAVE

**Qué dice la documentación**

> Paso 3: "La app envía `PATCH /delivery/:id/toggle-active`."
> Paso 4: "El backend **invierte** `Delivery.isActive`."
> Paso 5: "Si pasó a `false`: ejecuta `RedisService.zRem('drivers:locations', deliveryId)` para
> quitarlo del radar."
> Excepción paso 4: "Si el chofer tiene un pedido en curso (ACCEPTED/ON_THE_WAY) y se intenta
> desactivar → 400 'El chofer tiene una entrega en curso.'"

**Qué hace el código**

- La ruta `PATCH /delivery/:id/toggle-active` **no existe**. La real es
  `@Patch(':id/status')` (`src/delivery/delivery.controller.ts:141`), con
  `@Roles(RoleType.ADMIN, RoleType.SUPER_ADMIN)` (línea 142) y body `{ isActive: boolean }` (línea 149).
- No invierte nada: `src/delivery/delivery.service.ts:237-242` hace
  `delivery.isActive = isActive` con el valor que llega en el body.
- **No hay llamada a Redis** en `toggleActiveStatus` (`src/delivery/delivery.service.ts:237-242`).
  El `removeDriver` solo se ejecuta en `toggleAvailability`
  (`src/delivery/delivery.service.ts:261-267`), que es el toggle del propio chofer (CU-022) y opera
  por `user_id`, no por `delivery_id`.
- No hay consulta de pedidos activos: la excepción documentada no existe.
- La misma ruta desprotegida señalada en CU-032 (`delivery.controller.ts:77-87`) permite a cualquier
  usuario autenticado cambiar `isActive` de cualquier chofer.

**Gravedad:** grave. Ruta inexistente, semántica de la operación invertida y el efecto operativo
central —sacarlo del radar— ausente. Un chofer "desactivado" por el administrador queda con
`isActive = false` en la base pero **sigue en el conjunto geoespacial de Redis**, y por lo tanto
sigue siendo candidato del despacho.

**Corrección propuesta**

> Paso 3: "La app envía `PATCH /delivery/:id/status` con el cuerpo `{ isActive: <booleano> }`."
> Paso 4: "El backend **asigna** a `Delivery.isActive` el valor recibido (no lo invierte)."
> Paso 5: "**⚠️ El backend no toca Redis en esta operación.** El chofer desactivado por el
> administrador permanece en el conjunto `drivers:locations` y sigue apareciendo como candidato de
> cercanía; la aceptación del pedido sí lo rechaza, porque `update-order-status.use-case.ts` verifica
> `isActive`. La eliminación del radar solo ocurre cuando el propio chofer se pone fuera de línea
> desde su app (CU-022)."
>
> Excepción paso 4: eliminar. El sistema no consulta los pedidos en curso del chofer antes de
> desactivarlo.

---

### CU-034 — Registrar Vehículo del Chofer · MENOR

**Qué dice la documentación**

> Paso 2: "Completa el formulario: `type`, `patent`, `brand`, `model`, `year`, `color`, `capacity`."
> Paso 3: "Confirma. La app envía `POST /cars` con el DTO completo."
> Excepción paso 4: "Si la patente ya existe → **409** 'La patente ya está registrada en el sistema.'"
> Excepción paso 4: "Si algún campo requerido está vacío → 400 con detalle del campo."

**Qué hace el código**

- La ruta es `POST /car` (`src/car/car.controller.ts:29,33`), en singular.
- La patente duplicada lanza `BadRequestException` → **400**, no 409, y el mensaje es
  `'La patente del vehículo ya está registrada'` (`src/car/car.service.ts:41-44`).
- Los nombres reales de los campos son `type_car`, `car_patent`, `car_brand`, `car_model`,
  `car_year`, `car_color`, `car_capacity`, y **todos son `@IsOptional()`**
  (`src/car/dto/create-car.dto.ts:16-54`). El único campo obligatorio es `user_id`
  (`src/car/dto/create-car.dto.ts:11-14`), que el CU no menciona en ningún paso.
- La distribuidora se toma del contexto con `{ required: true }`
  (`src/car/car.controller.ts:39`), lo que agrega una excepción 400 no documentada aquí (sí está
  documentada en CU-051).

**Gravedad:** menor. La operación existe y funciona; falla la especificación de la interfaz.

**Corrección propuesta**

> Paso 2: "Completa el formulario: `user_id` del chofer (obligatorio), y opcionalmente `type_car`,
> `car_patent`, `car_brand`, `car_model`, `car_year`, `car_color` y `car_capacity`."
> Paso 3: "Confirma. La app envía `POST /car` con el DTO."
> Excepción paso 4: "Si la patente ya existe → **400** 'La patente del vehículo ya está registrada.'"
> Excepción paso 4: "Si falta `user_id` o no es un UUID válido → 400. El resto de los campos son
> opcionales y su ausencia no produce error."
> Agregar: "Si el administrador no tiene distribuidora en contexto → 400 pidiendo el header
> `X-Distributor`."

---

### CU-035 — Consultar Listado de Choferes · GRAVE

**Qué dice la documentación**

> Paso 2: "El frontend ejecuta `GET /delivery?validated=&isActive=&page=`."
> Paso 3: "El backend retorna **paginado con join**: `{ id, fullName, email, phone, validated,
> isActive, calification, car: {...} }`."
> Paso 4: "El administrador puede filtrar por validado/no validado, activo/inactivo."
> Paso 5: "Cada chofer muestra: nombre, email, teléfono, estado, **vehículo asignado**, calificación
> promedio."

**Qué hace el código**

- `GET /delivery` (`src/delivery/delivery.controller.ts:41-50`) recibe `@Query() paginationDto: PaginationDto`.
  `src/common/dtos/pagination.dto.ts:4-28` declara únicamente `limit`, `offset`, `role`, `page` y
  `term`. **No existen `validated` ni `isActive`.**
- Por `forbidNonWhitelisted: true` (`src/main.ts:39-42`), la query exacta que documenta el paso 2
  (`?validated=&isActive=`) **devuelve 400**, no un listado filtrado.
- `page` está declarado en el DTO pero `src/delivery/delivery.service.ts:124` desestructura solo
  `{ limit = 10, offset = 0 }`: el parámetro `page` se acepta y se descarta.
- `src/delivery/delivery.service.ts:126-131` devuelve `deliveryRepository.find(...)` con
  `relations: ['user', 'user.role']`. **No hay relación con `Car`** — comparar con
  `src/car/car.service.ts:62`, que sí trae `['user', 'user.delivery']` en el sentido inverso.
- El retorno es un **array plano**, no un objeto paginado con total (comparar con
  `src/gascylinder/gascylinder.service.ts:89`, que sí devuelve `{ gasCylinders, total, limit, offset }`).
- El alcance por distribuidora sí se aplica (`src/delivery/delivery.service.ts:127`).

**Gravedad:** grave. Los pasos 2 a 5 —el cuerpo entero de la secuencia normal— no corresponden a
nada que el código haga, y el paso 2 tal como está escrito produce un error.

**Corrección propuesta**

> Paso 2: "El frontend ejecuta `GET /delivery?limit=&offset=`. **No existen parámetros de filtro por
> `validated` ni por `isActive`; enviarlos produce un 400** porque la validación global rechaza toda
> propiedad no declarada en el DTO de paginación."
> Paso 3: "El backend retorna un **array plano** (sin total ni metadatos de paginación) de perfiles
> `Delivery` con sus relaciones `user` y `user.role`, acotado a la distribuidora del administrador."
> Paso 4: "El filtrado por estado de validación o de actividad debe hacerse en el cliente sobre el
> listado recibido: el backend no lo ofrece."
> Paso 5: "Cada chofer muestra nombre, email, teléfono, estado y calificación promedio. **El vehículo
> asignado no viene en esta respuesta**: el panel debe consultarlo aparte con
> `GET /car/user/:userId` (CU-051)."

---

### CU-036 — Crear Producto (Garrafa) · MENOR

**Qué dice la documentación**

> Paso 2: "Completa el formulario: tipo, precio de venta, stock inicial y descripción opcional."
> Paso 3: "El sistema valida que tipo y precio son requeridos, que **precio > 0 y stock ≥ 0**."
> Excepción paso 3: "Si el precio es 0 o negativo → 'El precio debe ser mayor a cero.'"
> Excepción paso 3: "Si el stock es negativo → 'El stock no puede ser negativo.'"
> Excepción paso 4: "Si ya existe un producto **activo** con el mismo tipo → 'Ya existe un producto
> de ese tipo registrado.'"

**Qué hace el código**

- `src/gascylinder/dto/create-gascylinder.dto.ts:10-21` declara `weight` como **obligatorio**
  (`@IsNumber()`, sin `@IsOptional`), campo que el paso 2 no menciona. Omitirlo produce 400.
- `price` solo tiene `@IsNumber()` (línea 14-16) y `stock` solo `@IsOptional() @IsNumber()`
  (líneas 18-21): **no hay `@IsPositive()` ni `@Min(0)`**. Un precio `-500` o un stock `-3` se
  persisten sin error. Las dos excepciones documentadas no existen.
- El control de duplicado (`src/gascylinder/gascylinder.service.ts:52-60`) busca por
  `{ type, distributor_id }` **sin filtrar por `isActive`**: un producto dado de baja lógica
  (CU-040) sigue bloqueando el alta de un producto del mismo tipo. Dado que CU-040 declara que no
  existe camino de reactivación, ese nombre de tipo queda inutilizable de forma permanente.
- El mensaje real es `'Ya existe una garrafa con este tipo en tu distribuidora'` (línea 57-59).
- El paso 4 (`isActive = true`) sí se cumple, por el default de columna
  (`src/gascylinder/entities/gascylinder.entity.ts:44-45`).
- Actor y aislamiento correctos: `@Roles(ADMIN, SUPER_ADMIN)` y
  `@CurrentDistributor({ required: true })` (`src/gascylinder/gascylinder.controller.ts:29,37`).

**Gravedad:** menor.

**Corrección propuesta**

> Paso 2: "Completa el formulario: tipo, **peso en kg**, precio de venta, stock inicial y descripción
> opcional."
> Paso 3: "El sistema valida que tipo, peso y precio estén presentes y sean del tipo correcto.
> **⚠️ No valida el signo: un precio menor o igual a cero y un stock negativo se aceptan y se
> persisten.**"
> Excepciones del paso 3 sobre precio y stock: eliminar.
> Excepción paso 4: "Si ya existe un producto del mismo tipo en la distribuidora —**activo o dado de
> baja**— el sistema informa 'Ya existe una garrafa con este tipo en tu distribuidora.' Combinado con
> la ausencia de reactivación (CU-040), esto deja el nombre del tipo bloqueado de forma permanente."

---

### CU-037 — Actualizar Precio de Producto · MENOR

**Qué dice la documentación**

> Paso 3: "El sistema valida que el nuevo precio es un número **mayor a cero**."
> Excepción paso 3: "Si el precio ingresado es 0, negativo o no es un número válido, el sistema
> informa el error específico."

**Qué hace el código**

- `src/gascylinder/dto/update-gascylinder.dto.ts:7` — `UpdateGasCylinderDto extends PartialType(CreateGasCylinderDto)`,
  y `price` en el DTO base solo lleva `@IsNumber()` (`src/gascylinder/dto/create-gascylinder.dto.ts:14-16`).
  Un `PATCH` con `price: 0` o `price: -1` se acepta y se guarda
  (`src/gascylinder/gascylinder.service.ts:132-141`).
- El resto del CU es fiel: la ruta existe (`src/gascylinder/gascylinder.controller.ts:81-99`), el
  404 se produce por la verificación de pertenencia previa
  (`src/gascylinder/gascylinder.service.ts:130`), y el aislamiento por distribuidora se aplica.
- La afirmación de Comentarios sobre el snapshot de precio en `OrderItem.unitPrice` es correcta.

**Gravedad:** menor.

**Corrección propuesta**

> Paso 3: "El sistema valida que el nuevo precio sea un número. **⚠️ No valida que sea mayor a cero:
> un precio de 0 o negativo se acepta y queda vigente en el catálogo.**"
> Excepción paso 3: "Si el precio no es un número válido → 400. Un precio 0 o negativo **no** produce
> error."

---

### CU-038 — Actualizar Stock de Producto · GRAVE

**Qué dice la documentación**

> Paso 2: "Edita el campo 'Stock' ingresando el **nuevo valor total (no el incremento, sino el valor
> absoluto resultante)**."
> Paso 4: "El sistema actualiza `GasCylinder.stock` **con el nuevo valor**."
> Postcondición: "`GasCylinder.stock` fue actualizado **al valor indicado**."
> Excepción paso 3: "Si el valor ingresado es negativo, el sistema informa 'El stock no puede ser
> negativo.'"
> Excepción paso 3: "Si el valor no es un número entero, el sistema informa error de formato."

**Qué hace el código**

- `src/gascylinder/gascylinder.service.ts:144-153`:

  ```ts
  async updateStock(id: string, quantity: number, distributorId: string) {
    const gasCylinder = await this.findOne(id, distributorId);
    gasCylinder.stock += quantity;          // ← línea 146: SUMA, no asigna
    if (gasCylinder.stock < 0) {
      throw new BadRequestException('Stock cannot be negative');
    }
    ...
  ```

  El valor recibido es un **delta**, exactamente lo contrario de lo que dice el paso 2. Un
  administrador que sigue la documentación al pie de la letra y envía `120` sobre un stock de `80`
  deja el producto en `200`, no en `120`.
- El body no tiene DTO: `@Body() body: { quantity: number }`
  (`src/gascylinder/gascylinder.controller.ts:108`). Al no ser una clase, el `ValidationPipe` no
  interviene: **no se valida que sea entero ni numérico**. La excepción de formato documentada no
  existe.
- La validación de negativo existe pero se aplica **al resultado de la suma**
  (línea 148), no al valor ingresado, y el mensaje es `'Stock cannot be negative'`, en inglés.
- Actor y aislamiento correctos (`src/gascylinder/gascylinder.controller.ts:102,109`).

**Gravedad:** grave. Es la discrepancia con mayor potencial de daño operativo del bloque: la
documentación instruye a hacer exactamente lo que corrompe el inventario, y el propio texto se
detiene a aclarar —incorrectamente— que **no** es un incremento.

**Corrección propuesta**

> Paso 2: "Ingresa el **ajuste** de stock: la cantidad a sumar al stock actual. Un valor negativo
> descuenta. **No es el valor absoluto resultante.**"
> Paso 4: "El sistema **suma** el valor recibido a `GasCylinder.stock` y verifica que el resultado no
> quede por debajo de cero."
> Postcondición: "`GasCylinder.stock` quedó incrementado (o decrementado) en la cantidad indicada."
> Excepción paso 3: "Si el ajuste dejaría el stock resultante por debajo de cero → 400
> 'Stock cannot be negative'. **El valor ingresado en sí no se valida: el cuerpo se recibe como
> objeto plano sin DTO, de modo que un valor no numérico o no entero no es rechazado por el
> backend.**"

---

### CU-039 — Configurar Promociones por Cantidad · GRAVE

**Qué dice la documentación**

> Paso 3: "Confirma. La app envía `PATCH /gas-cylinders/:id` con el array `promotions`."
> Paso 4: "El backend valida que cada regla tenga `quantity > 0` y `0 < discountPercentage <= 50`."
> Excepción paso 4: "Si `discountPercentage > 50` → 400 'El descuento máximo permitido es 50%.'"
> Excepción paso 4: "Si `quantity <= 0` → 400 'La cantidad mínima debe ser mayor a cero.'"

**Qué hace el código**

- La ruta `PATCH /gas-cylinders/:id` **no existe**. El controlador es
  `@Controller('gascylinder')` (`src/gascylinder/gascylinder.controller.ts:24`), sin guion y en
  singular: la ruta real es `PATCH /api/gascylinder/:id`.
- `src/gascylinder/dto/update-gascylinder.dto.ts:13-15` declara `promotions` con
  `@IsOptional() @IsArray()` y **nada más**. No hay `@ValidateNested`, ni `@Type`, ni una clase de
  regla de promoción: el contenido del array no se valida en absoluto. El paso 4 completo es
  inventado, y con él las dos excepciones.
- Consecuencia real: `PATCH /api/gascylinder/:id { "promotions": [{ "quantity": 0, "discountPercentage": 200 }] }`
  se persiste. El motor de precios lo consume sin control adicional
  (`src/order/domain/order-pricing.service.ts:40-48`, que hace
  `new Decimal(promo.discountPercentage).dividedBy(100)`), de modo que un descuento de 200 % produce
  un subtotal negativo.
- Actor y aislamiento correctos (`src/gascylinder/gascylinder.controller.ts:82,92`).

**Gravedad:** grave. El paso 4 no es un detalle de forma: es la única salvaguarda declarada sobre un
valor que se aplica directamente al precio cobrado, y no existe.

**Corrección propuesta**

> Paso 3: "Confirma. La app envía `PATCH /gascylinder/:id` con el array `promotions`."
> Paso 4: "El backend valida únicamente que `promotions` **sea un array**. **⚠️ No valida el
> contenido de cada regla**: ni `quantity`, ni `discountPercentage`, ni sus signos ni sus topes. Un
> descuento mayor a 100 se persiste y el motor de precios lo aplica tal cual, produciendo un subtotal
> negativo."
> Excepciones del paso 4: eliminar ambas, y agregar a Comentarios: "Acotar `discountPercentage` a
> `(0, 50]` y `quantity` a valores positivos, con `@ValidateNested` sobre una clase de regla, queda
> registrado como pendiente de implementación."

---

### CU-040 — Activar / Desactivar Producto · MENOR (residual)

El aviso de "implementado parcialmente" ya presente en el documento es correcto en su fondo. Queda
un residuo de forma no cubierto por ese aviso:

**Qué dice la documentación**

> Paso 3: "La app envía `PATCH /gas-cylinders/:id/toggle-active`."
> Paso 4: "El backend **invierte** `GasCylinder.isActive`."

**Qué hace el código**

- No existe ninguna ruta `toggle-active` en `src/gascylinder/gascylinder.controller.ts` (las rutas
  son `POST /`, `GET /`, `GET /:id`, `GET /type/:type`, `GET /available/list`, `PATCH /:id`,
  `PATCH /:id/stock`, `DELETE /:id`). La desactivación se ejecuta con
  `DELETE /gascylinder/:id` (`src/gascylinder/gascylinder.controller.ts:114-127`), que llama a
  `remove` y hace `gasCylinder.isActive = false` (`src/gascylinder/gascylinder.service.ts:155-165`).
- No invierte: **siempre** asigna `false`. Es lo que sostiene la observación de que no hay
  reactivación.

**Gravedad:** menor (residual sobre un hallazgo ya declarado).

**Corrección propuesta**

> Paso 3: "La app envía `DELETE /gascylinder/:id`."
> Paso 4: "El backend **asigna** `GasCylinder.isActive = false` (nunca `true`) y persiste el cambio."

---

### CU-041 — Consultar Catálogo de Productos · GRAVE

**Qué dice la documentación**

> Precondición: "El usuario está **autenticado** con rol CLIENTE o ADMIN."
> Secuencia — Cliente, paso 2: "El sistema consulta todos los registros `GasCylinder` donde
> `isActive = true` **y `stock > 0`**."
> Secuencia — **Administrador**, paso 2: "El sistema retorna **todos los productos sin filtro de
> estado ni de stock**."
> Secuencia — Administrador, paso 3: "Cada producto muestra: tipo, precio actual, stock actual y
> **estado activo/inactivo**."

**Qué hace el código**

- `GET /gascylinder` está marcado `@Public()` (`src/gascylinder/gascylinder.controller.ts:42-48`), lo
  mismo que `GET /gascylinder/available/list` (línea 73-79). **No hay precondición de autenticación
  ni de rol**: cualquiera con la URL lee el catálogo.
- `src/gascylinder/gascylinder.service.ts:77` — `const where: FindOptionsWhere<GasCylinder> = { isActive: true };`
  El listado **siempre** filtra por producto activo. **No existe ningún endpoint que devuelva el
  catálogo completo con inactivos**: la vista de administrador descrita en la secuencia
  correspondiente no está implementada.
- El filtro `stock > 0` que la secuencia del cliente atribuye a este listado está en un endpoint
  distinto, `getAvailableCylinders` (`src/gascylinder/gascylinder.service.ts:167-187`, `MoreThan(0)`
  en línea 171). `findAll` no filtra por stock.
- Consecuencia práctica: el panel de administración no puede ver ni recuperar un producto dado de
  baja, lo que cierra el círculo con la limitación ya declarada en CU-040.
- El único acceso a un producto inactivo es `GET /gascylinder/:id`
  (`src/gascylinder/gascylinder.service.ts:97-108`, sin filtro de `isActive`), es decir, conociendo
  el UUID de antemano.

**Gravedad:** grave. Una de las dos secuencias normales del CU no tiene respaldo en el código, y la
precondición de autenticación es falsa.

**Corrección propuesta**

> Precondición: "**Ninguna.** El listado del catálogo es un endpoint público: no requiere token ni
> rol. La distribuidora se selecciona con el parámetro `?distributor=<slug|uuid>`; si se omite, el
> sistema cae en la distribuidora por defecto."
> Secuencia — Cliente, paso 2: "La app consulta `GET /gascylinder/available/list`, que devuelve los
> registros con `isActive = true` **y `stock > 0`** de esa distribuidora. (El listado paginado
> `GET /gascylinder` filtra solo por `isActive` y **no** por stock.)"
> Secuencia — Administrador: reemplazar por: "**⚠️ No implementado.** No existe endpoint que devuelva
> el catálogo completo: `GET /gascylinder` filtra siempre `isActive = true`, de modo que el panel de
> administración no puede listar productos dados de baja. El único acceso a un producto inactivo es
> `GET /gascylinder/:id` conociendo su identificador. Queda registrado como pendiente de
> implementación junto con la reactivación de CU-040."

---

### CU-042 — Crear Franja Horaria · GRAVE

**Qué dice la documentación**

> Paso 2: "Completa: `name`, `startTime`, `endTime`, `capacity`."
> Paso 3: "Confirma. La app envía `POST /time-slots` con el DTO."
> Paso 4: "El backend valida que **`endTime > startTime`** y **`capacity > 0`**."
> Excepción paso 4: "Si `endTime <= startTime` → 400 'La hora de fin debe ser posterior a la de
> inicio.'"
> Excepción paso 4: "Si `capacity <= 0` → 400 'La capacidad debe ser mayor a cero.'"

**Qué hace el código**

- La ruta es `POST /time-slot` (`src/time-slot/time-slot.controller.ts:11,15`), en singular.
- `src/time-slot/time-slot.service.ts:50-56` — `create` construye la entidad y la guarda. **No hay
  ninguna validación**: ni de orden de horas, ni de capacidad.
- `src/time-slot/dto/create-time-slot.dto.ts:10-22` valida el **formato** `HH:MM` de `startTime` y
  `endTime` con `@Matches`, pero jamás compara uno con otro. `"18:00"` a `"09:00"` se acepta.
- `src/time-slot/dto/create-time-slot.dto.ts:24-27` — `capacity` es `@IsInt() @IsOptional()`, sin
  `@IsPositive()` ni `@Min()`. Además es **opcional**: si se omite, la columna toma el default 50
  (`src/time-slot/entities/time-slot.entity.ts:36-37`). `capacity: 0` o `capacity: -5` se persisten,
  y una franja con capacidad negativa nunca queda disponible en CU-045 sin que nadie sepa por qué.
- El paso 5 (`isActive = true`) sí se cumple por el default de columna
  (`src/time-slot/entities/time-slot.entity.ts:39-40`).
- Actor y aislamiento correctos (`src/time-slot/time-slot.controller.ts:16,20`).

**Gravedad:** grave. El paso 4 entero y sus dos excepciones son inventados; son las únicas reglas de
integridad declaradas para una entidad que gobierna la capacidad diaria de entrega.

**Corrección propuesta**

> Paso 2: "Completa: `name`, `startTime`, `endTime` y, opcionalmente, `capacity` (si se omite, la
> franja toma la capacidad por defecto de 50 pedidos diarios)."
> Paso 3: "Confirma. La app envía `POST /time-slot` con el DTO."
> Paso 4: "El backend valida el **formato** `HH:MM` de ambas horas y que `capacity`, si viene, sea un
> entero. **⚠️ No valida que `endTime` sea posterior a `startTime` ni que `capacity` sea mayor a
> cero**: una franja invertida o con capacidad 0 o negativa se persiste sin error y queda
> permanentemente sin cupo."
> Excepciones del paso 4: reemplazar por: "Si alguna hora no respeta el formato `HH:MM` → 400. Si
> `capacity` no es un entero → 400."

---

### CU-044 — Seleccionar Franja Horaria al Crear Pedido · MENOR

**Qué dice la documentación**

> Descripción: "Durante el checkout, el cliente **debe** elegir una franja horaria de entrega
> disponible para la fecha solicitada."
> Excepción paso 6: "Si entre el paso 4 y 6 la franja se llenó (race condition) → **409** 'Franja sin
> capacidad disponible. Volvé a elegir.'"

**Qué hace el código**

- `src/order/dto/create-order.dto.ts:67-70` — `timeSlotId` es `@IsOptional() @IsUUID()`. La franja
  **no es obligatoria**: omitir `timeSlotId` y `scheduledDate` produce un pedido de entrega
  inmediata, como el propio DTO documenta en su descripción (líneas 73-81).
- El control de capacidad bajo concurrencia sí existe y es correcto:
  `src/time-slot/time-slot.service.ts:194-229` (`assertSlotAvailableTx`) toma la fila de la franja
  con `lock: { mode: 'pessimistic_write' }` (línea 206) dentro de la transacción que inserta el
  pedido, y cuenta los pedidos no cancelados con el mismo `EntityManager` (línea 223).
- Pero el error que emite es `BadRequestException` → **400**, con el mensaje
  `` `La franja "${slot.name}" del ${date} está completa` `` (líneas 224-228). No es 409 ni ese texto.

**Gravedad:** menor. El mecanismo existe y es sólido; falla la obligatoriedad declarada y el código
HTTP.

**Corrección propuesta**

> Descripción: "Durante el checkout, el cliente **puede** elegir una fecha y una franja horaria de
> entrega. Omitir ambas produce un pedido de entrega inmediata; elegirlas agenda el pedido y valida
> el cupo de esa franja para ese día."
> Excepción paso 6: "Si entre el paso 4 y el 6 la franja se llenó → **400** 'La franja "<nombre>" del
> <fecha> está completa'. La carrera está resuelta con un bloqueo pesimista sobre la fila de la
> franja dentro de la misma transacción que inserta el pedido."

---

### CU-045 — Consultar Franjas Horarias Disponibles · GRAVE

**Qué dice la documentación**

> Precondición: "El cliente está **autenticado** y consulta una fecha de entrega válida (≥ hoy)."
> Paso 2: "La app envía `GET /time-slots/availability?date=YYYY-MM-DD`."
> Paso 5: "Calcula `availableSlots = capacity − ordersCount`."
> Paso 6: "Retorna `[{ id, name, startTime, endTime, capacity, **availableSlots** }]`."
> Excepción paso 2: "Si la fecha es anterior a hoy → **400** 'La fecha debe ser igual o posterior a
> hoy.'"

**Qué hace el código**

- El endpoint es `GET /time-slot/availability` y está marcado **`@Public()`**
  (`src/time-slot/time-slot.controller.ts:39-40`): no hay autenticación ni rol. La precondición es
  falsa. Al ser público, el tenant no puede venir del token: llega por `?distributor=slug|uuid`
  (línea 51), dato que el paso 2 omite.
- `src/time-slot/time-slot.service.ts:117-148` — `getAvailability` **no valida la fecha en absoluto**.
  No hay comparación contra hoy: la excepción documentada no existe en este camino. Consultar una
  fecha pasada devuelve 200 con las franjas y su conteo histórico. (La validación de fecha pasada sí
  existe, pero recién al **crear** el pedido: `src/time-slot/time-slot.service.ts:172-175` y
  `212-215`.) Tampoco se valida el formato de `date`, que llega como `@Query('date') date: string`
  sin DTO (`src/time-slot/time-slot.controller.ts:50`).
- Los nombres de los campos de la respuesta son otros
  (`src/time-slot/time-slot.service.ts:137-145` e interfaz `SlotAvailability`, líneas 17-25):
  `{ timeSlotId, name, startTime, endTime, capacity, booked, remaining }`. No hay `id` ni
  `availableSlots`; hay además un campo `booked` que el CU no menciona.
- El resto es fiel: se filtra `isActive: true` (línea 122), se acota por distribuidora (línea 123) y
  se cuentan los pedidos no cancelados de esa fecha y franja
  (`src/time-slot/time-slot.service.ts:98-110`, `status: Not(OrderStatus.CANCELLED)`).

**Gravedad:** grave. Actor equivocado (endpoint público), una excepción inventada y un contrato de
respuesta que un frontend escrito contra la documentación no podría consumir.

**Corrección propuesta**

> Precondición: "**Ninguna: el endpoint es público.** La distribuidora se indica con
> `?distributor=<slug|uuid>`."
> Paso 2: "La app envía `GET /time-slot/availability?date=YYYY-MM-DD&distributor=<slug>`."
> Paso 5: "Calcula `remaining = max(0, capacity − booked)`."
> Paso 6: "Retorna `[{ timeSlotId, name, startTime, endTime, capacity, booked, remaining }]`."
> Paso 7: "El frontend muestra solo las franjas con `remaining > 0`."
> Excepción paso 2: reemplazar por: "**⚠️ La consulta no valida la fecha**: ni el formato ni que sea
> igual o posterior a hoy. Una fecha pasada devuelve 200 con el conteo histórico. El rechazo de
> fechas pasadas ocurre recién al crear el pedido (CU-005/CU-044), con el mensaje 'No se puede
> agendar en una fecha pasada'."

---

### CU-046 — Gestionar Direcciones de Entrega · MENOR

Los once pasos de la secuencia y las seis excepciones se verificaron uno a uno y **coinciden** con
`src/user-addres/user-addres.controller.ts` y `src/user-addres/user-addres.service.ts`: el alcance
por rol (`scope()`, controlador líneas 28-32), la reescritura del `user_id` (servicio líneas 48-53),
el desmarcado de predeterminadas (líneas 192-212), la promoción de la más reciente al borrar
(líneas 161-174), el fallback a la primera dirección (líneas 123-129), el 403 con el texto exacto
(líneas 36-38) y el 404 `No addresses found for user` (línea 128). El `GET /user-address` global
está efectivamente reservado a `@Roles(SUPER_ADMIN)` (controlador línea 50). Los Comentarios sobre
la baja física y el desmarcado fuera de transacción son correctos.

Queda un solo punto:

**Qué dice la documentación**

> Postcondición: "Como máximo una dirección del usuario queda marcada como predeterminada, y **si el
> usuario conserva al menos una dirección, siempre hay una predeterminada**."

**Qué hace el código**

- `src/user-addres/user-addres.service.ts:65-70` — el desmarcado y la marca solo ocurren
  `if (createUserAddressDto.isDefault)`. Un usuario que crea todas sus direcciones sin ese flag
  **no tiene ninguna predeterminada**. El invariante solo se sostiene por el camino de borrado
  (líneas 161-174) y por `setAsDefault` (líneas 184-190).
- Lo que sí es cierto es el fallback de lectura: `findDefaultByUserId` devuelve la primera del
  listado ordenado si ninguna está marcada (líneas 123-129) — eso es el paso 11, no la postcondición.

**Gravedad:** menor.

**Corrección propuesta**

> Postcondición: "La libreta refleja el alta, la modificación o la baja realizada. Como máximo una
> dirección del usuario queda marcada como predeterminada. **El sistema no garantiza que siempre haya
> una: si el cliente nunca marcó ninguna, ninguna queda marcada.** Lo que sí garantiza es la lectura:
> la consulta de dirección predeterminada devuelve la más reciente cuando ninguna está marcada."

---

### CU-053 — Consultar Distribuidoras · MENOR

**Qué dice la documentación**

> Descripción: "El sistema lista todas las distribuidoras o devuelve una en base a su ID **o slug**,
> ordenadas por fecha de creación."

**Qué hace el código**

- `src/distributor/distributor.controller.ts` expone exactamente cuatro rutas de lectura/escritura:
  `POST /` (36), `GET /` (44), `GET /:id` (50), `PATCH /:id` (57), `DELETE /:id` (67). **No hay
  ninguna ruta de consulta por slug.**
- `findBySlug` existe en el servicio (`src/distributor/distributor.service.ts:47-53`) pero solo la
  consumen internamente los resolvedores de tenant de catálogo y franjas
  (`src/gascylinder/gascylinder.service.ts:42`, `src/time-slot/time-slot.service.ts:46`). No es
  alcanzable como operación del administrador general.
- Lo demás es fiel: `@Roles(SUPER_ADMIN)` a nivel de clase (línea 31), orden `createdAt: 'ASC'`
  (`src/distributor/distributor.service.ts:34`) y 404 con mensaje propio (líneas 41-43).

**Gravedad:** menor.

**Corrección propuesta**

> Descripción: "El sistema lista todas las distribuidoras ordenadas por fecha de creación ascendente,
> o devuelve una en base a su **ID**. **La búsqueda por slug existe internamente —la usan los
> endpoints públicos de catálogo y franjas para resolver el tenant del parámetro `?distributor=`—
> pero no está expuesta como endpoint del administrador general.**"

---

### CU-060 — Registrar Incidencia de Entrega · GRAVE

**Qué dice la documentación**

> Paso 2: "El sistema obtiene la ID del usuario **y distribuidora** desde contexto."
> Paso 3: "El sistema verifica la existencia del pedido (**y que incumba a la organizacion**)."

**Qué hace el código**

- `src/incident/incident.controller.ts:39-44` — el handler inyecta **solo** `@CurrentUser()`. A
  diferencia de sus hermanos del mismo controlador (`findAll` línea 49, `findByOrder` línea 59,
  `resolve` línea 72), el `create` **no inyecta `@CurrentDistributor()`**: no hay distribuidora de
  contexto en esta operación.
- `src/incident/incident.service.ts:27-32`:

  ```ts
  const order = await this.orderRepository.findOne({
    where: { order_id: dto.orderId },      // ← línea 28: sin distributor_id
  });
  if (!order) { throw new NotFoundException('Pedido no encontrado'); }
  ```

  La búsqueda del pedido **no filtra por distribuidora**. La verificación de pertenencia al tenant
  que promete el paso 3 no existe.
- `src/incident/incident.service.ts:36` — `distributor_id: order.distributor_id`: el tenant se
  denormaliza **del pedido**, no del contexto del solicitante. Combinado con lo anterior, un chofer o
  un administrador de la distribuidora A que conozca el UUID de un pedido de la distribuidora B puede
  crear una incidencia sobre ese pedido, y la incidencia queda registrada **bajo la distribuidora B**,
  donde su administrador la verá en `GET /incidents` como si fuera propia.
- El resto es fiel: actor `@Roles(DELIVERY, ADMIN, SUPER_ADMIN)` (línea 33), 400 por DTO
  (`src/incident/dto/create-incident.dto.ts:6-17`), 404 (`incident.service.ts:31`) y 201 por defecto.
  Los demás endpoints del módulo **sí** aplican el filtro por tenant
  (`src/incident/incident.service.ts:50`, `70`, `84`).

**Gravedad:** grave. Es un CU que promete aislamiento multi-tenant explícitamente y el código no lo
aplica, en el único endpoint de escritura del módulo y contra el patrón que el propio módulo sigue en
todas sus demás operaciones.

**Corrección propuesta**

> Paso 2: "El sistema obtiene la ID del usuario desde el token. **La distribuidora no se toma del
> contexto de la petición: se denormaliza del pedido referenciado.**"
> Paso 3: "El sistema verifica **únicamente la existencia** del pedido. **⚠️ No verifica que el pedido
> pertenezca a la distribuidora del solicitante**: quien conozca el identificador de un pedido de otra
> distribuidora puede registrar una incidencia sobre él, y la incidencia queda asentada bajo esa otra
> distribuidora. Corregirlo requiere inyectar `@CurrentDistributor()` en el handler y acotar la
> búsqueda del pedido a ese tenant, como ya hacen el listado, la consulta por pedido y la resolución
> de incidencias."

---

## Casos de uso sin respaldo en el código

Se listan aquí los elementos documentados que **no tienen absolutamente ninguna contraparte** en el
código, distinguidos de los que existen pero difieren.

**Casos de uso completos:**

- **CU-043 — Modificar Capacidad de Franja Horaria.** Confirmado: `src/time-slot/time-slot.controller.ts`
  contiene `@Post` (15), `@Get` (25), `@Get('availability')` (39), `@Get(':id')` (56) y `@Delete(':id')`
  (65). **No existe ningún `@Patch` ni `@Put`.** El aviso ya presente en el documento es correcto.

**Secuencias normales completas sin implementación:**

- **CU-041, secuencia "Actor: Administrador".** Sus cuatro pasos describen un catálogo completo con
  productos inactivos y stock 0 que ningún endpoint devuelve: `src/gascylinder/gascylinder.service.ts:77`
  fuerza `isActive: true` en el único listado existente.

**Pasos y excepciones inventados (no existe la línea de código correspondiente):**

| Ubicación | Elemento documentado | Estado en el código |
|-----------|----------------------|---------------------|
| CU-032 paso 4 | `ZREM drivers:locations` al invalidar | `invalidateDelivery` no toca Redis (`delivery.service.ts:213-218`) |
| CU-032 excepción paso 3 | 400 por entrega en curso | No hay consulta de pedidos (`delivery.service.ts:206-218`) |
| CU-033 paso 5 | `RedisService.zRem` al desactivar | `toggleActiveStatus` no toca Redis (`delivery.service.ts:237-242`) |
| CU-033 excepción paso 4 | 400 por entrega en curso | No hay consulta de pedidos |
| CU-035 pasos 2 y 4 | Filtros `?validated=&isActive=` | No están en `PaginationDto`; producen 400 (`main.ts:39-42`) |
| CU-035 pasos 3 y 5 | Join con el vehículo | `relations: ['user','user.role']` (`delivery.service.ts:130`) |
| CU-036 excepciones paso 3 | Precio > 0, stock ≥ 0 | Sin `@IsPositive`/`@Min` (`create-gascylinder.dto.ts:14-21`) |
| CU-037 paso 3 | Precio > 0 | Ídem, vía `PartialType` (`update-gascylinder.dto.ts:7`) |
| CU-038 excepción "no es entero" | Error de formato | Body sin DTO (`gascylinder.controller.ts:108`) |
| CU-039 paso 4 y excepciones | `quantity > 0`, `discount ≤ 50` | Solo `@IsArray()` (`update-gascylinder.dto.ts:13-15`) |
| CU-042 paso 4 y excepciones | `endTime > startTime`, `capacity > 0` | `create` no valida nada (`time-slot.service.ts:50-56`) |
| CU-045 excepción paso 2 | 400 por fecha pasada | `getAvailability` no valida fecha (`time-slot.service.ts:117-148`) |
| CU-060 paso 3 (parcial) | Pertenencia del pedido al tenant | `findOne` sin `distributor_id` (`incident.service.ts:27-29`) |

**Rutas documentadas que no existen:**

| Documentada | Real |
|-------------|------|
| `PATCH /delivery/:id/toggle-active` (CU-033) | `PATCH /api/delivery/:id/status` |
| `POST /cars` (CU-034) | `POST /api/car` |
| `PATCH /gas-cylinders/:id` (CU-039) | `PATCH /api/gascylinder/:id` |
| `PATCH /gas-cylinders/:id/toggle-active` (CU-040) | `DELETE /api/gascylinder/:id` |
| `POST /time-slots` (CU-042) | `POST /api/time-slot` |
| `PATCH /time-slots/:id` (CU-043) | *no existe* |
| `GET /time-slots/availability` (CU-045) | `GET /api/time-slot/availability` |
| Consulta de distribuidora por slug (CU-053) | *no expuesta* |

**Hallazgo transversal de autorización (afecta a CU-031, CU-032, CU-033 y CU-049):**

`src/delivery/delivery.controller.ts:77-87` expone `@Patch(':id')` **sin `@Roles`**, con
`UpdateDeliveryDto = PartialType(CreateDeliveryDto)` (`src/delivery/dto/update-delivery.dto.ts:4`),
que incluye `validated`, `isActive`, `calification` y `distributorId`. Por
`src/common/guards/roles.guard.ts:40-42`, cualquier usuario autenticado puede escribir esos campos en
cualquier perfil de chofer, incluida la reasignación de distribuidora —que rompe el aislamiento
multi-tenant en el que se apoyan CU-035, CU-051 y todo el subsistema SS-10—. Los tres CU que
declaran al administrador como único actor de esas operaciones son, por esta ruta, inexactos.
Igual observación, de menor alcance, para `@Get('active')` (línea 52) y `@Patch(':id/location')`
(línea 112), también sin `@Roles`.
