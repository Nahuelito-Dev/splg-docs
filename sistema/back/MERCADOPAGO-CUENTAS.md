# Cuenta de Mercado Pago por distribuidora (API v2)

Cada distribuidora puede cobrar con **su propia cuenta de Mercado Pago**. Si no cargó ninguna, se
cobra con la cuenta del sistema (las variables `MP_ACCESS_TOKEN` y `MP_WEBHOOK_SECRET` del entorno),
como hasta ahora.

## Endpoints

Rol `admin` de la distribuidora o `superadmin` con `X-Distributor`.

| Método | Ruta | Qué hace |
|---|---|---|
| `GET` | `/api/v2/distributor/mercadopago-credentials` | Estado: `source` (`own` o `system`), `active`, `encryptionConfigured`, los tres valores **enmascarados**, `verifiedAt` y `accountType` (`test`, `real` o `unknown`: según `GET /users/me` de Mercado Pago, etiqueta `test_user` o nickname `TESTUSER…`; el panel lo muestra como «Cuenta de prueba» / «Cuenta real») |
| `PUT` | `/api/v2/distributor/mercadopago-credentials` | Carga o reemplaza la cuenta (`accessToken`, `publicKey`, `webhookSecret`). Antes de guardar verifica el token contra Mercado Pago |
| `PUT` | `/api/v2/distributor/mercadopago-credentials/deactivate` | Baja lógica: la distribuidora vuelve a cobrar con la cuenta del sistema |

Errores: `400` cuerpo inválido · `404` desactivar sin cuenta propia · `409` dos cargas simultáneas ·
`422` Mercado Pago rechazó el token · `502` Mercado Pago no respondió · `503` el servidor no tiene la
clave de cifrado. En `422` y `502` no se guarda nada.

Panel: **Configuración → Mercado Pago**. Los campos son de tipo contraseña, nunca se precargan y sólo
se muestra el valor enmascarado.

## Cómo se guardan

- Tabla `distributor_mercadopago_credentials`. Los tres valores se guardan **cifrados con AES-256-GCM**
  (IV aleatorio por valor y tag de autenticación). La clave está en `CREDENTIALS_ENCRYPTION_KEY`
  (32 bytes en base64: `openssl rand -base64 32`). Sin la variable no se pueden cargar cuentas y todo
  cobra con la del sistema.
- Reemplazar crea una fila nueva y desactiva la anterior, en una transacción. Una sola activa por
  distribuidora (índice único parcial `WHERE active`).
- Ni la auditoría por triggers (columnas cifradas fuera del mapa) ni la auditoría HTTP (`webhookSecret`
  y `accessToken` depurados) guardan los valores en claro.
- Si se cambia la clave de cifrado, las cuentas guardadas no se pueden leer: hay que volver a cargarlas.

## Qué cuenta usa cada operación

Cada pago (`payment.credential_id`) guarda **con qué cuenta se cobró** (null = la del sistema). La
consulta del pago, el webhook, la comisión y la devolución usan siempre esa cuenta, aunque después la
distribuidora la haya reemplazado o desactivado. El checkout nuevo usa la cuenta activa.

El webhook es el mismo `POST /api/webhook/mercadopago`. Con cuenta propia, la `notification_url` lleva
`?account=<id de la cuenta>`: la firma se valida con el secreto de esa cuenta y el pago se consulta con
su token. Antes de escribir, dentro de la transacción, se compara esa cuenta con la del intento de cobro
del pedido: si no coinciden (otra distribuidora, la cuenta del sistema contra un cobro con cuenta propia,
o una cuenta propia sin intento de cobro), el aviso se registra y se descarta sin tocar el pedido.

La conciliación (`FINANZAS.md`) pide los reportes con la cuenta vigente de la distribuidora; si no se
puede leer, la corrida termina `failed` con el motivo.

## Alta de una distribuidora: la URL de webhooks del panel de Mercado Pago

La `notification_url` que el back manda en cada checkout ya trae lo necesario. Pero la URL que se carga **a mano en el
panel de Mercado Pago** (Tus integraciones → Webhooks) tiene que llevar el mismo parámetro de cuenta:

- cuenta propia: `https://<dominio>/api/webhook/mercadopago?account=<credentialId>` (el `credentialId` es el de la
  cuenta cargada en el panel de SPLG); sin él, la firma se valida con el secreto del sistema y el aviso se descarta;
- cuenta del sistema: la misma URL sin `account`.

