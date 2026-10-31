# Recompra anticipada — módulo M3 (CU-106, CU-145 y CU-146, API v2)

El módulo estima **cuándo se le acaba el gas** a cada cliente con lo que compró en la distribuidora y, unos días antes,
le manda una **invitación a reponer** con el pedido ya armado (lo de su última compra, su dirección, su franja y su medio
de pago habituales). El cliente la acepta con un toque y el pedido sale por el mismo camino que `POST /orders`, o la
descarta. El administrador ve a quién se le acaba el gas (CU-146), las invitaciones que salieron y cuántas terminan en
pedido. En el panel: Clientes → «Recompra» (`/customers/repurchase`) y la tarjeta de recompra en la ficha de cada cliente.

**Viene apagado.** Hasta que el administrador ponga `enabled = 1` en los parámetros, el proceso diario no invita a nadie,
el barrido de vencimientos no corre y «Correr ahora» responde **409**. La simulación (`dryRun`) y las consultas funcionan
igual.

## Cómo estima la fecha

Se calcula al vuelo, por cliente y **con las entregas de esa distribuidora** de los últimos 400 días (un cliente nunca
aparece para una distribuidora que no le entregó nada). La fecha no se guarda.

1. **Compras:** las entregadas, con los kilos de gas de cada una; dos compras del mismo día cuentan como una. Se usan las
   últimas 13 (o `minOrders`, si es mayor): el consumo de hace dos años no es el de hoy.
2. **Ritmo base:** para cada tramo entre dos compras, kilos ÷ días, con los días **ponderados por la estacionalidad**
   (un día de julio pesa 1,4 y uno de enero 0,7; los coeficientes por mes están fijos en el código). Los tramos cuyo ritmo
   se aleja más de tres veces de la mediana (vacaciones, compra doble) se descartan.
3. **Proyección:** desde la última entrega se consumen los kilos de esa compra día por día, al ritmo base corregido por
   la estacionalidad de cada día. El día en que se terminan es la fecha estimada (`source: history`).
4. **Respaldo:** sin `minOrders` compras, o con un historial irregular (no queda ningún tramo válido), se usa el consumo
   que declaró el cliente (`CARRITO-Y-CONSUMO.md`) desde su última compra (`source: declared`).
5. **Sin estimación:** sin compras (`no_purchases`), sin historia ni consumo declarado (`insufficient_history` o
   `irregular_history`), o con una fecha que ya pasó hace más de `staleDays` (`stale`: el cliente dejó de comprar).

**Cuándo se invita:** cuando la fecha estimada cae dentro de los días de aviso del cliente (hoy + días ≥ fecha; incluye a
los atrasados hasta `staleDays`). Los días de aviso son los del cliente (CU-145, de 1 a 30) o, si no eligió, los de la
distribuidora (`anticipationDays`). Un cliente que desactivó el aviso no recibe invitaciones.

**Cuándo no se invita** (cada motivo se cuenta en la respuesta de la corrida, `skipped`):

| Motivo | Cuándo |
|---|---|
| `notice_disabled` | El cliente desactivó el aviso. |
| `not_yet` | La fecha estimada todavía no entra en sus días de aviso. |
| `recent_order` | Tiene un pedido vigente o hecho en los últimos `recentOrderDays`. |
| `cooldown` | Tiene una invitación abierta, o la última se cerró hace menos de `minIntervalDays`. |
| `same_cycle` | Ya se lo invitó desde su última compra y todavía no pasó un ciclo estimado completo: una invitación por ciclo. |
| `no_stock` | Ningún producto de su compra habitual sigue en el catálogo o con stock. |
| `no_address` | No tiene una dirección para el pedido. |

## Parámetros (`repurchase`)

Se leen y guardan con `GET|PUT /module-config/repurchase` (CU-172, ver `PROCESOS-AUTOMATICOS.md`); en el panel, botón
«Parámetros» de la pantalla de Recompra. Validados en el esquema del proceso y con un CHECK en la base.

