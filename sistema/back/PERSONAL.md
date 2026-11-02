# Personal: documentación, asistencia, licencias, tablero y habilitación laboral

Iteración C-08 (segunda tanda). Lo ya construido de personal (puestos, legajos,
egreso, reingreso, cuenta de acceso, adjuntos) está en `src/employee/`; esto
suma lo que cuelga del legajo. Casos de uso: CU-183 a CU-185, CU-187 a CU-194,
CU-246 y CU-313 a CU-319.

Todos los endpoints son de `admin` / `super_admin` (con distribuidora en
contexto: `X-Distributor` para el super admin) salvo las dos marcas del chofer.
Lo de otra distribuidora responde **404**, no 403.

## Módulos

| Módulo | Qué tiene |
|---|---|
| `fleet/` (existente) | Los planes y tareas son la misma tabla de siempre; el dueño de la tarea puede ser un **empleado**. `EmployeeDocumentsService` arma la ficha de documentación. El aviso diario (`FleetAlertsCron`) y el gate del despacho (`FleetDispatchLockService`) incluyen al personal. |
| `attendance/` | Jornadas (`employee_attendance`), grilla, marcas del chofer y el aviso de las 7 (`AttendanceOpenAlertCron`). |
| `leave/` | Licencias (`employee_leave`), máquina de estados (`domain/leave-state.ts`) y saldo de vacaciones (`domain/vacaciones.ts`). |
| `personnel/` | Tablero (modelo de lectura sobre los servicios de los anteriores). |

Migración: `1792080000000-DocumentacionAsistenciaYLicenciasDelPersonal.ts`
(esquema generado con `schema:log` contra una base vacía, más la siembra de
planes, el backfill del tipo de documento y el trigger de superposición).
Probada en `test/integration/personal-documentacion-migracion.e2e-spec.ts`.

## Documentación del personal (CU-183, CU-184, CU-185, CU-187)

Un empleado tiene documentación por la **misma tabla de tareas de flota**
(`maintenance_task`), con el sujeto `employee` en el plan.

Planes base nuevos (se siembran con la distribuidora, y por migración para las
existentes; `fleet/domain/base-plans.ts` y la migración tienen los mismos
valores):

| Plan | `documentKind` | Anticipación | Bloquea | Aplica a |
|---|---|---|---|---|
| Curso de transporte de mercancías peligrosas (GLP) | `hazmat_driver_course` | 60 días | sí | `driver` |
| Examen psicofísico | `psychophysical` | 30 días | sí | `driver` |
| Alta en ART | `art_coverage` | 30 días | no | todas |

`maintenance_plan` suma `document_kind` (qué formulario muestra el panel y qué
`details` valida el back) y `applies_to_categories` (`null` = todas;
`varchar[]` con valores de `JobPositionCategory`). `maintenance_task` suma
`employee_id` (FK a `employee`, `ON DELETE CASCADE`) y `details` (jsonb).

### Cargar el documento: `POST /fleet/tasks`

Es la operación genérica de CU-136 a CU-138, ahora con `employeeId`. Idempotente
(`Idempotency-Key`).

```json
{
  "planId": "…",
  "employeeId": "…",
  "dueAt": "2027-05-10T00:00:00.000Z",
  "details": { "certificateNumber": "123/26", "issuer": "CNRT" }
}
```

`details` según `plan.documentKind` (todos los campos obligatorios, sin otras
claves, texto recortado):

| `documentKind` | `details` |
|---|---|
| `hazmat_driver_course` | `certificateNumber` (≤ 40), `issuer` (≤ 80) |
| `psychophysical` | `examDate` (`YYYY-MM-DD` real) |
| `art_coverage` | `insurer` (≤ 80), `policyNumber` (≤ 40) |
| el resto (seguro, VTV, licencia, service, genérico, sin tipo) | no lleva detalle |

`dueAt` es obligatorio en un plan de personal por fecha fija; se normaliza a
medianoche UTC de su fecha calendario. Un plan con `subject=employee` pide
`employeeId` y no acepta `carId` ni `deliveryId` (y al revés).

Errores:

