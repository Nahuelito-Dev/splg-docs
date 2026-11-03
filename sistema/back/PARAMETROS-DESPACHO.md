# Parámetros del despacho y frecuencia de las tareas programadas (M1)

Módulo inteligente M1 (negociación secuencial de asignación): CU-171 y CU-173. Lo que antes
eran constantes del programa se configura por distribuidora en `module_config`
(`configurable_process_enum`: `dispatch` y `scheduled_tasks`). Todo está también en Swagger
(`/docs`, tag "Configuración · Parámetros por distribuidora").

## Acceso

Rol `admin` o `super_admin`. El admin opera sobre su distribuidora (ignora `X-Distributor`);
el super admin elige con `X-Distributor` y, sin él, responde **400**
`Falta la distribuidora: enviá el header X-Distributor (slug o id)`. Chofer y cliente: 403.

## `GET` / `PUT /module-config/dispatch` (CU-171)

`PUT` guarda sólo los campos que vienen; lo que falta no se guarda y se lee con su valor por
omisión (un `PUT` sin campos restablece todo). Lo que viene se valida igual.

| Campo             | Tipo       | Regla                                                            | Por omisión       |
| ----------------- | ---------- | ---------------------------------------------------------------- | ----------------- |
| `radiusStepsKm`   | `number[]` | de 1 a 8 pasos, cada uno de 1 a 100 km y estrictamente creciente | `[5, 10, 15, 20]` |
| `offerTtlSeconds` | `integer`  | de 10 a 300 s: ventana de aceptación de cada oferta              | `30`              |
| `finishingRadiusMeters` | `integer` | de 0 a 5000 m: distancia al punto de entrega desde la que un chofer con un solo pedido en camino cuenta como «por terminar» (CU-013); `0` lo apaga | `300` |

Cualquier violación responde **400** con el detalle del campo; un campo desconocido también.

Respuesta de `GET` y `PUT`: los tres campos (con su valor efectivo) más `isDefault` (`true` si rigen
los valores por omisión: nada configurado, `PUT` sin campos, o todo coincide con ellos), `updatedAt` y `updatedByUserId` (quién modificó por última vez; `null` si nunca).

Cómo rige:

- `DispatchOrchestratorService` lee la configuración **en cada oferta** (pasos de radio y
  ventana); la asignación manual (`PATCH /orders/:id/assign/:deliveryId`) usa la misma ventana
  para el `expiresAt` del aviso al chofer.
- **Choferes por terminar su entrega (`finishingRadiusMeters`, CU-013).** La regla vive en un solo
  lugar, `situacionDelChofer` (`order/domain/chofer-por-terminar.ts`), y devuelve `libre`,
  `por_terminar` u `ocupado`. Es `por_terminar` el chofer con **un solo** pedido en curso, en estado
  `on_the_way`, cuya última posición conocida **y reciente** (el radar de Redis, la misma que reporta por socket o
  por `PATCH /orders/:id/location`; si tiene más de 2 minutos, no tiene fecha o la fecha está más de
  30 s en el futuro, no cuenta) está a `finishingRadiusMeters` o menos del punto de entrega de
  ese pedido (haversine, límite inclusivo). Sin posición, sin punto de entrega, con un pedido sólo
  `accepted` o con dos pedidos en curso es `ocupado`; con radio `0` la regla está apagada y rige el
  comportamiento de antes (sólo libres).
- `DispatchOrchestratorService` admite a los `libre` y a los `por_terminar` en las ofertas de M1; dentro
  de cada paso de radio los libres van antes que los por terminar. Siguen aplicando flota, carga del camión,
  habilitación laboral y distribuidora. **M4 (lotes), el despacho express y el diagnóstico de M4 usan
  sólo choferes libres.** La asignación manual (`PATCH /orders/:id/assign/:deliveryId`) no controla
  si el chofer está ocupado, como antes.
- **Aceptar un pedido más.** El chofer (rol `delivery`) que acepta (`PATCH /orders/:id/status`
  `accepted`) con otro pedido ya `accepted` recibe **409** «Ya tenés un pedido aceptado esperando:
  terminá el actual antes de tomar otro»: nunca dos encolados. Quedan el actual (`on_the_way`) y el
  nuevo (`accepted`). `GET /orders/delivery/me/active` devuelve el que va en camino; si no hay,
  el aceptado más antiguo (el que espera aparece al entregar el actual); y si no hay activos, el
  entregado en efectivo de hoy con el cobro pendiente. Un cobro pendiente nunca tapa a un pedido
  activo: así el pedido en espera se abre aunque el cobro del anterior haya quedado en «Más tarde».
  Es el mismo orden de siempre; el contrato no cambió.
  Un chofer con un pedido `accepted` que todavía no salió tampoco puede tomar otro del listado. El administrador no tiene este límite.