| Parámetro | Rango | Por omisión | Qué es |
|---|---|---|---|
| `enabled` | 0–1 | **0** | Interruptor del módulo: el proceso diario, el barrido y «Correr ahora». |
| `minOrders` | 2–50 | 3 | Compras mínimas para estimar con el historial. |
| `anticipationDays` | 1–30 días | 3 | Días de aviso de la distribuidora (los usa el cliente que no eligió los suyos). |
| `invitationTtlHours` | 1–168 h | 24 | Vigencia de la invitación. |
| `minIntervalDays` | 1–90 días | 7 | Intervalo mínimo antes de volver a invitar al mismo cliente. |
| `runHour` | 8–21 h | 9 | Hora de la corrida diaria (hora argentina; las invitaciones no salen de madrugada). |
| `recentOrderDays` | 1–30 días | 2 | Un cliente con un pedido en estos días no recibe invitación. |
| `staleDays` | 7–365 días | 30 | Pasados estos días de la fecha estimada sin comprar, se lo deja de proyectar. |

## Proceso automático

- **Corrida diaria:** un cron cada hora (hora argentina) recorre las distribuidoras **activas** con `enabled = 1` y corre
  la anticipación en la que tiene `runHour` igual a la hora actual. La corrida vence las invitaciones sin respuesta,
  estima, excluye y abre una invitación a cada cliente que corresponde.
- **Barrido cada 5 minutos:** vence las invitaciones cuya vigencia terminó (en las distribuidoras encendidas), cierra
  (`cancelled`) las de un cliente que hizo un pedido por su cuenta y las de distribuidoras que ya no están activas.
- **Cerrojo en Redis** en los dos (`cron:repurchase` y `cron:repurchase-expiry`): con varias instancias corre una sola.
- **Idempotente y con tope:** a lo sumo **una invitación abierta por cliente y distribuidora** (índice único parcial en la
  base), una por ciclo y nunca antes de `minIntervalDays`; repetir la corrida no invita dos veces. Toda transición es un
  `UPDATE` condicionado a `pending`, así que aceptar, descartar y vencer no se pisan. Aceptar y descartar comparten un
  cerrojo por invitación; si el pedido se creó y falló el registro de la aceptación, el reintento la reconoce y no crea
  otro pedido.
- **El pedido sale al precio de hoy.** La invitación guarda los renglones y la dirección; al aceptar, se valida contra el
  catálogo, el stock y la cobertura del momento.

## API (`/api/v2`)

Con `X-Distributor` (obligatorio en `GET /customers/me/repurchase` y para el super admin; sin él, **400**). Sin token,
**401**; con otro rol, **403** `Acceso denegado. Requiere rol: …`.

**Administrador** (`admin`, `super_admin`):

| Método | Ruta | Qué hace | Errores |
|---|---|---|---|
| GET | `/repurchase/forecast?days&limit&offset` | Clientes a los que se les acaba el gas dentro de `days` (1–90, por omisión 14), los atrasados primero; cada uno con fecha, `daysLeft`, `source`, compras usadas, kg por mes estimados, aviso e invitación abierta. Devuelve `{ data, total, days, generatedAt }`. | 400 fuera de rango |
| GET | `/repurchase/forecast/customers/:userId` | La estimación de un cliente: `{ forecast, reason }` (`forecast: null` con el motivo si no hay). | 404 si no es cliente de la distribuidora |
| GET | `/repurchase/invitations?status&userId&from&to&limit&offset` | Invitaciones emitidas, la más nueva primero: `{ data, total }`. | 400 estado inválido o período al revés |
| GET | `/repurchase/stats?from&to` | Del período (por omisión 90 días): enviadas, por estado, `conversionRate` = aceptadas ÷ (aceptadas + descartadas + vencidas) o `null`, y `acceptedRevenue` (sin pedidos cancelados). | 400 `from no puede ser posterior a to` |
| POST | `/repurchase/run` `{ dryRun? }` | Corre la anticipación ahora. Con `dryRun: true` sólo calcula a quién invitaría (`candidates`), sin escribir ni avisar. Devuelve `evaluated`, `invited`, `expired`, `skipped`. | 409 con el módulo apagado (salvo `dryRun`) |

**Cliente** (`customer`, app del cliente):

