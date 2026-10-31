# Recupero de envases — módulo M5, envases no devueltos (CU-108, API v2)

El módulo detecta los **envases que un cliente retiene** más allá de la tolerancia, abre un **caso** por envase y le
avisa al cliente en **escalones** (primero un recordatorio, después el aviso de que el depósito está comprometido). Si el
cliente tiene una entrega ya programada, le **ofrece devolver el envase en ese viaje** y el chofer lo retira. Si la
secuencia se agota, el caso **escala al administrador** (depósito mayor que el umbral) o queda registrado como
**envase perdido**. El administrador decide con el legajo: cobrar el depósito, dar de baja el envase o cerrar sin cargo.
**El sistema nunca cobra solo.** En el panel: Catálogo y cobertura → «Recupero de envases» (`/physical-cylinders/recovery`).

**Viene apagado.** Hasta que el administrador ponga `enabled = 1` en los parámetros, el proceso no abre casos ni manda
avisos y «Correr ahora» responde **409**. Las consultas funcionan igual.

## Cómo decide

1. **Detección:** un envase `with_customer` cuya entrega (el último movimiento a `with_customer`) tiene `toleranceDays` o
   más, sin caso vivo y sin un caso ya resuelto para esa misma entrega. Si no se puede saber en poder de quién está (sin
   movimiento de entrega), no abre caso: va a **revisión manual** (se cuenta en la corrida y se lista en el reporte).
2. **Caso:** uno vivo por envase (índice único parcial en la base), con el depósito del producto (`depositAmount`). Antes
   de cada paso se relee el envase: si ya volvió, el caso se cierra.
3. **Escalones** (cada uno dura `escalationStepDays`; el aviso de cada escalón se registra una sola vez):

   | Escalón | Qué pasa |
   |---|---|
   | 1 | Recordatorio: «Devolvé tu envase». |
   | 2 | Aviso del depósito: «Tu depósito está comprometido», con la fecha límite y el importe. |
   | 3 | Secuencia agotada (no es un aviso): el caso escala o queda perdido. |

4. **Oferta de retiro:** mientras el caso está abierto, si el cliente tiene una entrega programada dentro de
   `pickupWindowDays`, se le ofrece devolver el envase en ese pedido, con vigencia `pickupOfferTtlHours` (una oferta viva
   por caso; cada pedido se ofrece una sola vez). Sin entrega programada, se saltea. Si acepta, el caso **espera** el
   retiro y no avanza. Si el chofer no lo retira, o el pedido termina sin retiro (cancelado, o entregado hace más de 24 h),
   la oferta se da por fallida y el caso vuelve a su escalón.
5. **Al agotarse:** depósito **estrictamente mayor** que `escalationAmountThreshold` → `escalated`, con aviso en la bandeja
   del administrador; si no → `lost`, que figura en el reporte. Los dos los puede decidir el administrador.
6. **Devolución:** cuando el envase pasa de `with_customer` a `empty_returned` (por el chofer, el depósito o el retiro
   confirmado), el caso vivo se cierra `returned` en el momento, sin esperar la corrida. La corrida también cierra los
   escalados y perdidos cuyo envase volvió o ya tiene otro cliente; uno dado de baja por otra vía se cierra sin cargo.
7. **Decisión del administrador** (sólo sobre `escalated` o `lost`, con una nota de 10 a 500 caracteres; queda quién
   decidió): `charge_deposit` registra el cobro del depósito (no genera ningún cargo: lo cobra una persona en el próximo
   pedido o en efectivo), `write_off` da de baja el envase (`with_customer → retired`, por la máquina de estados y en la
   misma transacción) y `close_no_charge` cierra sin cargo. Antes de decidir se relee el envase: si ya volvió o cambió de
   manos, el caso se cierra solo y la decisión responde 409.

## Parámetros (`cylinder_recovery`)

`GET|PATCH /cylinder-recovery/settings` (o `GET|PUT /module-config/cylinder_recovery`, ver `PROCESOS-AUTOMATICOS.md`);
en el panel, botón «Parámetros» de la pantalla. Validados en el DTO, con zod en el panel y con un CHECK en la base.

