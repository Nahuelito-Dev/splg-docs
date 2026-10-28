# Exportes completos (F1, API v2)

Cualquier listado del panel se puede bajar entero en CSV o en Excel: todas las filas que cumplen los
filtros activos, no sólo la página que se ve.

## Endpoint

`GET /api/v2/exports/:recurso?format=csv|xlsx&<filtros>` — sólo existe en la v2.

| | |
|---|---|
| Quién | Admin de la distribuidora, o superadmin con `X-Distributor` (sin distribuidora responde 400) |
| Filtros | Los mismos que el listado de cada recurso; `limit`, `offset` y `page` se ignoran |
| `format` | `csv` (por defecto) o `xlsx`; otro valor responde 400 |
| Respuesta | El archivo como descarga (`<recurso>-<AAAA-MM-DD>.<ext>`) y el total de filas en `X-Total-Count` |
| Tope | 50.000 filas por exporte (`EXPORT_MAX_ROWS`); si hay más, responde 400 |
| Recurso inexistente | 404 con la lista de recursos válidos |

El CSV usa `;` como separador y coma decimal, con BOM UTF-8 para que Excel lea bien las tildes. Los
textos que empiezan con `=`, `+`, `-` o `@` se escriben como texto, para que Excel no los ejecute como
fórmula.

Un administrador siempre exporta su propia distribuidora: un `X-Distributor` de otra empresa se
ignora (comprobado contra la API el 28/10/2026).

## Recursos

`pedidos`, `clientes`, `choferes`, `vehiculos`, `garrafas`, `envases`, `stock-resumen`,
`stock-movimientos`, `cajas`, `movimientos-caja`, `cuentas-corrientes`, `rendiciones`, `liquidaciones`,
`combustible`, `multas`, `siniestros`, `neumaticos`, `costos-flota`, `reclamos`, `incidencias`,
`ordenes-compra`, `recepciones`, `proveedores`, `legajos`, `auditoria` y `auditoria-datos`.

`reclamos` e `incidencias` no aceptan filtros: exportan todas las filas.

## Panel

En cada listado, el menú «Más» (⋮) ofrece **Exportar CSV** y **Exportar Excel**. Mientras se prepara
el archivo avisa «Preparando…» y al terminar dice cuántas filas se exportaron; si el back responde un
error, muestra su mensaje.

El exporte queda apagado, con el motivo, cuando no coincidiría con lo que muestra la pantalla:

| Pantalla | Cuándo | Por qué |
|---|---|---|
| Reclamos e Incidencias | Con un filtro activo | El back no filtra esos recursos |
| Choferes | Pestaña «En línea» | La pestaña lista habilitados, validados y disponibles; el exporte filtra sólo disponibles |
| Vehículos | Con búsqueda por patente | El back no acepta esa búsqueda |
| Garrafas | Vistas por tipo, «Sólo disponibles» y «Dados de baja» | El back no acepta esos filtros |
| Envases | Con búsqueda de texto | El back no acepta esa búsqueda |
| Legajos | Mientras cargan los puestos | Evita exportar sin el filtro de puesto |
| Cualquiera | Superadmin sin «Ver como» | El back necesita la distribuidora |

Con filas marcadas, Pedidos, Clientes, Choferes y Envases ofrecen además **Exportar selección** (CSV de
las filas elegidas). Comisiones conserva el CSV de la página visible porque el back no tiene ese
recurso.
