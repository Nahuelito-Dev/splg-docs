# Vigencia de envases (C-11)

CU-132 a CU-135. El sistema conoce hasta cuándo puede circular cada envase y bloquea el despacho
del vencido. Todo está también en Swagger (`/docs`, tag "Cylinders").

El vencimiento vive en `cylinder.expires_at`; el historial de revisiones, en
`cylinder_inspection` (una fila por revisión, sólo altas). No hay migración nueva: las dos
estructuras ya existían (`ModeloPropuesto`).

## Acceso y aislamiento

Rol `admin` o `super_admin`. Las escrituras exigen distribuidora en contexto (el admin, la suya; el
super admin, `X-Distributor`). Un envase, serial o pedido de otra distribuidora responde **404**.

## Fechas: día calendario de Buenos Aires

El vencimiento es un **día de calendario** en `America/Argentina/Buenos_Aires` (UTC-3, sin horario
de verano) y el envase es vigente **durante todo ese día**. El back normaliza:

- `POST .../inspections` recibe `inspectedAt` y `nextDueAt` como `YYYY-MM-DD` (si llega un ISO
  completo se toma su parte de fecha, sin correr por zona).
- `cylinder.expires_at` se guarda como las 23:59:59.999 hora argentina del día de vencimiento
  (= día siguiente 02:59:59.999 UTC); `inspectedAt` / `last_inspection_at`, como las 00:00 hora
  argentina del día de la revisión. La revisión no puede ser de un día futuro (según Buenos Aires).
- `daysRemaining` cuenta **días calendario** argentinos: 0 = vence hoy (todo el día), -1 = venció ayer.
- Los clientes tienen que mostrar estas fechas en esa zona (el panel lo hace). Los instantes viajan
  en UTC como siempre.

Borde cubierto por test (`domain/cylinder-vigencia.spec.ts`): el día de vencimiento a las 00:00,
21:00 (medianoche UTC) y 23:59 hora argentina el envase sigue vigente con 0 días; a las 00:00 del
día siguiente ya está vencido.

## Vigencia

Un único cálculo (`domain/cylinder-vigencia.ts`) lo comparten la consulta, el listado y el bloqueo:

| `status`     | Cuándo                                     | `daysRemaining`                         |
| ------------ | ------------------------------------------ | --------------------------------------- |
| `valid`      | `expires_at` en el futuro                  | días que faltan (redondea hacia arriba) |
| `expired`    | `expires_at` igual o anterior a ahora      | negativo                                |
| `unverified` | sin `expires_at` (sin revisión registrada) | `null`                                  |

`unverified` **no es** `expired`: no bloquea el despacho, para no frenar el parque entero el día que
se active el control.

## `POST /cylinders/:id/inspections` (CU-132)

Cuerpo: `inspectedAt` (día, no futuro), `result` (`approved` | `conditional` | `rejected`), `nextDueAt`
(último día vigente; obligatorio salvo `rejected`, posterior a `inspectedAt`), `notes` (opcional, hasta 500).

- Guarda la revisión y copia en la ficha `last_inspection_at` y `expires_at`.
- `rejected`: el vencimiento queda en `inspectedAt` (el envase queda bloqueado) y `nextDueAt` no se guarda.
- Una revisión anterior a la última cargada sólo entra al historial; no pisa la ficha.
- Rechazado y en reparto o en poder de un cliente: no cambia de estado; se anota un movimiento
  (mismo estado, nota "retirar el envase cuando vuelva") y la vigencia devuelve `withdrawalPending: true`.
- Envase dado de baja: **409**. Fecha futura, vencimiento faltante o no posterior: **400**.

`PATCH /cylinders/:id` **ya no acepta** `expiresAt` ni `lastInspectionAt` (400): sólo se asientan por
esta operación.

Responde **201** con la vigencia del envase (misma forma que `GET .../vigencia`).

## `GET /cylinders/:id/vigencia` y `GET /cylinders/vigencia/serial/:serial` (CU-133)

`cylinderId`, `serial`, `state`, `productType`, `manufacturedAt`, `lastInspectionAt`, `expiresAt`,
`status`, `daysRemaining`, `withdrawalPending` (vencido y todavía afuera) e `inspections` (de la más
reciente a la más antigua).

## `GET /cylinders/vigencia/proximos-a-vencer?days=30&limit=100&offset=0` (CU-134)

`days` de 1 a 365 (por omisión 30); `limit` de 1 a 500 (por omisión 100) y `offset` pagina **cada
grupo**; fuera de rango, **400**. Responde `windowDays`, `totals` (total de cada grupo sin paginar) y
tres grupos, sin envases dados de baja:

- `expired`: ya vencidos, del más atrasado al menos.
- `expiring`: vencen dentro de la ventana, del más urgente al menos.
- `unverified`: sin revisión registrada (aparte, no tienen fecha con la cual comparar), por serial.

`GET /cylinders/vigencia/serial/:serial` exige distribuidora en contexto: el serial es único por
distribuidora, y el super admin sin `X-Distributor` recibe **400**.

## Despacho: `POST /cylinders/assign` y `PATCH /cylinders/:id/transition` (CU-135, extiende CU-068)

El bloqueo vive en la transición a `dispatched` (`recordTransition`), así que cubre **todas** las
puertas: la asignación a un pedido y la transición suelta, desde el admin o el chofer. Un envase
vencido que vuelve al depósito (`in_depot`) no se bloquea.

En `assign`, con los envases bloqueados (`FOR UPDATE`):

1. Pedido o algún serial inexistente o de otra distribuidora: **404**, sin escribir. Seriales repetidos: **400**.
2. Algún envase que no puede pasar a `dispatched` (no está `filled`): **400**, antes de mirar vencimientos.
3. Algún envase vencido: **409** y no se asigna ninguno. Cuerpo (Swagger: `CylinderExpiredResponseDto`):
   `{ statusCode: 409, error: "Conflict", code: "CYLINDER_EXPIRED", message, serials: ["SN-1"] }`.
   La transición suelta devuelve el mismo 409 con ese único serial. Además se avisa a los admins de
   la distribuidora por el socket del panel (evento `cylinder:dispatch-blocked`,
   `{ orderId | null, serials }`); un aviso que falla no cambia la respuesta.
4. Sin vencimiento cargado: pasa; el movimiento queda con la nota "(sin revisión registrada)".
5. Cualquier falla revierte todo: la asignación es atómica. Dos asignaciones del mismo serial a la
   vez: una gana y la otra recibe 400.

No hay parámetro para desactivar el bloqueo: el CUE no lo prevé.

Para buscar un reemplazo, `GET /cylinders` acepta `gasCylinderId` (tipo de producto) y
`vigencia` (`valid` | `expired` | `unverified` | `dispatchable`; este último = vigentes + sin
revisión registrada, los que se pueden asignar), combinables con `state`.