| Código | Cuándo |
|---|---|
| 400 | `details` con otra forma (el mensaje nombra `detalle.<campo>`), falta `dueAt`, plan inactivo, el plan no aplica a la categoría del puesto del empleado, sujeto que no coincide con el plan |
| 404 | plan o empleado inexistente o de otra distribuidora |
| 409 | el empleado está egresado |

`PATCH /fleet/tasks/:id` corrige el `details` de una tarea abierta (se valida contra el
tipo del plan); el dueño (`employeeId`) no se edita: si cambia, se cancela y se carga otra.

Renovar = cargar la nueva y cerrar la anterior (`PATCH /fleet/tasks/:id/close`). Editar,
cerrar, cancelar y adjuntar usan las operaciones existentes de `fleet/tasks`
(`GET /fleet/tasks?employeeId=` filtra por empleado). `FleetTaskResponseDto`
suma `employeeId` y `details`; `FleetPlanResponseDto` suma `documentKind` y
`appliesToCategories` (`POST/PATCH /fleet/plans` los aceptan).

### `GET /employees/:id/documents`

`{ employeeId, isLocked, lockReasons[], tasks[], missingPlans[] }`. `tasks` incluye las del
legajo **y la licencia de conducir** del perfil de reparto del mismo chofer (esa
sigue colgando de `delivery_id`). `missingPlans` son los planes activos que le
aplican por la categoría de su puesto y para los que no tiene ninguna tarea
abierta. `isLocked` y `lockReasons` usan la MISMA regla que el despacho (CU-246),
salvo el vehículo en uso: legajo egresado, licencia aprobada que cubre hoy y
documentación bloqueante vencida (incluida la licencia de conducir).

### `GET /fleet/expirations`

Nuevos parámetros: `subject=vehicle|employee` (acota qué trae) y
`category=<JobPositionCategory>` (filtra el personal por categoría de puesto).
La respuesta suma `employees[]`: `{ employeeId, fullName, fileNumber,
positionName, category, isLocked, items[] }`, de la más urgente a la menos. Las
tareas sin fecha límite no entran. `employees[]` incluye la licencia de conducir
de los choferes (también sigue saliendo en `drivers[]`, sin cambios).

## Aviso diario (CU-188)

`FleetAlertsCron` (cada hora, a la hora que cada distribuidora configuró con
`fleetAlertHour`) ahora también junta las tareas de empleados, que el correo
nombra («Empleado Ana Pérez»). Además lista a los **choferes activos a los que
les falta un documento bloqueante** (planes bloqueantes que les aplican y no
tienen cargados, incluida la licencia): esos **no se marcan como avisados**, se
repiten cada día hasta que se carguen. Sigue valiendo: si falla el envío no se
marca `alertedAt`; si no hay administradores con correo, se marca igual.

## Asistencia (CU-189, CU-313, CU-314, CU-190, CU-315)

| Método | Ruta | Quién | Qué |
|---|---|---|---|
| POST | `/employees/:id/attendance` | admin | CU-189. `{ checkInAt, checkOutAt? }`. Idempotente. 201 |
| PATCH | `/attendance/:id` | admin | CU-313. `{ checkInAt?, checkOutAt?, notes }`. 200 |
| GET | `/attendance?date&from&to&employeeId&open&page&limit` | admin | CU-314. `{ data, total, presentToday, staleOpen }` |
| POST | `/attendance/mine/check-in` | chofer | CU-190. Idempotente: 201 al abrir, 200 si ya tenía una abierta de hoy desde la app |
| POST | `/attendance/mine/check-out` | chofer | CU-315. 200; 409 si la abierta es de un día anterior |
| GET | `/attendance/mine/current` | chofer | La jornada abierta (también la de un día anterior sin cerrar). 200, o 204 si no tiene ninguna o su cuenta no está vinculada a un legajo |