En el panel de Mercado Pago hay que activar los tópicos **Pagos**, **Contracargos** y **Alertas de fraude**
(`stop_delivery_op_wh`). Si se carga la URL en las notificaciones de la preferencia no hace falta: el back agrega
`source_news=webhooks` para que Mercado Pago no mande además el aviso IPN (https://www.mercadopago.com.ar/developers/es/docs/your-integrations/notifications/ipn).

## Estados del pago de Mercado Pago (ledger `payment`)

El ledger guarda **los nueve estados de la API de pagos de Mercado Pago**
(https://www.mercadopago.com.ar/developers/en/docs/checkout-api-payments/response-handling/query-results), con el mismo
nombre que informa la pasarela: `pending`, `in_process`, `authorized`, `approved`, `rejected`, `cancelled`, `refunded`,
`charged_back`, `in_mediation`. Además de `status`, cada pago guarda:

- `status_detail`: el motivo que informó la pasarela (`accredited`, `cc_rejected_insufficient_amount`,
  `pending_waiting_payment`…);
- `status_history` (jsonb, sólo se agrega): cada lectura del estado con `status`, `statusDetail`, `at`, `origin`
  (`webhook`, `conciliacion`, `consulta` o `reintegro` si lo hizo el propio sistema) y `applied` (`false` = el aviso llegó fuera de
  orden y no cambió el pago). Un mismo aviso repetido no ensucia el historial. Un trigger de la base
  (`TRG_payment_historial_solo_crece`) impide quitar o reescribir entradas.

### Transiciones (`puedeTransicionarElPago`)

Un aviso fuera de secuencia no retrocede un pago: queda en el historial con `applied: false`.

| Desde | Puede pasar a |
|---|---|
| `pending` | cualquiera (es lo primero que se ve de un pago) |
| `in_process` / `authorized` | `in_process`, `authorized`, `approved`, `rejected`, `cancelled` |
| `approved` | `in_mediation`, `refunded`, `charged_back` |
| `in_mediation` | `approved`, `refunded`, `charged_back` (el reclamo se resuelve) |
| `rejected`, `cancelled`, `refunded`, `charged_back` | finales |

Un `approved` después de `refunded` o `charged_back` no se aplica. La misma regla vive en la base
(`payment_estado_no_retrocede`), como segunda barrera.

### Qué hace el sistema con cada estado

| Estado de MP | Pago (ledger) | Pedido | Aviso al admin |
|---|---|---|---|
| `pending` | queda `pending` con su motivo | espera; **no se cancela por vencimiento** si hay un pago en curso | – |
| `in_process` | `in_process` | espera (no se cancela por vencimiento) | – |
| `authorized` | `authorized` | espera | – |
| `approved` | `approved`, ingreso a la caja de Mercado Pago | pasa a pagado y se despacha (si el importe coincide; si no, queda sin despachar y la conciliación avisa) | – |
| `rejected` / `cancelled` | con su motivo (`cc_rejected_*`…) | el pago del pedido queda `failed`; sigue vivo y el cliente **reintenta con otro medio sobre el mismo enlace** mientras el checkout no venza | – |
| `refunded` | `refunded` | sin cambios; si no lo pidió el sistema, se asienta la salida de caja | `payment_refunded` |
| `charged_back` | `charged_back`; egreso en caja por el **total del pago menos lo ya devuelto** (no se duplica un reintegro previo) | sin cambios | `payment_chargeback` |
| `in_mediation` | `in_mediation` (la plata sigue acreditada) | si el aviso de la aprobación no llegó, se da por pagado | `payment_in_mediation` |

El **contracargo** llega además por su propio tópico (`topic_chargebacks_wh`): se consulta `GET /v1/chargebacks/:id`, se marca
en el pago, se alinea el estado del pago con lo que dice la pasarela hoy y se avisa con el plazo y el pedido de comprobante de
entrega (`payment_chargeback_opened`). El `status_detail` del contracargo decide la caja, y **sólo se mueve plata con lo que la documentación respalda**
(https://www.mercadopago.com.ar/developers/en/docs/checkout-api-payments/response-handling/query-results y
https://www.mercadopago.com.ar/developers/en/docs/checkout-pro-preferences/chargebacks/introduction):

| `status_detail` | Lo que dice la documentación (textual) | Qué hace la caja |
|---|---|---|
| `in_process` | «The payment is in process due to the payer disowning it.» Y: «During the chargeback resolution period, the disputed amount remains on hold in the seller's account until the process is completed.» | **Nada**: el monto está en espera, no retirado. Solo el aviso `payment_chargeback` |
| `settled` | «The money was retained after a chargeback process.» Y: «If the chargeback request is deemed valid […] the funds are withdrawn from the seller, and returned to the customer.» | **Egreso** por el total del pago menos lo ya egresado |
| `reimbursed` | «The money was reimbursed after a chargeback process.» (no dice a quién). La resolución sí: `coverage_applied` `true` = «The decision was in favor of the seller and the money will be refunded»; `false` = «The decision was against the seller and the money will be deducted» (https://www.mercadopago.com.ar/developers/en/docs/checkout-pro-preferences/chargebacks/manage) | Si el caso informa `coverage_applied: true`: **contra-asiento** (ingreso a la misma caja, una vez) + `payment_chargeback_resolved`. Si no: **no asienta nada** y avisa `payment_chargeback_review` para que el administrador lo concilie a mano |

El contra-asiento se decide por el estado de la caja (hay egreso del contracargo y no hay ingreso), no por el cambio de
`status_detail`: si un asiento falla, el próximo aviso (de pago o de contracargo) o la conciliación lo reintentan. Los contracargos
que el ledger viejo guardó como `refunded` los pasa a `charged_back` la migración `ContracargosComoContracargo` (con su entrada de historial).

La **alerta de fraude** (`stop_delivery_op_wh`) marca el pago, avisa (`payment_fraud_alert`, con mail)
y, si el pedido (o la reserva con seña paga) todavía no tiene chofer, lo **retiene** (`order.payment_fraud_hold`): deja de ofrecerse
(se retiran las ofertas vivas y los lotes de recorrido lo saltean), nadie lo acepta ni lo asigna (409 propio: «retenido por una alerta de
fraude») y una reserva no se activa. El estado v2 del pago informa `paymentFraudHold`; el panel lo muestra en la lista y en el
detalle y un administrador lo libera con `PATCH /api/v2/orders/:id/payment/fraud-hold/release` (motivo obligatorio de 10 a 500
caracteres; quedan quién, cuándo y por qué en el pedido y lo asienta la auditoría). La otra salida es cancelar el pedido
(https://www.mercadopago.com.ar/developers/es/docs/your-integrations/notifications/additional-info). Se resuelve cancelando el pedido
(que devuelve el pago).

### La alerta de fraude no se reintenta: bandeja de entrada

**Aislamiento entre cuentas.** El `payment_id` del cuerpo del aviso no está firmado (la firma cubre el `data.id` de la URL): una
distribuidora con su propio secreto podría nombrar un pago ajeno. Por eso el pago se lee SIEMPRE de Mercado Pago con la cuenta que
firmó el aviso (`?account=`): si esa cuenta no lo tiene (404) o el ledger lo tiene con otra cuenta, la alerta se descarta con un log
(y se contesta 200). La bandeja deduplica por tipo, recurso **y cuenta**, así una alerta falsa sembrada no tapa a la verdadera.

Según la documentación, la alerta de fraude no sigue la lógica de reintentos: sin 200/201 se pierde
(https://www.mercadopago.com.ar/developers/es/docs/your-integrations/notifications/additional-info). Por eso, con la firma
válida, el webhook **guarda el aviso crudo** en `payment_notification_inbox`, **contesta 200 siempre** (503 sólo si ni siquiera se
puede guardar) y lo procesa aparte, con reintentos propios (cada 30 s; espera que se duplica hasta 30 min; 8 intentos). Los intentos se cuentan en SQL al tomar el lote (con `FOR UPDATE SKIP LOCKED` y un lease de 60 s). Si se
agotan, el aviso queda `failed` y el administrador recibe `payment_alert_unprocessed` (con mail). Los avisos procesados se purgan a los `PAYMENT_INBOX_RETENTION_DAYS` días (90 por defecto); los `failed` se conservan con su
`raw_body` y `credential_id` como evidencia. La tabla es una cola técnica y no
entra en la auditoría de datos; lo que se hace con el aviso (retener el pedido) sí.

### Webhook: responde después de procesar

`POST /api/webhook/mercadopago` valida la firma, procesa y **recién entonces** responde. Mercado Pago espera un 200/201 dentro de
22 segundos y, si no lo recibe, reintenta 8 veces (a los 0, 15 y 30 minutos, a las 6 y 48 horas y tres veces cada 96 horas;
https://www.mercadopago.com.ar/developers/es/docs/your-integrations/notifications/webhooks):

| Caso | Respuesta |
|---|---|
| Procesado (o aviso que no corresponde: pago desconocido, tópico que no usamos) | `200` |
| Firma que falta, mal formada o que no coincide; cuenta inexistente | `401` |
| No se pudo verificar la firma (base o credencial caídas) o no se pudo procesar (Mercado Pago no responde, base) | `503`: Mercado Pago reintenta |

Sin cola en memoria: un aviso que se perdiera con el proceso dejaría un pago cobrado sin aplicar. El procesamiento es idempotente.
**La firma se valida sin tolerancia de `ts`**: la documentación dice que el `ts` va en milisegundos (su ejemplo de 10 dígitos
parece de segundos) y no aclara si los reintentos —que siguen durante días— se vuelven a firmar con un `ts` nuevo; rechazar por
antigüedad podría tirar avisos legítimos. El pago se
vuelve a consultar siempre a Mercado Pago, así que un aviso repetido no puede falsear nada. Para decidirlo con datos reales: loguear
temporalmente el `ts` crudo de un aviso (10 o 13 dígitos) y ver si un reintento trae `ts` nuevo.

### Conciliación (las redes de seguridad)

Si un aviso no llega (proceso caído, red, reintentos agotados), el pago se recupera preguntándole a Mercado Pago por
`external_reference`:

- **cada 5 minutos** (`ConciliacionMercadoPagoService`, en el segundo 30): pedidos de Mercado Pago pendientes con más de 3 minutos;
  aplica los pagos cobrados con el mismo caso de uso del webhook. Si hay **más de un pago cobrado**, aplica todos: el primero
  confirma el pedido y el resto se devuelve como cobro duplicado. Revisa 50 por pasada, empezando por los que hace más que no mira;
- antes de **cancelar un pedido por vencimiento** pregunta lo mismo: con un pago cobrado lo aplica, con uno en curso espera, y si
  Mercado Pago no responde no cancela. Si hay plata cobrada que el pedido no pudo tomar (importe o cuenta distintos, también en un pedido cancelado o ya pagado), avisa
  (`payment_needs_review`) y no cancela: decide el administrador. Si la consulta falla más de 2 horas (p. ej. credencial propia
  revocada, 401/403) avisa (`payment_lookup_failed`);
- las **reservas** con la seña por Mercado Pago también se concilian, y antes de cancelar una reserva por seña impaga se le pregunta a
  la pasarela (con el pedido bloqueado y la seña re-chequeada dentro de la transacción);
- **cada 15 minutos** (segundo 45): pedidos de Mercado Pago **cancelados** en las últimas `ORDER_MERCADOPAGO_CANCELLED_SWEEP_HOURS`
  (48 por defecto); un pago cobrado que no se devolvió se aplica y el flujo de pago tardío lo devuelve. Se pagina (no sólo los primeros) y sólo se saltea el **pago** cuya devolución rechazó la pasarela. Un pago con reclamo abierto no
  se devuelve solo: se avisa.

Al cancelar un pedido de Mercado Pago (o vencerlo) se **cierra el checkout** en la pasarela (`PUT /checkout/preferences/:id` con
`expiration_date_to` = ahora), para que el enlace deje de cobrar.

### Pago duplicado y pago tardío

- Un **segundo pago aprobado** del mismo checkout sobre un pedido ya pagado se devuelve solo (CU-168), siempre **ese** pago y no el
  primero, y se avisa (`payment_duplicate`).
- Un pago aprobado sobre un pedido **cancelado** se devuelve; si no se puede dejar registrada la devolución, el webhook responde
  `503` y se reintenta.

### API v2: estado del pago

| Endpoint | Rol | Devuelve |
|---|---|---|
| `GET /api/v2/orders/:id/payment` | cliente (sus pedidos), admin, superadmin con `X-Distributor` | `paymentStatus` (los 9, o `null` sin pagos de Mercado Pago), `paymentStatusDetail`, `paymentStatusLabel` (texto en castellano **armado por el back**; un rechazo sin motivo conocido dice «Rechazado por el banco»), `canRetry`, `paymentUrl` y, para el staff, `history` |
| `GET /api/v2/orders/payments?ids=a,b,c` | admin, superadmin | lo mismo sin historial, hasta 50 pedidos (la lista del panel) |

`canRetry` es `true` si el pedido sigue vivo y sin pagar, el pago no está en curso ni acreditado y el enlace no venció. El panel y la
app muestran el texto tal cual y no deciden el estado. `GET /api/v1/orders/:id` devuelve `payment_url` también con el último pago
rechazado, para reintentar.

## Pendiente

- La clave pública se guarda pero todavía no la usan las apps.
- La conciliación de un rango que cruza un reemplazo de cuenta sólo trae los movimientos de la cuenta
  vigente.
- Al regenerar un checkout (todavía no existe), el intento de cobro a tomar tiene que filtrarse por cuenta.
- El caso feliz de la carga sólo está probado con Mercado Pago simulado: falta probarlo con una cuenta real.