| Método | Ruta | Qué hace | Errores |
|---|---|---|---|
| GET | `/customers/me/repurchase` | Mi fecha estimada en la distribuidora del header: `{ estimatedAt, daysLeft, source, reason, notice, openInvitation }`. | 400 sin `X-Distributor` |
| GET | `/customers/me/repurchase/notice` | Mi aviso (CU-145): `{ enabled, days, distributorDays, effectiveDays }` (`days: null` = rige el de la distribuidora). | — |
| PATCH | `/customers/me/repurchase/notice` `{ enabled?, days? }` | Cambiarlo: `days` de 1 a 30 o `null`; al menos un campo. | 400 |
| GET | `/customers/me/repurchase/invitations[?all=true]` | Mis invitaciones abiertas y vigentes; con `all=true`, también las resueltas (hasta 50). Cada una con renglones a precio de hoy (`available`), `estimatedTotal` (lista, sin promociones ni recargos), dirección, franja y medio de pago. | — |
| GET | `/customers/me/repurchase/invitations/:id` | Una. | 404 si es de otro cliente |
| POST | `/customers/me/repurchase/invitations/:id/accept` `{ paymentMethod?, timeSlotId?, scheduledDate?, notes? }` | **Crea el pedido** (201 `{ invitation, order }`, `order` con `paymentUrl` si es Mercado Pago). Medios: efectivo, transferencia o Mercado Pago (nunca cuenta corriente). `timeSlotId` y `scheduledDate` van juntos; sin ellos usa la franja de la invitación si sigue activa, o entrega inmediata. Acepta `Idempotency-Key`. | 400 franja sin fecha, sin stock, fuera de cobertura u otra regla del pedido (la invitación sigue abierta); 404 ajena; 409 ya aceptada, descartada, vencida, cerrada o distribuidora no disponible |
| POST | `/customers/me/repurchase/invitations/:id/dismiss` | Descartarla. | 404 ajena; 409 ya no está abierta |

## Avisos

- **Socket** (namespace `/customers`, sala del cliente): `repurchase:invitation`
  `{ invitationId, distributorId, projectedDepletionAt, expiresAt }` y `repurchase:invitation-closed`
  `{ invitationId, reason: expired | cancelled }`.
- **Push** (FCM): «¿Reponés tu garrafa?», con `data { event: REPURCHASE_INVITATION, invitationId, distributorId }`. A un
  atrasado le dice «Ya te tocaría reponer…», sin fecha pasada. Sin token, no se manda; no hay mail.
- El administrador no recibe avisos en la bandeja: lo ve en la pantalla de Recompra.

## En el panel

Clientes → **Recompra** (`/customers/repurchase`): tarjetas de los últimos 90 días (invitaciones, aceptadas, conversión,
vendido por invitación), pestañas «Próximas recompras» e «Invitaciones», y los botones «Parámetros», «Simular» (`dryRun`)
y «Correr ahora». La **ficha del cliente** muestra su fecha estimada y su tarjeta de recompra.

## Estados de la invitación

| Estado | Cuándo |
|---|---|
| `pending` | Abierta, dentro de su vigencia. |
| `accepted` | El cliente la aceptó; queda ligada al pedido (`orderId`). |
| `rejected` | El cliente la descartó. |
| `expired` | Venció sin respuesta (la cierra el barrido). |
| `cancelled` | Se cerró sin efecto: el cliente pidió por su cuenta o la distribuidora dejó de estar activa. No cuenta para la conversión. |

## Pendiente y diferencias con la especificación

- Los coeficientes de estacionalidad están fijos en el código, no son configuración por mes; no están calibrados con datos
  reales.
- La fecha estimada no se guarda: se calcula al vuelo (CU-146 habla de una lectura por rango).
- Estado nuevo `cancelled`, que la especificación no tiene.
- CU-145 se resuelve con dos datos por cliente: activar o desactivar el aviso, y sus días (o los de la distribuidora).
- Parámetros nuevos fuera de la especificación: `enabled`, `recentOrderDays` y `staleDays`; `runHour` sólo de 8 a 21.
- La invitación guarda también la franja y el medio de pago; la franja no trae fecha.
- Extras: estadísticas, simulación (`dryRun`) y avisos por socket y push.
- Los parámetros siguen en la ruta de la v1 (`/module-config/repurchase`); no hay `GET|PATCH /repurchase/settings` como
  en el planificador de flota.
- Falta: la colección de Postman y las pantallas de la app del cliente.
