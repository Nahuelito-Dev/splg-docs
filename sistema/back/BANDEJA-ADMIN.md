# Bandeja de notificaciones del admin

Los avisos que piden hacer algo quedan **guardados** para los administradores de cada distribuidora:
llegan en vivo, se ven en la campana y en la página «Notificaciones» del panel, cada admin marca lo
suyo como leído y, si el aviso lo pide, salen también por mail.

## Cómo entra un aviso

Cualquier módulo emite `EVENTO_NOTIFICAR_ADMIN` (`src/common/events/notificar-admin.event.ts`) con la
distribuidora, el tipo (`kind`), título, cuerpo, a dónde lleva (`link`), si va por mail y una
`dedupeKey`. El módulo `src/admin-notifications/`:

1. Lo guarda en `admin_notification`, **una sola vez** por `(distribuidora, dedupeKey)`. Un repetido
   no se guarda ni vuelve a avisar; si dos llegan a la vez, el único de la base decide.
2. Lo empuja por socket al panel: `admin:notification` (namespace `admin`, sala de la distribuidora
   y de los super admin) con el aviso y su `distributorId`.
3. Con `email: true`, manda un mail a cada admin **activo** de esa distribuidora (no bloqueado, no
   dado de baja), con el texto escapado, el asunto en una sola línea y el enlace al panel. Anota
   `emailed_at`. Un fallo de envío se registra y no rompe nada.

Un error al guardar o avisar nunca rompe la operación que lo pidió (el reclamo, la incidencia,
el despacho).

## Qué avisos hay hoy

| Tipo | Cuándo | Lleva a | Mail |
|---|---|---|---|
| `claim_created` | Un cliente abre un reclamo | el reclamo | no |
| `incident_created` | Se registra una incidencia (también el cobro impago) | la incidencia | no |
| `order_no_drivers` | Un pedido se quedó sin choferes a quién ofrecerlo (uno por pedido y día) | el pedido | no |
| `refund_failed` | Falló un reintegro (uno por intento: si el reintento vuelve a fallar, es un aviso nuevo) | el pedido | no |
| `transfer_receipt_uploaded` | El cliente subió el comprobante de su transferencia | el pedido | no |
| `cylinder_dispatch_blocked` | Se rechazó un despacho por envases con la revisión vencida | el pedido | no |
| `fleet_document_due` | Un vencimiento de flota o de personal entró en su anticipación (la VTV, 30 días antes) | la tarea | el resumen diario |
| `fleet_document_expired` | Ese vencimiento ya pasó (aunque se haya avisado antes como «por vencer») | la tarea | el resumen diario |
| `employee_document_missing` | A un chofer activo le falta cargar un documento que bloquea el despacho (uno por documento y por mes mientras falte) | la pestaña Documentación del legajo | el resumen diario |
| `insurance_installment_due` | Una cuota del seguro vence en 5 días o menos | el seguro del vehículo | sí |
| `insurance_installment_overdue` | Una cuota del seguro pasó su gracia sin pagar | el seguro del vehículo | sí |
| `insurance_policy_expiring` | La póliza vence en 30 días o menos y no hay otra que la reemplace | el seguro del vehículo | sí |
| `traffic_fine_due` | Una multa pendiente vence en 5 días o menos | la multa | sí |
| `traffic_fine_overdue` | Una multa pendiente venció sin pagar (hasta 30 días después) | la multa | sí |
| `payment_in_mediation` | El comprador abrió un reclamo sobre un pago de Mercado Pago (uno por pago) | el pedido | no |
| `payment_chargeback_opened` | Mercado Pago informó un contracargo: plazo y comprobante de entrega a presentar (uno por contracargo y pago) | el pedido | no |
| `payment_chargeback` | El pago pasó a contracargo y Mercado Pago lo devolvió (uno por pago) | el pedido | no |
| `payment_refunded` | Un pago se devolvió desde el panel de Mercado Pago, no desde el sistema (uno por pago) | el pedido | no |
| `payment_fraud_alert` | Alerta de fraude de Mercado Pago sobre un pago: no entregar el pedido, que se frenó si todavía no tenía chofer (uno por pago) | el pedido | sí |
| `payment_chargeback_resolved` | Mercado Pago le devolvió al comercio el dinero de un contracargo (`reimbursed`); se asentó el ingreso (uno por pago) | el pedido | no |
| `payment_alert_unprocessed` | Una alerta de Mercado Pago (fraude) no se pudo procesar tras 8 intentos: mirarla en Mercado Pago (uno por pago) | el pedido | sí |
| `payment_chargeback_review` | Mercado Pago informa un contracargo `reimbursed` sin confirmar que el caso se resolvió a favor del comercio: conciliarlo a mano (uno por pago) | el pedido | no |
| `payment_duplicate` | Un cliente pagó dos veces el mismo pedido: se devolvió el segundo pago (uno por pago) | el pedido | no |
| `payment_needs_review` | Mercado Pago cobró un pago que el pedido no pudo tomar (importe o cuenta distintos): decide el admin (uno por pago) | el pedido | no |
| `payment_lookup_failed` | Hace más de 2 horas que no se puede consultar a Mercado Pago el pago de un pedido (p. ej. credencial rechazada) (uno por pedido) | el pedido | no |
| `payment_without_attempt` | Llegó un pago de Mercado Pago para un pedido sin intento de cobro registrado (uno por pago) | el pedido | no |

