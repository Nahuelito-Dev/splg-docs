# M3′ — Planificador Predictivo de Mantenimiento y Habilitaciones de Flota

> Propuesta de módulo inteligente para reemplazar a **M3 — Reserva y restitución
> atómica de stock** en la terna especificada en profundidad (Doc 3 §6).
>
> Estado: **propuesta de análisis y diseño**. No implementado.
> Fecha: 2026-08-27.

---

## 1. Por qué se reemplaza M3

### El problema con la reserva atómica de stock

`StockReservationService` (`src/order/domain/stock-reservation.service.ts`) son
80 líneas con dos métodos:

- `reserve()` → lock pesimista, valida stock, resta, guarda.
- `restore()` → lock pesimista, suma, guarda.

Eso no es un módulo inteligente: es **atomicidad transaccional**, la A y la D de
ACID. Un módulo inteligente sustituye *una decisión que tomaría un humano*; acá
no hay decisión que sustituir, hay un procedimiento determinista que siempre
hace lo mismo.

El único punto con forma de decisión es `applyCancellationPolicy()`
(`src/order/application/cancel-order.use-case.ts`), que resuelve si devolver el
stock según quién cancela y en qué estado está el pedido. Pero es un árbol de
`if` sobre una política de negocio escrita a mano: son *reglas*, no inferencia.

### El criterio que lo descarta

La consigna de la cátedra pide describir cada proceso automatizado por
**tiempos, grado de automatización, disparadores, resultados esperados e impacto
en los registros**. El eje del **disparador** es el que resuelve la discusión:

| Proceso | Disparador | ¿Propio? |
|---|---|---|
| Despacho por proximidad | Evento: creación de pedido | Sí |
| Reintento con radio expandido | Temporal: el reloj | Sí, el más puro |
| Reserva atómica de stock | La transacción del propio usuario | **No tiene** |

La reserva de stock ocurre **dentro** del request HTTP, con el cliente esperando
la respuesta del otro lado. No es un proceso: es un paso de un proceso.

> **Test de una línea:** un proceso automatizado tiene que poder ejecutarse sin
> un humano esperando el resultado.

### Qué hacer con M3 (no se descarta, se reubica)

