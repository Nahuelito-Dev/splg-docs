# Catálogo: productos dados de baja y reactivación

CU-269 y CU-268. El catálogo (`GET /gascylinder`) sólo incluye productos activos; la baja (`DELETE /gascylinder/:id`, CU-040) es
lógica y deja el producto con `isActive = false`, con su stock y sus promociones.

## `GET /gascylinder/inactive` (CU-269)

Admin o super admin; chofer y cliente: **403**. Lista los productos dados de baja **de la distribuidora del administrador** (la de
`X-Distributor` para el super admin; sin él, **400**
`Falta la distribuidora: enviá el header X-Distributor (slug o id)`). Misma paginación (`limit`, `offset`) y búsqueda (`term`, por
tipo o descripción) que el catálogo; misma respuesta (`CatalogoDto`: `gasCylinders`, `total`, `limit`, `offset`), ordenada por
tipo. Una distribuidora no ve los inactivos de otra.

## `PATCH /gascylinder/:id/reactivate` (CU-268)

Admin o super admin con distribuidora (igual que arriba). Deja el producto **activo**: no invierte el estado, siempre lo deja activo,
así que reactivar uno que ya estaba activo responde `200` con el producto sin cambios. Sólo escribe `isActive` (por `save`: queda en la auditoría de datos): el stock, el costo
y las promociones quedan intactos. Un producto inexistente o de otra distribuidora es **404**, sin distinguir los dos casos.
Vuelve a aparecer en el catálogo del cliente en su siguiente consulta.

Es una operación propia: enviar `isActive` en `PATCH /gascylinder/:id` se rechaza (**400**, campo no permitido).

El `type` es único por distribuidora **incluyendo los inactivos**, así que un producto dado de baja no puede quedar duplicado por uno
activo nuevo y reactivar nunca choca con la unicidad.