Los vencimientos los arma el aviso diario de flota (`FleetAlertsCron`, a la hora que eligió
cada distribuidora): además de su **mail resumen** de siempre, deja cada vencimiento y cada documento
faltante en la bandeja, sin pedir otro mail para no mandarlo dos veces. La anticipación es la del plan
(la VTV, 30 días). Un vencimiento avisa dos veces por fecha: al entrar en «por vencer» y al vencer.
Si se reprograma la fecha, la nueva vuelve a avisar. Antes, una tarea avisada como «por vencer» no
volvía a avisar cuando vencía. La marca de «avisado por mail» (`alertedAt`) se sigue escribiendo
sólo en su columna (`update`). Con `save`, una tarea que el admin cerró mientras salía el mail
volvería a los valores leídos antes. Esa marca técnica está fuera de la auditoría de datos a
propósito. Los seguros (`SEGUROS.md`) y las multas (`FLOTA-AMPLIADA.md`) avisan por la bandeja
con su propio mail, uno por aviso. Los movimientos comunes del pedido (creado, aceptado, en camino, entregado) siguen sólo en
vivo: no se guardan, para no llenar la bandeja.

## API (v2)

| Endpoint | Devuelve |
|---|---|
| `GET /api/v2/admin-notifications?unread=true\|false&limit=1..100&offset` | `{ items, total }`, más nuevos primero |
| `GET /api/v2/admin-notifications/unread-count` | `{ count }` |
| `PATCH /api/v2/admin-notifications/:id/read` | el aviso; idempotente (conserva la primera fecha) |
| `PATCH /api/v2/admin-notifications/read-all` | `{ updated }` |

Cada aviso: `{ id, kind, title, body, link: { entity, id } | null, createdAt, readAt }`. `readAt` es
el del admin que pregunta: lo que lee uno no queda leído para otro. Admin y super admin; el admin ve
su distribuidora, el super admin la del `X-Distributor` («ver como») o, sin él, todas. Un aviso de
otra distribuidora es 404. «Marcar todas» marca uno por uno: si otra solicitud ya marcó alguno, ése
se saltea sin deshacer los demás.

Todo se escribe con `save`/`insert` de TypeORM, así que los avisos, las lecturas y el envío del
mail quedan en la auditoría de datos.

## Panel

- **Campana:** los avisos guardados (primera página) más los de la sesión que no se guardan, en orden.
  El número suma los sin leer de los dos. Al tocar un aviso guardado se marca leído y lleva a su
  pantalla: el pedido, el reclamo (`/claims?claim=<id>`) o la incidencia (`/incidents?incident=<id>`).
  «Ver todas» abre la página.
- **Página «Notificaciones»** (Administración): pestañas Todas y Sin leer, paginada, con «Marcar todas
  como leídas».

Probado el 28/10/2026 contra la API y en el panel:
- una incidencia y un reclamo nuevos entraron a la bandeja y a la campana en vivo, sin recargar;
- el click llevó al reclamo con su detalle abierto y lo marcó leído;
- la lectura es por usuario: el super admin lo siguió viendo sin leer;
- otra distribuidora no los ve y recibe 404 al marcarlos;
- «marcar todas» dejó el contador en 0;
- se vio en escritorio y a 320 px.

Los datos de prueba quedaron cerrados: el reclamo rechazado y la incidencia descartada.

Vencimientos de flota y personal, probado el 28/10/2026 sobre la demo, corriendo sólo el paso de la bandeja (sin mail ni marca):
- entraron 12 avisos: 2 por vencer (la renovación del carnet de un chofer y el service de la
  camioneta AF218KT) y 10 documentos obligatorios sin cargar de 5 choferes;
- en el panel se vieron con su ícono, y el click llevó a la tarea y a la pestaña Documentación del
  legajo.
