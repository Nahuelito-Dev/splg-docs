# Convenciones del backend

Cómo se escribe código en este backend. La vara son las convenciones oficiales
de **NestJS** y el modo estricto de **TypeScript**, sin excepciones propias. Si
algo de acá contradice a la documentación de Nest, manda Nest y se corrige este
documento.

Un módulo se da por **alineado** cuando cumple la lista de la sección 12. Hasta
entonces, lo que diga este documento es el destino y no la descripción del
código.

---

## 1. TypeScript

- `strict: true` y `noFallthroughCasesInSwitch: true`. El proyecto compila sin
  errores con `npx tsc --noEmit`.
- **Prohibido `any`**, explícito o implícito. Lo que no se conoce es `unknown` y
  se estrecha con guardas de tipo antes de usarlo.
- En un `catch` llega `unknown`. El mensaje y el status se leen con
  `errorMessage()` y `errorStatus()` de `common/errors/error-message.ts`.
- `!` (asignación definida) sólo en propiedades que llena un framework: DTOs que
  arma `class-validator`, entidades que arma TypeORM, `@WebSocketServer()`, y
  lo que se asigna en `onModuleInit`. En cualquier otro lado es un error de
  diseño.
- Una columna `nullable: true` se tipa `T | null`, nunca `T`. Y **declara el
  `type`** en `@Column`: con una unión, el metadato que emite TypeScript es
  `Object` y TypeORM no puede inferir el tipo de la columna.
- Las conversiones (`as`) se justifican. `as unknown as T` sólo en tests.

## 2. Nombres

| Qué                         | Convención                            | Ejemplo                                           |
| --------------------------- | ------------------------------------- | ------------------------------------------------- |
| Carpeta de módulo           | kebab-case, singular                  | `user-address/`                                   |
| Archivo                     | `<nombre>.<tipo>.ts`, kebab-case      | `create-order.dto.ts`, `is-public.decorator.ts`   |
| Clase                       | PascalCase con el sufijo de su tipo   | `OrderController`, `CreateOrderDto`, `RolesGuard` |
| Propiedad, método, variable | camelCase                             | `deliveryId`, `findByUser()`                      |
| Constante de módulo         | UPPER_SNAKE_CASE                      | `CACHE_TTL_SEC`                                   |
| Enum                        | PascalCase, miembros UPPER_SNAKE_CASE | `OrderStatus.ON_THE_WAY`                          |

**La base y el JSON no se renombran para cumplir esto.** La propiedad de la
entidad va en camelCase y la columna conserva su nombre con
`@Column({ name: 'user_id' })`: la tabla no cambia y no hace falta migración.
Las claves del JSON las fija el DTO de salida (sección 7), no la entidad.

- **Endpoints existentes:** el DTO de salida conserva las claves de hoy, para no
  romper el panel ni las apps.
- **Endpoints nuevos:** claves en camelCase.
- El cambio de las claves existentes a camelCase, si se hace, va en `/v2`.

## 3. Estructura de un módulo

Dos plantillas, según lo que hace el módulo. Hexagonalizar un ABM es costo sin
beneficio; dejar plano un módulo con reglas y concurrencia las esconde.

### Módulo de soporte (ABM con reglas simples)

```
car/
├── car.module.ts
├── car.controller.ts
├── car.service.ts
├── car.service.spec.ts
├── car.mapper.ts
├── dto/
│   ├── create-car.dto.ts
│   ├── update-car.dto.ts
│   ├── query-car.dto.ts          (si el listado filtra)
│   └── car-response.dto.ts
└── entities/
    └── car.entity.ts
```

Son de soporte: `role`, `admin`, `customer`, `car`, `claims`, `incident`,
`rating`, `time-slot`, `coverage-zone`, `distributor`, `user-address`,
`reports`, `notifications`, `email`.

### Módulo núcleo (reglas de negocio, estados, concurrencia)

```
order/
├── order.module.ts
├── domain/            reglas puras: máquinas de estado, errores de dominio, puertos
├── application/       un caso de uso por archivo: create-order.use-case.ts
├── infrastructure/    adaptadores de los puertos (repositorios, gateways externos)
├── presentation/      controladores, DTOs y mappers
└── entities/
```

`domain/` no importa nada de `@nestjs/*` ni de TypeORM. Lanza errores de dominio
(`BadRequestDomainError`, `NotFoundDomainError`) y el `GlobalExceptionFilter`
los traduce a HTTP.

Son núcleo: `order` (pedidos y despacho), `payments`, `cylinder` (inventario de
envases), y los módulos inteligentes cuando existan.

Los módulos de infraestructura (`auth`, `users`, `delivery`, `gateways`,
`firebase`, `redis`, `health`) siguen la plantilla de soporte salvo que tengan
un puerto que justifique otra cosa.

## 4. Encapsulamiento entre módulos

- **Cada módulo es dueño de sus entidades.** `TypeOrmModule.forFeature([...])`
  lista sólo las del propio módulo.