Reglas: una sola jornada abierta por empleado (índice único parcial
`UQ_employee_attendance_abierta` + lock del legajo); la carga del panel sólo
exige «sin jornada abierta» si no trae egreso, y en todos los casos se rechaza
(409) una jornada que se superpone con otra del mismo empleado (también al
corregir); no se admiten ingresos ni egresos futuros (400, con un minuto de
tolerancia de reloj); el egreso es estrictamente posterior al ingreso; `workDate` es el día argentino del ingreso; origen `panel`
o `driver_app`. La corrección exige `notes` (400 sin ella) y las notas se
acumulan. `GET /attendance` sin ningún filtro trae el día de hoy;
`presentToday` y `staleOpen` (jornadas de días anteriores sin cerrar) no
dependen de los filtros. Fechas inválidas → 400.

Errores: 400 egreso no posterior / nota faltante / filtro inválido; 404
empleado o jornada de otra distribuidora; 409 empleado egresado o jornada
abierta o superposición (alta y corrección del panel) / cuenta sin legajo
activo, legajo egresado, abierta de otro día o cargada desde el panel, o
ninguna abierta (marcas del chofer).

**Aviso de las 7** (`AttendanceOpenAlertCron`, hora argentina): todas las jornadas
de días anteriores que siguen abiertas (no sólo la de ayer), por correo a los
administradores de cada distribuidora. No las cierra.

### Contrato para la app del chofer (tanda posterior)

La app no está tocada en esta tanda. Lo que tiene que consumir:

```
POST /attendance/mine/check-in    headers: Authorization, X-Client-Source: driver-app
  201 (abrió) / 200 (ya tenía una abierta de hoy desde la app: la devuelve) → AttendanceResponseDto { attendanceId, employeeId, employeeName, employeeFileNumber,
        workDate, checkInAt, checkOutAt: null, isOpen: true, durationMinutes: null,
        source: "driver_app", recordedByUserId, notes }
  409 → la cuenta no está vinculada a un legajo activo / hay una abierta de otro día o cargada
        desde el panel (se corrige desde el panel)
POST /attendance/mine/check-out
  200 → el mismo DTO con checkOutAt, isOpen=false y durationMinutes
  409 → sin legajo activo / no hay jornada abierta / la abierta es de un día anterior
        («corregila desde el panel»: no se cierra con la hora de hoy)
```

Sin cuerpo: el instante es el del servidor. La marca no condiciona la
disponibilidad para el despacho (ponerse en línea es independiente). Hacen falta
dos pantallas nuevas («Iniciar jornada» / «Finalizar jornada»).

## Licencias y ausencias (CU-191, CU-192, CU-193, CU-316 a CU-319)

| Método | Ruta | Qué |
|---|---|---|
| POST | `/employees/:id/leaves` | CU-191. `{ type, startDate, endDate, reason? }`. Nace `requested`. Idempotente. 201 |
| GET | `/leaves?status&type&employeeId&from&to&page&limit` | CU-319. `{ data, total }` (la bandeja de pendientes es `status=requested`) |
| PATCH | `/leaves/:id` | CU-316. Sólo `requested`: `type`, `startDate`, `endDate`, `reason` |
| PATCH | `/leaves/:id/approve` | CU-192. Asienta `decidedByUserId` y `decidedAt` |
| PATCH | `/leaves/:id/reject` | CU-318. `{ reason }` obligatorio (se guarda en `rejectionReason`) |
| PATCH | `/leaves/:id/cancel` | CU-317. Solicitada o aprobada que todavía no terminó |
| GET | `/employees/:id/vacation-balance?year` | CU-193 |

Tipos: `vacation`, `sick`, `work_accident`, `study`, `marriage`, `birth`,
`bereavement`, `unpaid`, `suspension`, `unjustified_absence`, `other`.

Estados (`domain/leave-state.ts`): `requested` → `approved` | `rejected` |
`cancelled`; `approved` → `cancelled`. `rejected` y `cancelled` son finales.
«Terminada» no es un estado: es `endDate` anterior a hoy (día argentino) y
impide cancelar. Una aprobada no se modifica: se cancela y se carga otra.

Superposición: dos licencias `requested`/`approved` del mismo empleado no se
pisan (extremos incluidos). Lo garantizan, en capas: el servicio bajo el lock
del legajo (`FOR UPDATE`) y el trigger `employee_leave_no_overlap`, que toma un
lock de aviso por empleado y lanza `23P01` (traducido a 409). Las rechazadas y
canceladas liberan el período. El 409 nombra la licencia que pisa.

