# Bandeja de notificaciones del admin (F10)

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

Los avisos con mail llegan con F11 (vencimientos de flota: VTV 30 días antes), F14 (seguros) y F15
(multas). Los movimientos comunes del pedido (creado, aceptado, en camino, entregado) siguen sólo en
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
