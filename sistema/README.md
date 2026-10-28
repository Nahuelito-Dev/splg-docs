# Documentación técnica del sistema

Lo que describe cómo está construido el código de SPLG. Vive acá, junto al resto de la
documentación, y no en los repositorios de código. Los `AGENTS.md`, `CLAUDE.md`,
`CONVENCIONES.md` y `README.md` de cada repo de código, el `legal/` de las apps, `test/README.md`
y los `scripts/**/LEEME.md` se quedan en su repo.

## Backend (`back/`)

Copiados de `splg-app-backend/docs/` (rama `develop`, commit `e05a549` del 24/10/2026). Desde entonces se mantienen acá: el back ya no tiene carpeta `docs/`.

| Archivo | Tema |
|---|---|
| `back/AUDITORIA.md` | Auditoría |
| `back/CARRITO-Y-CONSUMO.md` | Carrito persistente y consumo declarado (C-12 y C-13) |
| `back/CATALOGO.md` | Productos dados de baja y reactivación |
| `back/DEMO.md` | Demo limpia: purga completa y datos nuevos |
| `back/EXPORTES.md` | Exportes completos en CSV y Excel (F1, API v2) |
| `back/EXPRESS-REINTEGROS.md` | Compra express y reintegros (C-17) |
| `back/FINANZAS.md` | Caja, rendiciones, cuentas corrientes y comisiones |
| `back/FLOTA-AMPLIADA.md` | Flota ampliada (C-18) |
| `back/PARAMETROS-DESPACHO.md` | Parámetros del despacho y frecuencia de las tareas programadas (M1) |
| `back/PEDIDOS.md` | Pedidos, cobros, cotización, historial y rutas |
| `back/PDFS.md` | PDFs generados por el back: remito, recibo, rendición, liquidación, cierre de caja y ventas (F2, API v2) |
| `back/PERSONAL.md` | Documentación, asistencia, licencias, tablero y habilitación laboral |
| `back/PROCESOS-AUTOMATICOS.md` | Parámetros por distribuidora y zonas vencidas |
| `back/S3.md` | Archivos: Amazon S3 |
| `back/STOCK.md` | Stock físico |
| `back/VALIDACIONES-BASE.md` | Validaciones en la base (tanda V1) |
| `back/VIGENCIA-ENVASES.md` | Vigencia de envases (C-11) |

## Backend: convenciones, tests y scripts

| Archivo | Tema | De dónde vino |
|---|---|---|
| `back/CONVENCIONES.md` | Convenciones de código del back (manda sobre todo módulo nuevo) | `splg-app-backend/CONVENCIONES.md` |
| `back/TESTS.md` | Tests de integración (testcontainers) | `splg-app-backend/test/README.md` |
| `back/scripts/ALINEACION.md` | Batería de alineación API ↔ doc | `splg-app-backend/scripts/alineacion/LEEME.md` |
| `back/scripts/AISLAMIENTO.md` | Batería de aislamiento entre distribuidoras | `splg-app-backend/scripts/alineacion/aislamiento/LEEME.md` |

## Panel

| Archivo | Tema | De dónde vino |
|---|---|---|
| `panel/CONVENCIONES.md` | Convenciones de código del panel | `splg-app-admin/CONVENCIONES.md` |

## Landing

| Archivo | Tema | De dónde vino |
|---|---|---|
| `landing/README.md` | Landing comercial: stack, contenido y cómo levantarla | `splg-landing/README.md` |

## Lo que queda en los repos de código

Sólo lo que no es documentación: `AGENTS.md` y `CLAUDE.md` (configuración de los agentes y del
gate), un `README.md` de dos líneas que apunta acá, `legal/` de las apps (va empaquetado en la
app) y `ASSETS_LICENSES.md` de `splg-lib` (licencias de los recursos). Desde el 24/10/2026 la
documentación de cada repo se escribe acá, en la misma tanda que el cambio de código.

## Otros

| Archivo | Tema | De dónde vino |
|---|---|---|
| `postman.md` | Cómo usar la colección de Postman | `splg-app-backend/postman/LEEME.md` |

La colección de Postman (`SPLG.postman_collection.json`, el environment y `openapi.json`) es una
herramienta, no documentación: se queda en `splg-app-backend/postman/`. Las rutas que menciona
`postman.md` (`postman/…`, `scripts/postman/…`) son las de ese repo.