| Parámetro | Rango | Por omisión | Qué es |
|---|---|---|---|
| `enabled` | 0–1 | **0** | Interruptor del módulo: la corrida diaria y «Correr ahora». |
| `toleranceDays` | 1–365 días | 30 | Días desde la entrega antes de abrir un caso. |
| `escalationStepDays` | 1–90 días | 7 | Duración de cada escalón. |
| `escalationAmountThreshold` | 0–100.000.000 $ | 50.000 | Depósito por encima del cual el caso agotado escala al administrador. |
| `pickupOfferTtlHours` | 1–720 h | 72 | Vigencia de la oferta de retiro. |
| `pickupWindowDays` | 1–60 días | 7 | Ventana en que una entrega programada sirve para ofrecer el retiro. |
| `runHour` | 0–23 h | 10 | Hora de la corrida diaria (hora argentina). |

## Proceso automático

- Un cron cada hora (hora argentina) recorre las distribuidoras con envases afuera y corre la gestión en las que tienen
  `enabled = 1` y `runHour` igual a la hora actual; saltea las suspendidas o dadas de baja. Una vez por día.
- **Cerrojo en Redis** (`cron:cylinder-recovery`): con varias instancias corre una sola.
- **Idempotente:** un caso vivo por envase, un aviso por escalón y una oferta viva por caso; dos corridas seguidas no
  repiten nada (la segunda abre 0 casos y manda 0 avisos).
- **Tope de avisos:** el cliente recibe **un solo push por corrida** que resume todos sus envases y la oferta de retiro
  («Tenés N envases…»); el detalle de cada aviso sale por el socket. El aviso al administrador no se repite por caso.
- La corrida y sus avisos quedan auditados con la distribuidora (`AUDITORIA.md`).

## API (`/api/v2`)

Con `X-Distributor` (para el super admin, sin él **400**). Sin token, **401**; con otro rol, **403**
`Acceso denegado. Requiere rol: …`.

**Administrador** (`admin`, `super_admin`):

| Método | Ruta | Qué hace | Errores |
|---|---|---|---|
| GET | `/cylinder-recovery/cases?status&step&customerId&cylinderId&live&pending` | Casos con cliente, envase, días afuera, escalón, último aviso y oferta de retiro; `{ data, total, counts }` (`counts` por estado). `live=true`: abiertos, escalados y perdidos; `pending=true`: los que esperan la decisión (escalados y perdidos). | 400 estado inválido |
| GET | `/cylinder-recovery/cases/:id` | Legajo: el caso, sus avisos (`notices`), el historial del envase (`history`) y la resolución. | 404 |
| POST | `/cylinder-recovery/cases/:id/resolve` `{ decision, note }` | Decidir un caso escalado o perdido (`charge_deposit`, `write_off`, `close_no_charge`). | 400 nota fuera de 10–500; 404; 409 caso que no espera decisión, ya decidido o envase que volvió o cambió de manos |
| GET | `/cylinder-recovery/report` | Envases perdidos, escalados sin resolver y envases para revisión manual, con totales e importes. | — |
| GET | `/cylinder-recovery/settings` | Los parámetros con su esquema, rango, valor por omisión y valor vigente. | — |
| PATCH | `/cylinder-recovery/settings` | Cambia sólo los parámetros que vienen. | 400 fuera de rango |
| POST | `/cylinder-recovery/run` | Corre la gestión ahora; devuelve casos abiertos, avisos, ofertas, escalados, perdidos, devueltos y revisión manual. | 409 con el módulo apagado |

**Cliente** (`customer`, app del cliente):

| Método | Ruta | Qué hace | Errores |
|---|---|---|---|
| GET | `/cylinder-recovery/mine` | Mis envases pendientes de devolver (casos `open` y `escalated`), con escalón, depósito, días afuera y la oferta de retiro vigente (`pickup`). | — |
| POST | `/cylinder-recovery/mine/:id/pickup/accept` | «Lo devuelvo en la próxima entrega»: acepta la oferta. | 404 caso ajeno; 409 sin oferta pendiente, vencida o pedido que ya no admite el retiro |
| POST | `/cylinder-recovery/mine/:id/pickup/decline` | Rechaza la oferta; el caso sigue en su escalón. | 404; 409 sin oferta vigente |

