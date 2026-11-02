# Procesos automáticos: parámetros por distribuidora y zonas vencidas

CU-172 (parámetros de los cuatro procesos automáticos) y CU-151 (zonas de cobertura vencidas). Todo está también en
Swagger (`/docs`, tag "Configuración · Parámetros por distribuidora").

## Parámetros de un proceso automático (CU-172)

Acceso: igual que el despacho y las tareas programadas (`PARAMETROS-DESPACHO.md`): rol `admin` o `super_admin`; el admin
opera sobre su distribuidora y el super admin elige con `X-Distributor` (sin él, **400**
`Falta la distribuidora: enviá el header X-Distributor (slug o id)`). Chofer y cliente: **403**.

| Ruta | Qué hace |
|---|---|
| `GET /module-config/processes` | Los cuatro procesos con su esquema (`fields`: clave, tipo, rango, unidad, valor por omisión) y sus valores vigentes. |
| `GET /module-config/:process` | Un proceso. |
| `PUT /module-config/:process` | Guarda parámetros. Cuerpo: `{ <parámetro>: <número> }`. |

`:process` es uno de `fleet_planner`, `repurchase`, `route_batching`, `cylinder_recovery`. Cualquier otro
(incluidos `stock_control`, y `dispatch`, `scheduled_tasks` y `express_dispatch`, que tienen sus propias rutas fijas) responde **404**.
Las rutas fijas `dispatch`, `scheduled_tasks` y `express_dispatch` se resuelven primero. Los parámetros de la compra express
(recargo, radio, horario, tiempos) son de `/module-config/express_dispatch` y están en `EXPRESS-REINTEGROS.md`.

`PUT` **reemplaza**: se guarda sólo lo que viene, lo que falta se lee con su valor por omisión y `{}` restablece todo (la misma convención que el despacho, CU-171, y el panel). Los leen los módulos inteligentes ya construidos: M2 ([PLANIFICADOR-FLOTA.md](PLANIFICADOR-FLOTA.md)), M3 ([RECOMPRA.md](RECOMPRA.md)) y M5 ([RECUPERO-ENVASES.md](RECUPERO-ENVASES.md)); cada página lista sus parámetros con rango y valor por omisión. M3 y M5 vienen apagados por omisión (`enabled` en 0) y no hacen nada hasta que la distribuidora los enciende.
Se valida con el esquema del proceso (`src/distributor/process-config.ts`); un campo desconocido, de otro tipo, decimal en un entero,
fuera de rango o una regla cruzada incumplida responde **400** con el campo
(`anticipationDays: tiene que ser un entero entre 1 y 30`, `property invento should not exist`).

Respuesta de `GET` y `PUT`: `process`, `title`, `description`, `fields[]`, `params` (valor efectivo de cada parámetro), `isDefault`,
`updatedAt` y `updatedByUserId` (`null` si nunca se modificó).

| Proceso | Parámetro | Regla | Por omisión |
|---|---|---|---|
| `fleet_planner` (CU-105) | `cronHour` | entero 0–23, hora de Argentina | 3 |
| | `proposalTtlHours` | entero 1–168 | 24 |
| | `topNWindows` | entero 1–10 | 3 |
| | `minVehiclesPerZone` | entero 0–100 | 1 |
| | `minSampleDays` | entero 1–365 | 30 |
| | `decay` | número 0–1 | 0.7 |
| `repurchase` (CU-106) | `minOrders` | entero 2–50 | 3 |
| | `anticipationDays` | entero 1–30 | 3 |
| | `invitationTtlHours` | entero 1–168 | 24 |
| | `minIntervalDays` | entero 1–90 | 7 |
| | `runHour` | entero 0–23, hora de Argentina | 9 |
| `route_batching` (CU-107) | `maxBatchSize` | entero 2–20 | 4 |
| | `groupingRadiusKm` | número 0,5–50 | 3 |
| | `slotToleranceMinutes` | entero 0–480 | 60 |
| | `offerTtlSeconds` | entero 10–600 | 60 |
| | `evaluationFrequencyMinutes` | entero 1–1440 | 15 |
| `cylinder_recovery` (CU-108) | `toleranceDays` | entero 1–365 | 30 |
| | `escalationStepDays` | entero 1–90 | 7 |
| | `escalationAmountThreshold` | número 0–100 000 000 | 50 000 |
| | `pickupOfferTtlHours` | entero 1–720 | 72 |

Los esquemas son la **primera definición** de los parámetros de esos cuatro módulos (el diseño sólo
nombra qué se parametriza, no los rangos): el módulo que los consuma los lee con
`ProcessConfigService.obtener(distributorId, proceso)` (valores efectivos, con los de omisión donde falte o sea inválido lo guardado)
y puede ampliar su esquema en `process-config.ts`. Los procesos todavía no los consumen: las ejecuciones en curso no se interrumpen
y la siguiente lee lo guardado.

