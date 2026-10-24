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
| `back/EXPRESS-REINTEGROS.md` | Compra express y reintegros (C-17) |
| `back/FINANZAS.md` | Caja, rendiciones, cuentas corrientes y comisiones |
| `back/FLOTA-AMPLIADA.md` | Flota ampliada (C-18) |
| `back/PARAMETROS-DESPACHO.md` | Parámetros del despacho y frecuencia de las tareas programadas (M1) |
| `back/PEDIDOS.md` | Pedidos, cobros, cotización, historial y rutas |
| `back/PERSONAL.md` | Documentación, asistencia, licencias, tablero y habilitación laboral |
| `back/PROCESOS-AUTOMATICOS.md` | Parámetros por distribuidora y zonas vencidas |
| `back/S3.md` | Archivos: Amazon S3 |
| `back/STOCK.md` | Stock físico |
| `back/VALIDACIONES-BASE.md` | Validaciones en la base (tanda V1) |
| `back/VIGENCIA-ENVASES.md` | Vigencia de envases (C-11) |

## Otros

| Archivo | Tema | De dónde vino |
|---|---|---|
| `postman.md` | Cómo usar la colección de Postman | `splg-app-backend/postman/LEEME.md` |

La colección de Postman (`SPLG.postman_collection.json`, el environment y `openapi.json`) es una
herramienta, no documentación: se queda en `splg-app-backend/postman/`. Las rutas que menciona
`postman.md` (`postman/…`, `scripts/postman/…`) son las de ese repo.
