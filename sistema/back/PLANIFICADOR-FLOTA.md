# Planificador de taller — módulo M2, flota predictiva (CU-105, API v2)

El planificador anticipa los vencimientos de la flota con el **uso real** de cada vehículo, elige una ventana de taller
que no deje la zona sin vehículos y se la **propone al chofer**. Si el chofer no responde o rechaza, ofrece la
siguiente alternativa; si se agotan, **escala al administrador**. El administrador confirma la ventana y, al cerrar la
tarea, el gasto sale de Caja (`FINANZAS.md`). En el panel: Flota → «Planificador de taller» (`/fleet/planner`).

## De dónde sale el uso

`VehicleUsageCron` (todos los días a las 01:30, con cerrojo en Redis; también lo corre el planificador antes de
estimar) escribe `vehicle_usage_log` con los km de cada vehículo por día, recalculando los últimos 90 días (es
idempotente: una fila por vehículo y día).

- **Recorrido de las entregas:** la distancia entre las paradas entregadas del día, en el orden en que se entregaron, por
  1,3 para aproximar las calles. Un día con una sola parada no tiene recorrido medible y no se escribe.
- **Odómetro:** entre dos lecturas con fecha (cargas de combustible y cierres de tareas con kilometraje), la diferencia es
  lo recorrido de verdad y **reemplaza** lo estimado, repartida entre los días del tramo. Gana el odómetro porque es una
  medición.

La estimación de km por día promedia sólo los días con registro (un día sin registro no es un día sin uso), ponderados
por semana (`decay`) y corregidos por estacionalidad. Hace falta un mínimo de días con dato (`minSampleDays`, 10 por
omisión); sin historial propio usa el promedio de la flota del mismo tipo. Si el último registro es más viejo que
`usageStaleDays` (14 por omisión), los datos se consideran desactualizados y no se proyecta con ellos.

## Cómo planifica

1. **Pronóstico:** para cada tarea de un plan por km proyecta la fecha en que se llega al kilometraje
   (`predicted_due_at`); las de fecha fija usan su vencimiento. Una tarea entra a planificarse con la anticipación de su
   plan (`leadTimeDays`) o cuando faltan `anticipationKm` kilómetros (0 la desactiva).
2. **Ventanas candidatas:** días hábiles del taller (`workshopDays`, por omisión lunes a sábado; sin feriados nacionales)
   dentro del horizonte (`horizonDays`), con el aviso mínimo (`minLeadDays`) y antes del vencimiento, en el horario del
   taller (`workshopStartHour`–`workshopEndHour`, hora argentina). Se ordenan por la demanda esperada (pedidos de ese
   día de la semana en `demandWeeks` semanas, más los agendados) en la **zona** del vehículo (donde más entregó en los
   últimos `zoneLookbackDays`). Nunca deja la zona con menos de `minVehiclesPerZone` vehículos: cuentan también las
   propuestas pendientes y las acordadas.
3. **Propuesta al chofer** de la asignación vigente, con vigencia `proposalTtlHours`: socket `maintenance:proposal` y
   push. Aceptar deja el caso **esperando al administrador** (no programa la tarea); rechazar ofrece la siguiente
   ventana, o con una alternativa viable la deja acordada para el administrador.
4. **Escalamiento:** sin alternativas, sin chofer o sin cobertura, el caso se escala a la bandeja del administrador
   (`maintenance_escalated`, con mail la primera vez; se reitera una vez por día).
5. **Confirmación:** el administrador confirma (o fija otra ventana): la tarea queda `scheduled` y **la agenda del
   vehículo se bloquea** en esa ventana (el despacho no le ofrece pedidos al chofer). Una ventana que ya pasó no se
   confirma (400).
6. **Lo urgente** (vencido o sin margen) se negocia igual, desde el primer día hábil, con ventanas marcadas urgentes.
   Una habilitación bloqueante vencida deja el vehículo fuera de servicio (`grounded`) y libera su asignación.

Editar el turno agendado (`scheduledAt`, `PATCH /fleet/tasks/:id`) de una tarea con la ventana de M2 ya confirmada mueve esa ventana en la misma transacción, conservando la duración. Si el turno viene **sólo con fecha** (`YYYY-MM-DD`, lo que manda el panel) o a medianoche argentina, la ventana pasa a ese día (hora argentina) con su hora de inicio de siempre; si trae **hora**, arranca a esa hora. La tarea queda con `scheduledAt` igual al inicio de la ventana. Si el turno no cambió (el panel lo reenvía en cada edición), no se toca nada. Una ventana nueva que arrancaría en el pasado da 400 «scheduledAt: la ventana tiene que ser a futuro». Borrar el turno (`null`) cancela el caso. El caso registra quién lo movió o canceló (`resolvedByUserId`, `chosenSource = admin`). No se tocan ventanas que ya terminaron.

Cerrar o cancelar la tarea por fuera del planificador cierra su caso; dar de baja el vehículo cancela sus casos
abiertos. El seguro no pasa por taller: se paga por sus cuotas (`SEGUROS.md`).

## API (`/api/v2`)

**Administrador:** `GET /fleet/maintenance-planner` (casos con conteo por estado; filtros `status`, `carId`,
`pending`), `GET .../cases/:id`, `GET .../forecast[?carId]`, `GET|PATCH .../settings`, `POST .../run`,
`POST .../cases/:id/confirm|cancel`, `POST .../tasks/:taskId/force-window|replan`. Un caso escalado por cobertura se
puede confirmar igual con `ignoreCoverage: true`.

**Chofer** (app del chofer: aviso de propuesta nueva y pantalla «Taller» en el menú): `GET /driver/maintenance-proposals` (la vigente primero; cada una con `caseStatus`, `urgent`, `projectedDueAt` y la ventana que confirmó el administrador, `confirmedStart`/`confirmedEnd`), `GET .../maintenance-proposals/:id`,
`GET .../maintenance-proposals/settings` (horario, días, feriados, aviso mínimo, horizonte),
`POST .../:id/accept`, `POST .../:id/reject { reason, alternative?: { start, end } }`. Eventos de socket:
`maintenance:proposal`, `maintenance:proposal-closed`, `maintenance:window-confirmed` (con `source`) y
`maintenance:case-escalated`.

## Parámetros por distribuidora (`fleet_planner`)

`cronHour`, `proposalTtlHours`, `topNWindows`, `minVehiclesPerZone`, `minSampleDays`, `decay`, `horizonDays`,
`minLeadDays`, `zoneLookbackDays`, `demandWeeks`, `workshopStartHour`, `workshopEndHour`, `workshopDays` (máscara:
1 domingo, 2 lunes, 4 martes, 8 miércoles, 16 jueves, 32 viernes, 64 sábado), `usageStaleDays`, `anticipationKm` y
`driverEmail` (0/1: también un mail al chofer con cada propuesta; por omisión no). Validados en el DTO y con un CHECK en
la base. En la demo, `usageStaleDays` está en 30 porque sus últimas entregas son de mediados de octubre.

## Diferencias con la especificación del CU-105

- Aceptar no programa la tarea: queda esperando la confirmación del administrador (como pide el paso 8).
- El chofer puede rechazar proponiendo otra ventana; si es viable, queda acordada para el administrador.
- El estado «vencido» se deriva de la fecha y no se guarda.
- El seguro no pasa por taller.
- Las ventanas son de un día, con el horario de taller de la distribuidora.
- Los feriados son los nacionales de 2026 y 2027, cargados a mano; no hay feriados provinciales.
