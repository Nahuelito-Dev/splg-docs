# PDFs generados por el back (API v2)

El back arma los documentos en PDF con el membrete de la distribuidora (logo, razón social, CUIT y
contacto), con pie de página numerado. Sólo existen en la v2.

## Endpoints

Todos son `GET` bajo `/api/v2`, devuelven `application/pdf` y aceptan `?disposicion=inline|attachment`
(por defecto `attachment`).

| Endpoint | Documento | Quién |
|---|---|---|
| `/orders/:id/remito.pdf` | Remito del pedido | Cliente (sólo los suyos), admin y superadmin |
| `/orders/:id/recibo.pdf` | Recibo de pago | Cliente (sólo los suyos), admin y superadmin |
| `/driver-settlements/:id/pdf` | Rendición del chofer | Chofer (sólo las suyas), admin y superadmin |
| `/driver-liquidations/:id/pdf` | Liquidación de comisiones | Admin y superadmin |
| `/cash-sessions/:id/pdf` | Cierre (o arqueo, si está abierta) de una sesión de caja | Admin y superadmin |
| `/reports/sales.pdf?desde=AAAA-MM-DD&hasta=AAAA-MM-DD` | Reporte de ventas del período | Admin y superadmin |

## Reglas

- **Recibo**: sólo de un pedido pagado y no cancelado. Si no está pagado, o si está cancelado (un
  cancelado pagado se reintegra), responde **409**.
- **Código de entrega**: el remito lo imprime sólo cuando lo pide el personal (admin o superadmin).
  El remito que baja el cliente sale sin el código.
- **Cobrado el**: el remito y el recibo muestran la fecha del cobro. Desde la v2 también la guarda el
  pago aprobado por Mercado Pago.
- **Distribuidora**: el admin siempre obtiene documentos de su propia distribuidora; un pedido de otra
  responde 404. El superadmin necesita `X-Distributor` (sin ella responde 400).
- **Texto**: la fuente del PDF (Helvetica) cubre el alfabeto latino occidental. A las letras que no
  tiene se les quita el signo (Łódź → Lódz) y lo demás (emojis, otros alfabetos) sale como `?`. Los
  textos muy largos se cortan con «…» (300 caracteres en los datos, 200 en las celdas de una tabla)
  para que no desarmen la página.

Comprobado contra la API el 28/10/2026: los seis documentos, el 409 del recibo (impago y cancelado),
el 404 de otra distribuidora y de otro cliente, el 401 sin sesión, el remito del cliente sin código y
la rendición pedida por el chofer.

## Panel

| Pantalla | Dónde |
|---|---|
| Detalle del pedido | Menú «Más acciones»: «Remito (PDF)» y, si está pagado y no cancelado, «Recibo (PDF)» |
| Detalle de rendición y de liquidación | Botón «PDF» del encabezado |
| Detalle de una caja | Menú de cada sesión cerrada: «Cierre (PDF)» |
| Reportes | «Descargar PDF» con el período elegido |

El PDF se abre en una pestaña nueva; si el navegador la bloquea, se descarga. Si el back responde un
error, el panel muestra su mensaje. Para el superadmin sin «Ver como» las opciones quedan apagadas con
el motivo. La impresión vieja del remito desde el navegador se reemplazó por el PDF del back.

## Apps

| App | Dónde | Qué |
|---|---|---|
| Cliente | Detalle del pedido | «Remito (PDF)» siempre y «Recibo (PDF)» si el pedido está pagado y no cancelado |
| Chofer | Mi rendición | «Rendición (PDF)» de la rendición que se está viendo |

Las apps bajan el PDF de la v2 con la sesión del usuario, lo guardan en su carpeta temporal con el
mismo nombre que el panel (`recibo-15550F8E.pdf`, `rendicion-20.pdf`) y abren la hoja nativa del
sistema para verlo, guardarlo, imprimirlo o compartirlo (`share_plus`). Si el back responde un error,
la app muestra su mensaje. Probado en iPhone (cliente) y Android (chofer) contra la API el 28/10/2026.