1. **Permanece en Doc 2 §3**, en la tabla de módulos automáticos (puestos #3 y #4).
   Esa tabla no se toca.
2. **Lo técnicamente valioso se reubica al capítulo de arquitectura/calidad**
   como *mecanismo de integridad transaccional*: lock pesimista que previene
   oversell, prevención de race conditions y manejo de la carrera
   pago-vs-expiración del webhook de MercadoPago. Ahí el criterio de evaluación
   es "¿está bien resuelto?", y lo está.
3. **Solo cambia cuál de los diez se especifica en profundidad** en Doc 3 §6.

### El beneficio secundario: la terna queda coherente

Sacando M3 quedarían M1 y M2, que son el mismo pipeline (Doc 3 lo dice textual:
*"los 3 que forman el pipeline completo de despacho automático"*). M2 es el
reintento de M1 con el radio más grande. Con M3′ los tres cubren naturalezas
distintas:

| | Módulo | Naturaleza | Decide… |
|---|---|---|---|
| **M1** | Despacho por proximidad | Reactivo — geoespacial | …**ahora** |
| **M2** | Cron de reintentos | Adaptativo — relaja restricciones en el tiempo | …**después** |
| **M3′** | Mantenimiento predictivo de flota | Predictivo — infiere y planifica con restricciones | …**antes** |

Presente, futuro inmediato, futuro proyectado.

---

## 2. Evaluación contra los lineamientos de la cátedra

### El patrón que premian los ejemplos

Los tres ejemplos de la cátedra (reagendado de turnos, presupuestos a
proveedores, lista de espera de biblioteca) comparten una misma forma: recorrer
una lista de forma secuencial, ofrecer algo con **vigencia limitada**, esperar
respuesta, pasar al siguiente ante rechazo o timeout, y cerrar con una
**decisión humana** cuando hay plata de por medio.

No premian el cálculo: premian el **flujo de interacción**.

### Cumplimiento

| Criterio | Veredicto |
|---|---|
| Automatiza un flujo con valor agregado | **Cumple.** Reduce costos: una rotura no programada cuesta más que un mantenimiento planificado. Evita multas por habilitación vencida y el riesgo legal de operar carga peligrosa con documentación no vigente |
| No es intrínseco al PMV | **Cumple con claridad.** El sistema vende garrafas sin gestión de flota |
| Es más que una consulta SQL | **Cumple con el flujo de negociación de la etapa ③bis.** Sin esa etapa el módulo es cálculo + notificación, y ahí sí queda expuesto |
| Es parametrizable | **Cumple ampliamente.** Ver §6 |
| Decisión onerosa en manos humanas | **Cumple.** El sistema propone la ventana; el administrador la confirma. El gasto nunca lo decide el sistema |
| Flujo entre varios usuarios | **Cumple.** Sistema → chofer → administrador → taller |

### Riesgo identificado y su mitigación

El diseño puramente predictivo (estimar, proyectar, avisar) es fuerte en
cálculo pero **débil en flujo de interacción**, que es justamente lo que los
ejemplos de la cátedra valoran. Evaluado con ese criterio puede leerse como
"un cálculo y una notificación".

**Mitigación:** el módulo no impone la ventana de taller, la **negocia** —
etapa ③bis. Eso lo alinea con el patrón de la lista de espera de biblioteca
(oferta secuencial con vigencia y escalamiento) y con el de presupuestos a
proveedores (cotización a una lista de talleres).

### Ubicación en la terna

Se recomienda presentar la terna así:

| | Módulo | Patrón de la cátedra | Aporta |
|---|---|---|---|
| **A** | Despacho secuencial con oferta, timeout y radio progresivo (M1+M2 **unificados**) | Lista de espera de biblioteca | Opera el presente |
| **B** | Mantenimiento predictivo de flota (este documento) | Reagendado + presupuestos | Protege el activo — reduce costos |
| **C** | Recompra predictiva (D4 del roadmap) | Reagendado de turnos | Genera demanda — produce ingresos |

Dos observaciones sobre la terna actual:

1. **M1 y M2 no deberían presentarse por separado.** Aislados, uno queda en
   "hacer un GEORADIUS" y el otro en "un cron". Unificados son un flujo de
   oferta secuencial con timeout y relajación progresiva de restricción, que es
   el patrón de la biblioteca. Además libera un lugar en la terna.
2. **M1 tiene exposición en el criterio de PMV.** Asignar un pedido a un chofer
   es intrínseco a una app de delivery — es el caso del comedor. Es defendible
   (el PMV sería la asignación manual por un operador), pero hay que
   argumentarlo explícitamente.

> **Nota:** el último lineamiento admite la **integración con terceros** como
> proceso automatizado, y nombra MercadoPago y las APIs de resolución de rutas
> de transporte. Conviene consultarlo con la cátedra antes de descartar la
> pasarela de pagos como opción.

---

## 3. Análisis de viabilidad

Cuatro elementos ya presentes en el sistema sostienen el módulo:

**a) La entidad `Car` ya existe** (`src/car/entities/car.entity.ts`): patente
única, marca, modelo, año, capacidad en kg, chofer asignado y `distributor_id`
(multi-tenant). Es CRUD puro — sin kilometraje, sin estado, sin mantenimiento.
El sustrato del dominio está; el módulo inteligente sigue siendo trabajo real.

**b) El insumo predictivo ya se genera, y es propio.** El sistema hace tracking
GPS del chofer durante cada entrega (`startTracking`/`stopTracking` en
`RealtimeDispatchPort`, sobre Redis GEO). De ahí se deriva el **kilometraje real
recorrido por vehículo sin que nadie cargue un odómetro a mano**. El módulo no
es un calendario con alarmas: es un estimador alimentado por telemetría propia.

**c) El enganche con la logística tiene dónde ir.** En
`DispatchOrchestratorService.findNearestAvailable()` los candidatos ya pasan por
un filtro (`filterByDistributor`). Un segundo filtro por aptitud del vehículo
mete el mantenimiento **dentro del despacho**.

**d) Hay precedente arquitectónico.** `CylinderLifecyclePort` ya implementa este
patrón: un módulo acoplado al pedido por un puerto, best-effort, no-op si la
distribuidora no lo usa.

La infraestructura no cambia: `@Cron` ya está, FCM y WebSocket ya están, y
`coverage-zone` y `time-slot` ya existen (se usan en la etapa ③).

---

## 4. Modelo conceptual

| Concepto | Rol |
|---|---|
| `Vehicle` (extiende `Car`) | Agrega `odometer_km`, `odometer_source`, `fleet_status` (ACTIVE / IN_SERVICE / GROUNDED), `in_service_since` |
| `MaintenancePlan` | La **regla**: nombre, disparo (`BY_KM` / `BY_TIME` / `BY_FIXED_DATE`), intervalo, ventana de anticipación, criticidad **BLOCKING** vs **NON_BLOCKING** |
| `MaintenanceTask` | La **instancia**: `FORECAST → SCHEDULED → IN_PROGRESS → DONE / OVERDUE`, con `predicted_due_date`, ventana asignada, taller y costo |
| `VehicleUsageLog` | Append-only: km, cantidad de pedidos y horas en ruta por vehículo y día. Alimenta al predictor |

