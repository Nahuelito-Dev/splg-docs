# Clientes de la empresa: alta, baja y reactivación (API v2)

Un cliente es de la plataforma (su cuenta se crea una vez) y puede comprarle a más de una
distribuidora. Cada distribuidora maneja **su vínculo** con el cliente: lo da de alta, lo da de baja o lo
reactiva, sin tocar la cuenta ni lo que el cliente tiene con otras empresas.

Como toda eliminación en SPLG, la baja es **lógica**: el vínculo (`customer_distributor`) queda con
`removed_at` y quién la hizo (`removed_by_user_id`). No se borra nada: la cuenta, los pedidos y el
historial se conservan y la baja se revierte con la reactivación.

## Endpoints

| Endpoint | Quién | Para |
|---|---|---|
| `DELETE /api/v2/customers/:id/distributor` | admin, superadmin | Dar de baja al cliente en la distribuidora. 409 si tiene pedidos en curso con ella; 404 si no es su cliente |
| `GET /api/v2/customers/removed` | admin, superadmin | Los clientes que la distribuidora dio de baja, paginados, con búsqueda por nombre o teléfono |
| `POST /api/v2/customers/:id/distributor` | admin, superadmin | Reactivar a un cliente dado de baja |

El listado normal (`GET /api/v1/customers`) nunca incluye a los dados de baja, y la ficha de un dado de
baja responde 404 para el admin de esa distribuidora.

La baja v1 (`DELETE /api/v1/customers/:id`) es la baja lógica de la **cuenta entera** del cliente
(`deletedAt`), que alcanza a todas las distribuidoras: el panel ya no la usa.

## Panel

- **Dar de baja** (listado y ficha del cliente): la confirmación aclara que deja de ser cliente de esta
  distribuidora, que su cuenta sigue existiendo y que se puede reactivar. Si tiene pedidos en curso se
  muestra el motivo del back. La pueden usar el admin de la empresa y el superadmin con «Ver como».
- **Pestaña «Dados de baja»** en Clientes, con contador, búsqueda (nombre o teléfono) y «Reactivar».
- Si la lista estaba vieja (otro admin ya lo dio de baja o lo reactivó), se avisa y se refresca.
- El superadmin sin «Ver como» ve las acciones apagadas y, en la pestaña, el pedido de elegir una
  distribuidora.

Probado el 28/10/2026 contra la API y la base: se dio de baja a un cliente de la demo desde el panel (el
vínculo quedó con `removed_at` y la cuenta intacta), apareció en «Dados de baja» y al reactivarlo el
vínculo volvió a quedar activo.