Errores: 400 fin anterior al inicio / motivo faltante al rechazar / filtro o año
inválido; 404 empleado o licencia de otra distribuidora; 409 empleado egresado,
superposición, estado que no admite la operación, cancelar una terminada.

**Saldo de vacaciones**: `{ employeeId, year, entitledDays, takenDays,
balanceDays }`. Corresponden 14, 21, 28 o 35 días corridos según la antigüedad
al 31/12 del año (LCT art. 150: hasta 5 años, 14; más de 5 y hasta 10, 21; más
de 10 y hasta 20, 28; más de 20, 35; «excede» es estricto: con exactamente 5
años corresponden 14); los tomados son los días de las licencias `vacation`
aprobadas que caen en el año. Sin año, el actual. Es una referencia: no
considera licencias sin goce, ausencias ni el proporcional de quien ingresó en
el año. Se calcula en cada consulta, no se guarda.

## Tablero (CU-194): `GET /personnel/dashboard`

`{ today, totalActive, activeByPosition[], presentToday, onLeaveToday,
documents: { current, dueSoon, expired } }`. Cuenta, no lista. `presentToday`:
empleados con una jornada abierta de hoy (la misma cifra que `presentToday` de
`GET /attendance`; las abiertas de días anteriores no cuentan); `onLeaveToday`: con una licencia aprobada que
cubre hoy (día argentino); `documents`: tareas abiertas con fecha límite de
empleados activos y licencias de choferes, por estado de vencimiento. Sin
empleados, todo en cero.

## Habilitación laboral del chofer (CU-246)

`FleetDispatchLockService` (el gate único que usan la asignación manual, la
oferta automática y la aceptación del chofer) suma, además de lo de siempre
(licencia, vehículo en uso y sus documentos), tres motivos laborales:

- el legajo está egresado → «su legajo está egresado»;
- una licencia aprobada cubre hoy (día argentino) → «tiene una licencia aprobada
  que cubre el día de hoy»;
- una tarea bloqueante vencida de su **legajo** (cualquier plan de personal, no
  sólo la licencia) → «<plan>: venció el dd/mm/aaaa».

Sigue siendo una consulta en lote (cinco consultas sin importar cuántos
candidatos). Un chofer sin legajo conserva el comportamiento anterior. Probado
con cincuenta candidatos en `personal-documentacion.e2e-spec.ts`.

## Integración con el legajo

- `DELETE /employees/:id` (alta errónea) responde 409 si el legajo tiene
  jornadas, licencias o documentación: cada módulo registra su regla en
  `EmployeeRulesRegistry.alDarDeBaja`.
- `EmployeeService` suma las consultas de apoyo `findActivo` (404 / 409, con lock
  opcional), `findByUserIds`, `findByUserId`, `findActivos`, `findByIds`,
  `contarActivosPorPuesto` y `distribuidorasConChoferesActivos`.

## Egreso del chofer con una rendición pendiente (CU-181)

El egreso de un chofer (`POST /employees/:id/termination`) y su baja de usuario
(`DELETE /users/:id`, `DELETE /delivery/:id`; CU-085, CU-097) se rechazan con
**409** si le falta rendir. La regla la registra el módulo de rendiciones
(`driver-settlement/application/egreso-del-chofer.rule.ts`) en
`EmployeeRulesRegistry.alEgresar`.

**Qué cuenta como pendiente** (`pendienteDeRendir`, en este orden; la primera
que se cumple decide el mensaje):

1. Una rendición del chofer, **de cualquier día**, en un estado de
   `ESTADOS_SIN_CERRAR` (`open` o `submitted`; está en `driver-settlement.enums.ts`).
   El tablero financiero usa la misma constante para contar las rendiciones
   vencidas (`resumenDelDia`). Una `approved` no impide nada.
2. Si no tiene ninguna, efectivo que entregó y ninguna rendición tomó:
   `pedidosSinRendir` con el día de hoy (pedidos `delivered`, pago en efectivo
   `paid` o `pending`, sin `payment_resolved_by`, no incluidos en una
   rendición). Es la regla que usa la propia rendición.