**Chofer** (`delivery`, app del chofer):

| Método | Ruta | Qué hace | Errores |
|---|---|---|---|
| GET | `/cylinder-recovery/driver/pickups` | Retiros que el cliente aceptó en mis pedidos aceptados, en camino o entregados hace menos de 24 h: serie, producto, depósito y datos del cliente. | — |
| POST | `/cylinder-recovery/driver/pickups/:noticeId/confirm` | Retiré el envase: registra el retorno (`with_customer → empty_returned`) y cierra el caso `returned`. | 403 pedido que no está aceptado, en camino o entregado hace menos de 24 h; 404 pedido de otro chofer; 409 el cliente no aceptó o el caso ya cerró |
| POST | `/cylinder-recovery/driver/pickups/:noticeId/not-collected` `{ reason }` | No pude retirarlo: se descarta el retiro con el motivo y el caso vuelve a su escalón. | 403, 404 y 409 igual que `confirm` |

## Avisos

- **Socket** al cliente (namespace `/customers`): `cylinder-recovery:notice`
  `{ caseId, noticeId, kind (reminder | deposit_warning | pickup_offer), step, serial, depositAmount, expiresAt, orderId, scheduledDate, title, body }`.
- **Push** (FCM) al cliente, uno por corrida, con `data.type = CYLINDER_RECOVERY` (`kind`, `caseId` y `noticeId` del
  primero, y `count`). Sin token, no se manda.
- **Bandeja del administrador** (`BANDEJA-ADMIN.md`): `cylinder_recovery_escalated`, «Envase sin devolver para resolver»,
  con link al caso en el panel (`/physical-cylinders/recovery?case=…`).

## En el panel

Catálogo y cobertura → **Recupero de envases** (`/physical-cylinders/recovery`): pestañas «Casos» (con el legajo y la
decisión) y «Reporte de envases perdidos», y los botones «Parámetros» y «Correr ahora». La **ficha del cliente** muestra
sus envases en recupero.

## Estados del caso

| Estado | Cuándo |
|---|---|
| `open` | Abierto, avanzando por los escalones (o esperando un retiro acordado). |
| `returned` | El envase volvió. |
| `escalated` | Secuencia agotada con depósito mayor que el umbral: espera la decisión del administrador. |
| `lost` | Secuencia agotada con depósito igual o menor que el umbral: envase perdido, informado en el reporte. |
| `deposit_charged` | El administrador decidió cobrar el depósito. |
| `written_off` | El administrador dio de baja el envase. |
| `closed_no_charge` | Cerrado sin cargo (por el administrador, o porque el envase se dio de baja por otra vía). |

La oferta de retiro tiene su propio estado: `pending`, `accepted`, `rejected` o `expired`.

## Pendiente y diferencias con la especificación

- Cobrar el depósito no genera un cargo en la cuenta corriente ni un recargo del próximo pedido: sólo registra la
  decisión, el importe, la nota y quién decidió.
- Para dar de baja un envase perdido se sumó la transición `with_customer → retired` a la máquina de estados y al trigger
  de la base; sólo la usa la decisión `write_off` (las rutas de baja y transición del envase la siguen rechazando).
- Estado nuevo `lost`, que el administrador también puede decidir.
- Parámetros nuevos fuera de la especificación: `enabled`, `pickupWindowDays` y `runHour`. La granularidad es diaria.
- Un caso resuelto con el envase todavía afuera no se reabre mientras sea la misma entrega.
- El escalón 3 no es un aviso: es el estado de la secuencia terminada.
- El chofer puede confirmar el retiro hasta 24 h después de entregar el pedido.
- La descripción de `escalationAmountThreshold` dice «desde el cual», pero escala sólo un depósito **mayor** que el umbral.
- Falta: el aviso por socket al chofer cuando el cliente acepta un retiro (hoy lo ve al refrescar la lista), las
  pantallas de las apps y la colección de Postman. El avance por escalones, la oferta, el escalamiento y la decisión no se
  recorrieron todavía por HTTP en la demo (están cubiertos por tests de integración con reloj controlado).