- Para leer o escribir lo de otro módulo se usa **el servicio que ese módulo
  exporta**. Si el método no existe, se agrega en el módulo dueño.
- **Excepción: los modelos de lectura.** Un módulo que sólo lee y agrega datos
  de varios contextos para mostrarlos (`reports`) puede registrar entidades
  ajenas, **sólo para consultar**: nunca guarda, modifica ni borra. Es el lado
  de lectura de CQRS; forzarlo a pasar por los servicios de cada contexto
  agrega capas sin proteger nada.
- **Excepción: la pertenencia a una distribuidora.** Qué usuarios son de una
  distribuidora (sus choferes, sus admins y los clientes que le compraron) se
  define **una sola vez**, en `common/tenancy/pertenencia.ts`, con subconsultas
  de sólo lectura sobre `order`, `delivery` y `admin`. La usan todos los
  módulos que acotan por distribuidora; ninguno la reescribe.
- **Aislamiento entre distribuidoras.** Con distribuidora en contexto
  (`@CurrentDistributor()`: la del admin de empresa, o la que eligió el super
  admin con "ver como"), todo se acota a ella. Lo de otra responde **404**, no
  403: no se revela que existe. Los clientes se comparten entre distribuidoras:
  cada una los ve, pero su cuenta la administra el administrador general.
- **Sin `forwardRef`.** Una dependencia circular es un problema de diseño: se
  resuelve extrayendo lo compartido, invirtiendo la dependencia con un puerto, o
  con un evento.
- Lo que un módulo tiene que _enterarse_ pero no _contestar_ (auditoría,
  historial de estados, notificaciones) va por **eventos de dominio**
  (`@nestjs/event-emitter`), no por llamadas directas.

## 5. Controladores

- **Delgados.** Reciben, validan con el DTO, llaman al servicio o al caso de
  uso y devuelven un DTO de salida. Sin lógica de negocio, sin repositorios, sin
  `try/catch`.
