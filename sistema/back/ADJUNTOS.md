# Adjuntos

Adjuntos genéricos de cualquier registro del sistema: el archivo vive en S3 y se lee sólo con URL
firmada que vence; en la base queda la referencia (dueño, etiqueta, nombre, tipo, tamaño y quién lo
subió).

## Endpoints

| Endpoint | Para |
|---|---|
| `GET /api/v1/attachments/:ownerType/:ownerId` | Los adjuntos de un registro |
| `POST /api/v1/attachments/:ownerType/:ownerId` | Subir un adjunto (multipart: `file` y `label` opcional) |
| `GET /api/v1/attachments/:id/download` | El archivo (redirección a la URL firmada, o `?modo=url`) |
| `DELETE /api/v1/attachments/:id` | Baja lógica del adjunto (queda con `deleted_at`) |

## Dueños

`employee`, `fuel_load`, `traffic_fine`, `vehicle_accident`, `purchase_receipt`, `stock_adjustment`,
`driver_settlement`, `cash_movement`, `customer_account_entry` y `order`. Cada dueño tiene su resolver
que comprueba que el registro existe y es de la distribuidora (otra empresa responde 404).

## Tipos y tamaños

- **PDF, JPG, PNG, WEBP, Word (`.docx`), Excel (`.xlsx`) y CSV**, hasta 10 MB.
- El back verifica que el **contenido** coincida con el tipo declarado (firma del PDF y las imágenes;
  paquete de Office con su documento interno para Word y Excel; texto plano para el CSV).
- El chofer sólo puede subir fotos y PDF.
- Las fotos se guardan sin metadatos.
- Word, Excel y CSV siempre se descargan: nunca se abren en el navegador (sólo PDF e imágenes se
  pueden ver).

## Panel

- El selector acepta todos los tipos de arriba. Si el navegador no informa el tipo de un Word, Excel o
  CSV (pasa en Windows sin Office) o manda uno genérico, el panel lo sube con el tipo que corresponde a
  su extensión; el back igual verifica el contenido.
- Word, Excel y CSV muestran sólo «Descargar», con su ícono.
- Tienen adjuntos: legajos, combustible, multas, siniestros, recepciones de compra, ajustes de stock y,
  desde la v2, **rendiciones** (card «Comprobantes» en el detalle), **movimientos de caja** y
  **movimientos de cuenta corriente** (acción «Comprobantes» de cada fila).

Probado el 28/10/2026 contra la API: los tres dueños nuevos (GET 200, POST 201); desde el panel se
subieron a un movimiento de caja un Word y un Excel reales, un Word sin tipo y un CSV como `text/plain`
(guardados con su tipo correcto), se descargó el Excel y se dieron de baja.