El chofer se busca con `DeliveryService.findByUserIdEnTransaccion`, igual que el
caso de uso del egreso, pero **con las bajas** (`conBajas`): la baja del usuario
borra lógicamente el perfil de chofer antes de egresar el legajo.

Corre dentro de la transacción, con el chofer ya bloqueado, después de validar el
estado del legajo y los pedidos en curso y antes de tocar nada. La regla lanza el
409 ella misma (en vez de sumar un motivo a la lista genérica, que lo envolvería
en `No se puede registrar el egreso: …`) y la transacción se revierte. No se
aplica a `DELETE /employees/:id` (alta errónea).

Mensajes:

- Rendición sin cerrar: `No se puede dar de baja al chofer mientras tenga una rendición pendiente (rendición N° 26, abierta, del 02/11/2026): cerrala antes` (`presentada` si está en `submitted`).
- Sólo efectivo sin rendir: `No se puede dar de baja al chofer mientras tenga efectivo sin rendir (2 pedido(s) en efectivo por $ 7.500,50): generá y aprobá su rendición antes`.
- Ningún chofer da de baja su propia cuenta: `DELETE /users/me` es sólo del cliente y a un chofer le responde 403, así que la regla la dispara siempre un administrador.

### Matriz de `POST /employees/:id/termination`

«API» = probado contra el back del worktree (PORT=3010, `splg_db`) con un chofer de
prueba creado por `POST /users`. «Test» = sólo con test automático.

| Caso | Código | Prueba |
|---|---|---|
| Egreso correcto (chofer sin nada pendiente, rendición aprobada) | 200 | API + e2e |
| Reintento con la misma `Idempotency-Key` y el mismo body | 200, misma respuesta | API |
| Motivo no admitido; fecha que no es real; egreso anterior al ingreso | 400 | API + e2e / use-case spec |
| `:id` que no es UUID | 400 | API + e2e |
| `Idempotency-Key` que no es un UUID v4 | 400 | API |
| Sin token | 401 | API + e2e |
| `X-Client-Source` ausente o de una app a la que el rol no entra (chofer en `panel-app`) | 401 | API + e2e |
| Rol chofer en la app de reparto | 403 | API + e2e |
| Empleado inexistente o de otra distribuidora | 404 | API + e2e |
| Ya egresado | 409 | API + e2e |
| Rendición abierta o presentada | 409 | API + e2e + integración del SQL |
| Efectivo entregado sin rendir (sin rendición) | 409 | Test (unitario + integración del SQL): no se pudo armar por la API sin despachar un pedido real |
| Pedidos en curso | 409 | Test (use-case spec + e2e) |
| Carga de camión abierta | 409 | Test (`vehicle-assignment`) |
| `Idempotency-Key` repetida mientras la primera sigue en curso | 409 | API (dos pedidos en paralelo) |
| La cuenta del empleado cambió mientras se tomaban los locks | 409 | Test (use-case spec) |
| `Idempotency-Key` reusada con otro body | 422 | API |

`DELETE /users/:id` y `DELETE /delivery/:id` con una rendición abierta: 409 con el mismo
mensaje, sin cambios (API); el e2e cubre `DELETE /users/:id`. Con la rendición aprobada,
`DELETE /delivery/:id` responde 200 (API).

## Decisiones y desvíos del diseño original

Ver la entrega de la tanda (`.orq/ENTREGA.md`). Resumen: el tablero está en
`/personnel/dashboard` (no `/employees/dashboard`, que choca con `:id`); la
licencia de conducir del chofer sigue colgando de `delivery_id` (no se migró a
`employee_id`) y el gate, la ficha y el tablero la unen con el legajo; la
exclusión de superposición es un trigger y no un `EXCLUDE USING gist` (que
necesita `btree_gist` y una extensión en el esquema de prueba).

## Datos personales y auditoría

El `details` de la documentación (resultado del psicofísico, póliza de la ART,
certificados) no se guarda en la auditoría de requests (`depurarCambios`), ni en
la auditoría de datos (`MaintenanceTask.details` excluido), ni en el log de
requests (`morgan`). Los correos escapan el HTML de los nombres.
