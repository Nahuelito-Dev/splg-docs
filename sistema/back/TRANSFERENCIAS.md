# Pago por transferencia con comprobante (API v2)

Cuando un cliente elige pagar por transferencia, ve los datos bancarios de la distribuidora, transfiere
y sube el comprobante desde la app. El admin lo ve en el pedido y recién ahí confirma que el pago
llegó (antes confirmaba a ciegas).

## Endpoints

| Endpoint | Quién | Para |
|---|---|---|
| `GET/PUT /api/v2/distributor/bank-details` | admin, superadmin | Ver y cargar CBU, alias y titular de la cuenta |
| `GET /api/v2/orders/:id/bank-details` | cliente | Los datos bancarios para pagar ese pedido |
| `POST /api/v2/orders/:id/transfer-receipt` | cliente | Subir el comprobante (multipart, campo `file`) |
| `GET /api/v2/orders/:id/transfer-receipt` | cliente, admin, superadmin | Los comprobantes con su URL firmada |
| `PATCH /api/v1/orders/:id/payment/confirm-transfer` | admin, superadmin | Confirmar (`received: true`) o rechazar la transferencia, con motivo |

## Reglas

- **Datos bancarios**: CBU de 22 dígitos con sus dos dígitos verificadores, alias de 6 a 20 caracteres
  y titular de 2 a 120. Lo vacío se guarda como `null` y no se muestra. El panel valida igual que el
  back antes de guardar.
- **Comprobante**: imagen JPG, PNG o WEBP, o PDF (verificado por el contenido), hasta 10 MB y hasta 5
  por pedido. Sólo en un pedido propio, por transferencia, no cancelado y con el pago pendiente o
  marcado como no recibido (el comprobante sirve para corregirlo). Es idempotente con
  `Idempotency-Key`.
- **Historial y aviso**: cada comprobante deja una nota en el historial del pedido y avisa al panel en
  vivo (`order:transfer-receipt-uploaded` con `orderId`, `distributorId`, `customerId`,
  `attachmentId` y `uploadedAt`).
- **Archivos**: se guardan en S3 y se leen sólo con URL firmada que vence; el panel y la app la piden de
  nuevo antes de que caduque.

## App del cliente

En el detalle de un pedido por transferencia con el pago pendiente aparece la tarjeta «Pago por
transferencia»: titular, CBU y alias con «Copiar», y «Subir comprobante» (sacar foto, elegir de la
galería o elegir un PDF). La foto sale en JPEG sin metadatos; el PDF se mide antes de leerlo. Debajo
lista los comprobantes enviados. Si la distribuidora no cargó datos bancarios, lo dice y deja subir
igual.

## Panel

- **Configuración → Datos bancarios**: carga y edición, con la validación del CBU.
- **Detalle del pedido** (página y modal): tarjeta «Comprobantes de transferencia» con miniatura,
  nombre, fecha y «Abrir», sólo con los comprobantes que subió el cliente. Al lado está «Confirmar
  transferencia recibida».
- **Campana**: «El cliente subió el comprobante de transferencia», en vivo, filtrado por la
  distribuidora que se está mirando.

Probado de punta a punta el 28/10/2026: el admin cargó los datos bancarios (y el panel rechazó un CBU
con dígito verificador inválido), la clienta los vio en el iPhone y subió el comprobante desde la
galería, el panel lo mostró y avisó en vivo, y el admin confirmó la transferencia (el pedido quedó
pagado con su fecha de cobro).