### Decisión de diseño: una sola abstracción para mantenimiento y documentación

**No se modela la documentación como entidad aparte.** La RTO, el seguro, la
licencia habilitante del chofer y la recarga del matafuegos son todos
`MaintenancePlan` con disparo `BY_FIXED_DATE` y criticidad `BLOCKING`.

Una única abstracción cubre *"el aceite se cambia cada 10.000 km"* y *"el seguro
vence el 30/11"*. Queda más limpio en el diagrama de clases y es un punto
defendible en la presentación.

`VehicleUsageLog` es append-only por la misma razón que `cylinder_movement`:
auditabilidad y trazabilidad del insumo que alimenta la predicción.

---

## 5. Especificación del módulo (formato Doc 3 §6)

**Archivo previsto:** `src/fleet/application/maintenance-planner.service.ts`

### Descripción

El sistema estima el consumo diario de cada vehículo a partir del historial de
uso derivado del tracking GPS, proyecta cuándo va a vencer cada tarea de
mantenimiento o habilitación, y planifica automáticamente la ventana de taller
que minimiza el impacto sobre la operación. Si un vehículo queda inhabilitado,
lo excluye del despacho sin intervención humana.

### Entradas

- `VehicleUsageLog` — historial de km/día por vehículo (últimos N días)
- `MaintenancePlan` — reglas activas por vehículo o tipo de vehículo
- `MaintenanceTask` en estado `FORECAST`
- `Vehicle.odometer_km` — última lectura conocida
- Demanda histórica por franja horaria (`time-slot`) y zona (`coverage-zone`)

### Proceso

#### Etapa ① — Estimación de consumo

Media móvil ponderada de km/día, con más peso a las semanas recientes.

```typescript
estimateDailyKm(vehicleId: string, days = 90): number {
  const logs = await this.usageRepo.findRecent(vehicleId, days);

  if (logs.length < MIN_SAMPLE_DAYS) {
    // Arranque en frío: promedio de la flota del mismo tipo de vehículo
    return await this.usageRepo.fleetAverageByType(vehicle.type_car);
  }

  // Ponderación exponencial: las semanas recientes pesan más
  const weighted = logs.reduce((acc, log, i) => {
    const weight = Math.exp(-DECAY * i);
    return { sum: acc.sum + log.km * weight, weights: acc.weights + weight };
  }, { sum: 0, weights: 0 });

  const baseKmDay = weighted.sum / weighted.weights;

  // Ajuste estacional: el consumo de garrafas en Misiones tiene pico invernal
  return baseKmDay * this.seasonalFactor(currentMonth);
}
```

> El ajuste estacional no es cosmético: un promedio plano subestima el desgaste
> de julio, que es el mes de mayor demanda del rubro.

#### Etapa ② — Proyección de vencimiento

```typescript
projectDueDate(task: MaintenanceTask, vehicle: Vehicle): Date {
  if (task.plan.trigger === 'BY_FIXED_DATE') return task.plan.fixed_date;

  const kmPerDay = this.estimateDailyKm(vehicle.vehicle_id);
  const kmRemaining = task.due_km - vehicle.odometer_km;
  const daysRemaining = Math.floor(kmRemaining / kmPerDay);

  return addDays(today, daysRemaining);
}

// Se alerta cuando entra en la ventana de anticipación del plan
// (ej: 60 días para RTO, 15 para cambio de aceite)
shouldAlert(task): boolean {
  return daysBetween(today, task.predicted_due_date) <= task.plan.lead_time_days;
}
```

#### Etapa ③ — Planificación con restricciones

Es el núcleo del módulo: no alcanza con avisar, hay que elegir **cuándo**.

```typescript
scheduleTask(task: MaintenanceTask): ScheduledWindow | null {
  const candidates = this.enumerateWindows(today, task.predicted_due_date);

  const feasible = candidates.filter(w =>
    // Restricción dura: antes del vencimiento proyectado
    w.date <= task.predicted_due_date &&
    // Restricción dura: no dejar la zona bajo el mínimo operativo
    this.fleetCoverage.remainingActive(task.vehicle.zone, w) >= MIN_VEHICLES_PER_ZONE
  );

  if (feasible.length === 0) return null;  // escala al admin

  // Objetivo: la franja de menor demanda histórica proyectada
  return feasible.reduce((best, w) =>
    this.demandForecast(w) < this.demandForecast(best) ? w : best
  );
}
```