- **En la base:** `CHK_module_config_despacho` (migración `RadioPorTerminarEnDespacho1794700000019`) rechaza
  un `finishingRadiusMeters` fuera de 0..5000 o no entero, un `offerTtlSeconds` fuera de 10..300 o no
  entero y unos `radiusStepsKm` que no sean una lista de 1 a 8 elementos, aunque se escriban directo.
  El orden creciente y el rango de cada paso los valida sólo el servicio.
- Las ofertas ya creadas conservan su `expiresAt`; el cambio vale para las que se creen después.
- Copia en memoria de **1 minuto** por distribuidora (`DispatchSettingsService`). Guardar
  descarta la copia de esa distribuidora en la instancia que atiende el `PUT`; en las demás
  instancias el cambio rige, como máximo, un minuto después.

## `GET` / `PUT /module-config/scheduled_tasks` (CU-173)

`@Cron` no admite una expresión por distribuidora: cada tarea conserva su **tic fijo** y, en cada
tic, atiende sólo a las distribuidoras cuyo intervalo se cumplió. `PUT` guarda sólo los
campos que vienen; lo que falta se lee con su valor por omisión (un `PUT` sin campos restablece).

| Campo                            | Tarea                                                                      | Tic    | Regla                                      | Por omisión |
| -------------------------------- | -------------------------------------------------------------------------- | ------ | ------------------------------------------ | ----------- |
| `dispatchRetrySeconds`           | reintentos del despacho (ofertas vencidas y pedidos pendientes sin oferta) | 15 s   | múltiplo entero de 15, hasta 300 s (5 min) | `15`        |
| `reservationActivationSeconds`   | activación de reservas con la seña paga                                    | 5 min  | múltiplo entero de 300, hasta 86400 s      | `300`       |
| `unpaidReservationExpirySeconds` | vencimiento de reservas sin seña                                           | 1 h    | múltiplo entero de 3600, hasta 86400 s     | `3600`      |
| `unpaidMercadoPagoExpirySeconds` | vencimiento de pedidos de MercadoPago sin pagar                            | 30 min | múltiplo entero de 1800, hasta 86400 s     | `1800`      |
| `fleetAlertHour`                 | aviso de vencimientos de flota (hora de Argentina)                         | 1 h    | entero de 0 a 23                           | `8`         |

La respuesta suma `isDefault`, `updatedAt` y `updatedByUserId`, igual que `dispatch`.

Cómo rige:

- **Al empezar cada tic**, de una sola pasada, se decide a qué distribuidoras con trabajo pendiente
  les toca y se ponen sus marcas en ese momento; después se procesa. Si el tic falla antes de
  procesar una distribuidora, se le devuelve la marca (no pierde un intervalo entero). Cada
  distribuidora se consulta con su propio límite (50) y orden por antigüedad: ninguna tapa a otra.
- **Intervalo igual al tic**: la tarea corre para la distribuidora en cada tic, sin marcas.
- **Intervalo mayor**: la marca de última ejecución vive en Redis
  (`scheduled-task:<campo>:<distributorId>:<generación>`), creada con `SET NX` (con varias
  instancias, una sola gana el ciclo). Mientras exista, la distribuidora no corre. Vence **medio tic
  antes** del intervalo para absorber el jitter del reloj del cron.
- **Generación**: cada `PUT` incrementa `scheduled-task:gen:<distributorId>` y la clave de la marca
  la incluye. Una marca de la configuración vieja nunca queda viva (ni la que otra instancia o un
  tic en curso creen después del `PUT`). Cada lectura compara la generación de Redis con la de la
  copia en memoria; si difiere, la descarta y relee. El intervalo nuevo rige desde el ciclo siguiente.
- El tope de `dispatchRetrySeconds` es 300 s: una oferta vencida queda `offered` hasta que corre el
  ciclo de su distribuidora, y con más el pedido pasaría demasiado sin re-ofrecerse.
- Las ofertas vencidas de una distribuidora a la que todavía no le toca quedan `offered` con
  `expiresAt` pasado hasta su próximo ciclo (el chofer todavía podría aceptarlas).
- `fleetAlertHour` (hora de Argentina): el cron corre cada hora en punto (zona `America/Argentina/Buenos_Aires`) y avisa a la distribuidora cuya hora
  configurada es la actual (una vez por día; cada tarea se avisa una sola vez por `alertedAt`).
- Los barridos de mantenimiento globales (`s3-cleanup`, conciliación y stock bajo, desactivación
  de recargos) no son parte de esta configuración.

## Esquema

Migración `1792072095738-ParametrosDespachoYTareas`: agrega `dispatch` y `scheduled_tasks` a
`configurable_process_enum`. Al revertir se borran las filas de esos dos procesos.
