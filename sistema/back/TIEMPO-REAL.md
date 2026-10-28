# Tiempo real (F7)

Socket.IO con tres namespaces y adapter de Redis (varias instancias del back comparten las salas).
Los nombres de los eventos están escritos en el código, uno por uno: un estado nuevo del pedido no
crea un evento sin decidirlo.

## Conexión

- **Identidad**: el token de Firebase va en el handshake (`auth.token` o cabecera `Authorization`).
  El back resuelve el usuario en la base y decide las salas; lo que mande el cliente en el cuerpo se
  ignora.
- **Salas**: `admins:<distribuidora>` (los admins de esa distribuidora), `admins:super` (los super
  admin, ven todas), `customer_<userId>`, `driver_<userId>` y, en los tres namespaces,
  `usuario:<userId>` (para cortarle todo a un usuario).
- **Origen**: la misma lista que HTTP (`CORS_ORIGINS`). Un navegador desde otra página se rechaza
  aunque use el transporte websocket; las apps nativas no mandan `Origin` y entran (las autentica
  el token).

## Sesión

| Evento | Cuándo | Qué hace el cliente |
|---|---|---|
| `server:ack` | Al unirse a su sala | Nada (diagnóstico) |
| `server:session-expired` | Venció el token del handshake. Se revisa cada minuto y se corta la conexión | Vuelve a conectar con un token nuevo: el back resuelve la identidad otra vez (rol, distribuidora, bloqueo) |
| `server:access-revoked` `{ motivo: 'bloqueo' \| 'baja' }` | En el momento en que se bloquea, se da de baja o egresa la cuenta. Corta todas sus conexiones, en cualquier instancia | No reconecta. La app del chofer queda fuera de línea con el aviso «Tu cuenta no está habilitada» |

Cuando el servidor corta, socket.io no reconecta solo: el panel y la app del cliente vuelven a
conectar sólo después de `server:session-expired`. La app del chofer reintenta con espera creciente
y token nuevo, y se rinde al toque si antes llegó `server:access-revoked`.

## Panel (`/admin`)

| Evento | Qué avisa |
|---|---|
| `order:created`, `order:accepted`, `order:on-the-way`, `order:delivered`, `order:cancelled`, `order:pending` | Ciclo de vida del pedido (`pending`: liberado, vuelve a buscar chofer) |
| `order:assignment-declined`, `order:no-drivers` | Despacho: el chofer no confirmó; no quedan choferes |
| `order:address-changed`, `order:updated` | El cliente cambió la dirección o modificó el pedido |
| `order:payment-refunded`, `order:refund-failed` | Reintegro hecho o fallido |
| `order:express-degraded` | El express pasó al reparto común |
| `order:transfer-receipt-uploaded` | El cliente subió el comprobante de transferencia |
| `order:driver-location` | Posición del chofer en reparto |
| `incident:created` | **Toda** incidencia nueva. El cobro impago tiene su aviso propio; el resto avisa con su tipo |
| `claim:created` | Reclamo nuevo de un cliente, con su motivo |
| `coverage:no-active-zones`, `cylinder:dispatch-blocked` | Sin zonas activas; despacho bloqueado por envases vencidos |
| `admin:notification` | Un aviso nuevo de la bandeja (F10, ver `BANDEJA-ADMIN.md`): el panel refresca la campana |

Desde la v2 ya no sale el alias `order:on_the_way` (nadie lo escuchaba y duplicaba el aviso).

## App del cliente (`/customers`)

`order:accepted`, `order:on-the-way`, `order:delivered`, `order:cancelled`,
`order:searching-driver`, `order:arrived`, `order:express-degraded`, `order:driver-location` y, desde
la v2, `order:updated`, `order:payment-approved` y `order:payment-refunded` (el seguimiento vuelve a
leer el pedido). Reconecta sin tope de intentos mientras sigue el pedido.

## App del chofer (`/drivers`)

`server:new-order-request` (oferta), `order:cancelled` y, desde la v2, `order:address-changed`: la
pantalla del viaje relee el pedido, rehace la ruta al destino nuevo y avisa «El cliente cambió la
dirección de entrega».

Probado el 28/10/2026 contra la API: el panel desde :3001 entra y desde otra página no; un chofer
bloqueado pierde la conexión en el acto, no puede volver a entrar y sí al desbloquearlo (también en
la app, en el simulador de iPhone); un reclamo y una incidencia nuevos avisan en la campana y
refrescan sus listas sin recargar. El corte por token vencido se probó con tests (el token dura una
hora).