La demanda proyectada sale de los pedidos históricos por `time-slot`, y el
mínimo operativo se evalúa por `coverage-zone`. Ambos módulos ya existen.

#### Etapa ③bis — Negociación secuencial de la ventana

Es la etapa que le da al módulo la forma de flujo que la cátedra valora. El
sistema **no impone** la ventana: la ofrece, espera, y ante silencio o rechazo
pasa a la siguiente. El patrón es el de la lista de espera de biblioteca.

```typescript
async negotiateWindow(task: MaintenanceTask): Promise<void> {
  const candidates = this.scheduleTask(task, TOP_N_WINDOWS);  // las N mejores

  for (const window of candidates) {
    const proposal = await this.proposals.create({
      task_id: task.id,
      window,
      recipient: task.vehicle.assigned_driver_id,
      expires_at: addHours(now, PROPOSAL_TTL_HOURS),   // parametrizable
    });

    await this.notifications.sendWindowProposal(proposal);

    const answer = await this.proposals.awaitAnswer(proposal);  // por cron

    if (answer === 'ACCEPTED') {
      return this.confirmAndBlockAgenda(task, window);
    }
    // RECHAZADA o VENCIDA -> se ofrece la siguiente ventana
  }

  // Se agotaron las ventanas: decide un humano (criterio de la catedra:
  // las decisiones onerosas no las toma el sistema)
  await this.notifications.escalateToAdmin(task, candidates);
}
```

**Extensión opcional — cotización a talleres.** Antes de confirmar, el sistema
puede solicitar presupuesto a una lista de talleres registrados y presentarle
al administrador el cuadro comparativo. Es el ejemplo de presupuestos a
proveedores de la catedra, aplicado a flota. El sistema reune la informacion;
la contratacion la decide una persona.

**Estados del flujo:** `PROPOSED -> ACCEPTED | REJECTED | EXPIRED -> ESCALATED`

#### Etapa ④ — Realimentación al despacho

```typescript
// Puerto que el módulo `order` consume
abstract class FleetAvailabilityPort {
  abstract isVehicleFit(vehicleId: string, at: Date): Promise<boolean>;
}

// En DispatchOrchestratorService.findNearestAvailable(), junto al filtro de tenant:
const eligible = await this.filterByDistributor(drivers, distributorId);
const fit = await this.filterByVehicleFitness(eligible);   // ← nuevo
```

Un vehículo `GROUNDED` (RTO vencida, seguro vencido) o dentro de su ventana de
taller deja de recibir ofertas. **Acá el módulo deja de ser un recordatorio y
pasa a gobernar la operación.**

### Salidas

- `MaintenanceTask` en `SCHEDULED` con ventana asignada
- Notificación FCM/email al administrador con la anticipación configurada
- `Vehicle.fleet_status` actualizado
- Exclusión efectiva del vehículo en el despacho

### Precondiciones

- El vehículo existe y pertenece a una distribuidora activa
- Existe al menos un `MaintenancePlan` aplicable
- Hay historial de uso suficiente, o promedio de flota disponible como respaldo

### Postcondiciones

- Toda tarea en ventana de anticipación tiene `predicted_due_date` calculada
- Toda tarea alertada quedó `SCHEDULED` con ventana, o escalada al admin si no
  había ninguna ventana factible
- Ningún vehículo con habilitación vencida (`BLOCKING`) recibe ofertas

---

## 6. Disparadores y tiempos

| Disparador | Frecuencia | Acción |
|---|---|---|
| Cron diario | 03:00 | Recalcula predicciones y replanifica |
| Evento `order.delivered` | Por entrega | Acumula km del viaje en `VehicleUsageLog` |
| Evento `maintenance.completed` | Por tarea | Resetea contador y proyecta la siguiente |

**Grado de automatización:** autónomo con supervisión. El sistema planifica
solo; el administrador confirma o reprograma la ventana propuesta.

**Impacto en los registros:** crea `MaintenanceTask` y `VehicleUsageLog`,
actualiza `Vehicle.odometer_km` y `Vehicle.fleet_status`, y modifica
indirectamente el conjunto de choferes candidatos de cada pedido.


### Parametrización

La cátedra exige que un proceso automatizado sea configurable desde el sistema.
Todos estos valores son editables por el administrador de la distribuidora:

| Parámetro | Qué controla |
|---|---|
| `cron_hour` | Hora de ejecución diaria del planificador |
| `lead_time_days` (por plan) | Anticipación con la que se empieza a planificar (ej. 60 días RTO, 15 aceite) |
| `interval_km` / `interval_months` (por plan) | Cada cuánto se repite la tarea |
| `criticality` (por plan) | `BLOCKING` (inhabilita el vehículo) vs `NON_BLOCKING` |
| `PROPOSAL_TTL_HOURS` | Vigencia de la propuesta de ventana enviada al chofer |
| `TOP_N_WINDOWS` | Cuántas ventanas alternativas se ofrecen antes de escalar |
| `MIN_VEHICLES_PER_ZONE` | Mínimo operativo por zona de cobertura |
| `MIN_SAMPLE_DAYS` | Días de historial exigidos antes de confiar en la predicción propia |
| `DECAY` | Peso relativo de las semanas recientes en la media móvil |
| `seasonal_factors` | Coeficiente por mes del ajuste estacional |


---

## 7. Encaje arquitectónico

Módulo `src/fleet/` con la misma estructura hexagonal que `order`:

```
src/fleet/
  domain/
    usage-predictor.service.ts        (puro)
    maintenance-scheduler.service.ts  (puro)
    vehicle-fitness.machine.ts        (máquina de estados)
    ports/
      fleet-availability.port.ts
      maintenance-notification.port.ts
  application/
    maintenance-planner.service.ts    (cron + orquestación)
  infrastructure/
    *.typeorm.repository.ts
    notification.adapter.ts
```

El predictor y el planificador son **funciones puras sobre datos**: testeables
sin base ni Redis. Eso sostiene la cobertura de tests unitarios que el proyecto
ya viene manteniendo.

**No se toca el núcleo transaccional** (`order` / `payments` / `cylinder`), que
la revisión de arquitectura del 2026-07-16 declaró de calidad de producción.

### Alcance del cambio

- `Car` → campos nuevos (migración TypeORM)
- `DispatchOrchestratorService` → un filtro adicional
- Panel admin → pantalla de Flota (vehículos, tareas, calendario)
- App chofer → carga de odómetro y aviso de vencimientos (opcional)

---

## 8. Riesgos y decisiones pendientes

1. **`Car` hoy pertenece a un chofer** (`user_id` → `User`, ManyToOne). Para
   flota real el vehículo pertenece a la **distribuidora** y se asigna por
   turno. Es una decisión de modelado a tomar antes de implementar; da material
   de análisis.

2. **El odómetro derivado de GPS acumula error.** El GPS mide distancia entre
   pings, no lo que marca el tablero. Mitigación: lectura manual periódica del
   chofer como **ancla**, GPS como interpolación entre anclas. Reconocer el
   error del modelo y acotarlo es un punto fuerte en la defensa.

3. **Arranque en frío.** Vehículo nuevo sin historial → promedio de la flota o
   del tipo de vehículo hasta juntar `MIN_SAMPLE_DAYS`.

4. **Ninguna ventana factible.** Si el vehículo no puede ir al taller sin dejar
   la zona bajo el mínimo, el sistema escala al administrador en vez de decidir
   solo. Es una decisión de diseño explícita, no un caso no contemplado.

---

## 9. Normativa a verificar

> ⚠️ **Pendiente de verificación contra fuentes oficiales.** Lo que sigue son
> categorías a confirmar, no normativa citada.

- **No usar "VTV"**: es la denominación bonaerense. En Misiones corresponde
  **RTO** (Revisión Técnica Obligatoria). Si el transporte es
  interjurisdiccional, el régimen aplicable es el de CNRT.
- El transporte de GLP envasado es **carga peligrosa**, lo que arrastra
  habilitaciones que un delivery común no tiene. Categorías a modelar:
  - RTO del vehículo
  - Seguro y póliza de carga peligrosa
  - Licencia habilitante del conductor
  - Habilitación del transportista para GLP
  - Revisión periódica de matafuegos

Es dominio real y específico del rubro: bien citado, es un diferencial fuerte
del trabajo.

---

## 10. Argumento para la defensa

> M1 y M2 son inteligentes en la **ejecución**: reaccionan a un evento del
> momento. Este módulo es inteligente en la **anticipación**: infiere el futuro
> a partir del historial que el propio sistema genera, y modifica hoy la
> planificación para que ese futuro no rompa la operación. Es el único de los
> tres que actúa antes de que el problema exista.

Y no es MVP: se pueden vender garrafas sin él. Ninguna app de delivery lo tiene,
porque es lo que separa un sistema de *delivery* de uno de *logística*.

**Alternativa si igual se objeta:** D1 del roadmap — agrupar pedidos por chofer
(batching) y ordenar el recorrido. Ya está identificado como el gap más grande
del producto y es un problema de optimización con peso académico propio.