La tabla es `module_config` (una fila por distribuidora y proceso, `UNIQUE (distributor_id, module)`), sin migración nueva: los
valores del enum `configurable_process_enum` ya existían.

## «Armar ahora» de los recorridos: por qué no se armó un lote (CU-107)

`POST /api/v2/route-batches/run` (admin) responde `candidates`, `batches` y `orders` y, cuando algún pedido quedó sin lote,
explica por qué con dos campos:

- `reasons`: cuatro enteros que cuentan **pedidos candidatos que quedaron sin lote**, cada uno en un solo motivo (la suma de
  los cuatro es `candidates - orders`). `noDriversNearby`: ningún chofer de la distribuidora en el radar.
  `driversNotEligible`: hay choferes en el radar pero ninguno puede recibir el lote (vehículo en taller o fuera de servicio,
  documentación o situación laboral, carga del camión, pedido en curso o lote ya ofrecido). `notEnoughStops`: el grupo
  quedó con menos de 2 paradas por radio, franja o capacidad del vehículo. `lockConflict`: otro proceso (por ejemplo el
  despacho individual) tomó o cambió los pedidos mientras se armaba.
- `driversNotEligibleDetail`: hasta 5 choferes de la distribuidora, sin repetir, con `driverName` y `reasons` (textos en
  castellano escritos para el administrador). Vacío si se armó todo o no hay choferes bloqueados.

El detalle por chofer sólo se calcula en «armar ahora»; la pasada periódica no lo paga. El panel (Recorridos) arma con
esto el aviso «No se armó ningún lote: …».

## Zonas de cobertura vencidas (CU-151)

`CoverageZoneExpiryCron` (`src/coverage-zone/coverage-zone-expiry.cron.ts`) corre **cada cinco minutos** y desactiva las zonas con
`valid_until <= now()` que siguen activas y no están dadas de baja (`deletedAt IS NULL`), de **todas** las distribuidoras, con un
solo `UPDATE ... RETURNING` (dos barridos simultáneos no desactivan dos veces la misma). No borra la zona ni toca su polígono,
su recargo ni su vigencia; sólo `isActive` pasa a `false`. Deja en el log cuáles desactivó
(`Zona vencida desactivada: <id> "<nombre>" (distribuidora <id>, venció <fecha>)`).

- **Una sola instancia:** el barrido corre bajo el cerrojo Redis `cron:coverage-zone-expiry` (TTL 4 min). Si otra instancia lo tiene,
  el tic no hace nada. Si la ejecución falla, se registra el error y `withLock` libera el cerrojo, así que el tic siguiente lo toma.
- **Sin zonas vencidas** la ejecución termina sin hacer nada (el caso habitual).
- **Qué cambia para el panel:** `GET /coverage-zones` (sólo activas) deja de mostrar la zona; con `includeInactive=true` aparece
  con `isActive: false`. La zona queda en la auditoría de datos (`isActive: true → false`, sin usuario: lo hizo el sistema).
- **Cobertura (decisión de nahue):** `checkCoverage` cubre todo con recargo 0 **sólo si la distribuidora nunca definió zonas**
  (cuenta cualquier zona no borrada, activa o no, vigente o no). Con zonas pero ninguna activa y vigente, **no cubre nada** (el alta
  de pedidos y `PATCH /orders/:id/address` responden 400 «fuera de la zona de cobertura»). Una zona con `valid_until` pasado deja de
  contar en el acto, aunque el barrido todavía no la haya apagado (sin hueco de 5 minutos).
- **Aviso:** si el barrido apaga la última zona activa de una distribuidora, emite `coverage:no-active-zones`
  (`{ distributorId, zoneIds, at }`) a los admins de esa distribuidora y a los super admin (mismo canal que `order:no-drivers`); el
  panel lo muestra en la campana y, en Zonas de cobertura, con un aviso mientras no haya una zona activa y vigente.
- **Fecha de fin vencida:** crear una zona activa, o reactivarla / cambiarle `validUntil`, con `validUntil` ya pasado responde **400**
  (`validUntil ya pasó: una zona vencida no puede quedar activa`). Una zona creada inactiva sí puede tenerla.
- **Fechas de vigencia en día argentino:** `validFrom` y `validUntil` (alta `POST /coverage-zones` y edición `PATCH /coverage-zones/:id`) aceptan un día
  `YYYY-MM-DD` o un instante ISO con hora. Un día se interpreta en hora argentina: `validFrom` rige **desde las 00:00 ART** de ese día y
  `validUntil` **incluye el día entero** (la zona vence a las **23:59:59.999 ART**; el barrido la desactiva recién después). Un instante con
  hora se guarda tal cual. Desde y hasta el mismo día es una zona de un día; un hasta anterior al desde responde 400, y un día que no existe
  (por ejemplo `2026-02-30`) también. En la edición, `null` quita ese límite (rige desde siempre / no vence) y omitir el campo no lo toca.
  El panel muestra y edita el día argentino del instante guardado.