- La **autorización que depende de quién pide** (su rol, su distribuidora: "un
  admin de empresa no crea super admins") puede resolverse en el controlador,
  que es donde está `@CurrentUser()`. Las **invariantes del negocio** van al
  servicio.
- **Todo parámetro con su pipe:** `@Param('id', ParseUUIDPipe)`,
  `ParseIntPipe`, `ParseEnumPipe`. Los de consulta, en un DTO de consulta.
- **Swagger completo:** `@ApiTags`, `@ApiOperation` y una
  `@ApiOkResponse`/`@ApiCreatedResponse` con el tipo del DTO de salida, más las
  respuestas de error que el endpoint puede dar.
- La seguridad es global (`AuthGuard` + `RolesGuard`): un endpoint nace
  protegido. Se abre con `@Public()` a propósito y se restringe por rol con
  `@Auth(...roles)`, el decorador compuesto (`applyDecorators`) que suma
  `@Roles`, `@ApiBearerAuth` y las respuestas 401 y 403 de Swagger.

## 6. DTOs de entrada

- Una clase por operación, con `class-validator`. Nunca un tipo o interfaz
  inline: no existe en tiempo de ejecución y el `ValidationPipe` no puede
  validarlo.
- Los de modificación se derivan con `PartialType`, `PickType` u `OmitType`
  **de `@nestjs/swagger`**, no de `@nestjs/mapped-types`: así la documentación
  refleja los campos.
- Paginación: `PaginationDto` de `common/dtos/`, extendido si el listado filtra.
- `@ApiProperty` en cada campo, con ejemplo.

## 7. DTOs de salida

- **Ningún endpoint devuelve una entidad.** Devuelve un `<nombre>-response.dto.ts`.
- La entidad se convierte con un **mapper explícito** (`<modulo>.mapper.ts`,
  `XMapper.toDto(entidad)`), igual que `OrderMapper`. Con `strict`, el
  compilador obliga a asignar cada campo del DTO: nada sale sin que alguien lo
  haya decidido.
- **No salen campos internos:** identificadores de proveedores (`firebase_uid`),
  tokens de notificación, datos de auditoría interna. Cada campo que se saca y
  hoy sale se anota en el commit con el cliente que lo usaba, si alguno.
- Las relaciones anidadas tienen su propio DTO de salida.

## 8. Servicios y casos de uso

- Un servicio por responsabilidad. Si un servicio pasa de ~250 líneas o de ~6
  dependencias, probablemente hace dos cosas.
- Las transacciones se abren con el `DataSource` o el `QueryRunner` y se pasan
  como `EntityManager` a quien participa. `withTransactionRetry` para las que
  pueden chocar por concurrencia.
- Errores: en módulos de soporte, las excepciones HTTP de Nest
  (`NotFoundException`, `ConflictException`...). En el dominio de un módulo
  núcleo, errores de dominio. **Nunca `throw new Error()`**: sale como 500 sin
  explicación.
- Los errores de base se traducen con `traducirErrorDeBase()`.

## 9. Configuración

- Se lee con `ConfigService`, tipado. **Nada de `process.env`** fuera de las
  funciones de configuración de `common/config/` (el patrón de `load` que
  documenta Nest) y de `data-source.ts`, que corre en la CLI de TypeORM sin
  Nest.
- Toda variable nueva se agrega al esquema de validación de Joi
  (`common/config/joi.validation.ts`): si falta, la app no arranca.

## 10. Base de datos

- El esquema cambia **sólo por migraciones**: `migration:generate`, se revisa el
  archivo y se commitea junto al cambio de entidad. Nunca `synchronize` fuera de
  un experimento local.
- Toda relación tiene su clave foránea declarada, salvo que haya una razón
  escrita al lado.
- Coordenadas y áreas en tipos de PostGIS, no en `varchar`.
- **Auditoría de datos** (`splg-docs/sistema/back/AUDITORIA.md`): un subscriber global registra
  todo lo que pasa por `save`, `softRemove` y `recover`. `update()`,
  `softDelete()`, `delete()` y los query builders **no** pasan por él: para una
  entidad de negocio se usa `save`/`softRemove` con la entidad cargada, o se
  llama a `AuditoriaDeDatos.registrar(manager, ...)` en la misma transacción.

## 11. Pruebas y verificación

- Prueba unitaria del servicio (soporte) o de cada caso de uso (núcleo), con los
  repositorios y puertos simulados.
- Nada se da por bueno sin probarlo contra la API corriendo: la colección de
  Postman (`postman/`) y el recorrido del pedido (`02 · Recorrido del pedido`),
  más de una vez.
- Un refactor no cambia comportamiento: la batería tiene que dar lo mismo antes
  y después, y **las respuestas tienen que conservar su forma**.

### Reglas de Jest (las hace cumplir `npm run verify`)

- **Cobertura con piso por módulo.** `verify` corre `jest --ci --coverage` y falla si
  un módulo baja de su piso (`coverageThreshold` en `package.json`: una entrada por
  carpeta de `src/` y `global` para lo que no tiene entrada propia). Los pisos son la
  cobertura medida, redondeada hacia abajo: **sólo se suben**, nunca se bajan para
  pasar el gate. Un módulo nuevo entra con su propia entrada. Sólo quedan fuera de la
  cobertura `main.ts`, `data-source.ts`, `migrations/` y los `index.ts`; los
  `*.module.ts` y `cli/` cuentan, porque tienen lógica (configuración de la base,
  guardas del CLI).
- Por eso `jest --coverage` sobre un solo archivo falla por los pisos de los demás
  módulos: para correr un archivo suelto se usa `npx jest <archivo>` sin cobertura.
- **Mocks limpios entre tests** en los unitarios (`clearMocks` y `restoreMocks`): un
  test no puede depender de un mock o un `spyOn` armado en otro. Los de integración
  (`test/jest-e2e.json`) no lo tienen.
- **ESLint en los tests** (`eslint-plugin-jest`): prohibido `.only`, `.skip` y los
  tests comentados; todo test tiene al menos una aserción (`expect`, el `.expect(...)`
  de supertest o `desempata`, que hace `expect` adentro; un helper nuevo se suma a
  `assertFunctionNames` sólo si adentro tira o hace `expect`); prohibido el `expect`
  de Jest dentro de un `if` o un `catch`, porque si la rama no se ejecuta el test pasa
  sin verificar nada. En una carrera se arma el resultado y se compara una sola vez
  contra los finales válidos.
- **Control de mutación.** Un test nuevo tiene que fallar si se revierte el arreglo que
  prueba; la entrega dice cómo se comprobó.
- **`node_modules` limpio.** La extensión Console Ninja de VS Code reescribe archivos de
  `node_modules` (`jest-runner`, `@nestjs/core`) y con eso Jest se cae al azar
  (SIGSEGV, 404 en specs de controladores). Si el gate falla sin motivo, `npm ci`.

## 12. Módulo terminado

Un módulo está alineado cuando cumple las doce:

1. Cero errores de `tsc` y de ESLint en sus archivos.
2. Cero `any`.
3. `forFeature` sólo con sus entidades; lo ajeno por servicio exportado; sin
   `forwardRef`.
4. DTO de entrada en todos los endpoints que reciben cuerpo o consulta.
5. DTO de salida en todos los endpoints, con mapper.
6. Pipes en todos los parámetros.
7. `ConfigService` en lugar de `process.env`.
8. Excepciones de Nest o de dominio; ningún `Error` suelto.
9. Archivos en kebab-case; propiedades en camelCase con la columna mapeada.
10. Swagger completo.
11. Prueba unitaria y verificación contra la API corriendo, con la forma de las
    respuestas igual que antes.
12. Sus DSD y su parte del diagrama de clases de diseño, actualizados en
    `splg-docs`.
