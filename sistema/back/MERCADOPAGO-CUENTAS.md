# Cuenta de Mercado Pago por distribuidora (API v2)

Cada distribuidora puede cobrar con **su propia cuenta de Mercado Pago**. Si no cargó ninguna, se
cobra con la cuenta del sistema (las variables `MP_ACCESS_TOKEN` y `MP_WEBHOOK_SECRET` del entorno),
como hasta ahora.

## Endpoints

Rol `admin` de la distribuidora o `superadmin` con `X-Distributor`.

| Método | Ruta | Qué hace |
|---|---|---|
| `GET` | `/api/v2/distributor/mercadopago-credentials` | Estado: `source` (`own` o `system`), `active`, `encryptionConfigured`, los tres valores **enmascarados** y `verifiedAt` |
| `PUT` | `/api/v2/distributor/mercadopago-credentials` | Carga o reemplaza la cuenta (`accessToken`, `publicKey`, `webhookSecret`). Antes de guardar verifica el token contra Mercado Pago |
| `PUT` | `/api/v2/distributor/mercadopago-credentials/deactivate` | Baja lógica: la distribuidora vuelve a cobrar con la cuenta del sistema |

Errores: `400` cuerpo inválido · `404` desactivar sin cuenta propia · `409` dos cargas simultáneas ·
`422` Mercado Pago rechazó el token · `502` Mercado Pago no respondió · `503` el servidor no tiene la
clave de cifrado. En `422` y `502` no se guarda nada.

Panel: **Configuración → Mercado Pago**. Los campos son de tipo contraseña, nunca se precargan y sólo
se muestra el valor enmascarado.

## Cómo se guardan

- Tabla `distributor_mercadopago_credentials`. Los tres valores se guardan **cifrados con AES-256-GCM**
  (IV aleatorio por valor y tag de autenticación). La clave está en `CREDENTIALS_ENCRYPTION_KEY`
  (32 bytes en base64: `openssl rand -base64 32`). Sin la variable no se pueden cargar cuentas y todo
  cobra con la del sistema.
- Reemplazar crea una fila nueva y desactiva la anterior, en una transacción. Una sola activa por
  distribuidora (índice único parcial `WHERE active`).
- Ni la auditoría por triggers (columnas cifradas fuera del mapa) ni la auditoría HTTP (`webhookSecret`
  y `accessToken` depurados) guardan los valores en claro.
- Si se cambia la clave de cifrado, las cuentas guardadas no se pueden leer: hay que volver a cargarlas.

## Qué cuenta usa cada operación

Cada pago (`payment.credential_id`) guarda **con qué cuenta se cobró** (null = la del sistema). La
consulta del pago, el webhook, la comisión y la devolución usan siempre esa cuenta, aunque después la
distribuidora la haya reemplazado o desactivado. El checkout nuevo usa la cuenta activa.

El webhook es el mismo `POST /api/webhook/mercadopago`. Con cuenta propia, la `notification_url` lleva
`?account=<id de la cuenta>`: la firma se valida con el secreto de esa cuenta y el pago se consulta con
su token. Antes de escribir, dentro de la transacción, se compara esa cuenta con la del intento de cobro
del pedido: si no coinciden (otra distribuidora, la cuenta del sistema contra un cobro con cuenta propia,
o una cuenta propia sin intento de cobro), el aviso se registra y se descarta sin tocar el pedido.

La conciliación (`FINANZAS.md`) pide los reportes con la cuenta vigente de la distribuidora; si no se
puede leer, la corrida termina `failed` con el motivo.

## Pendiente

- La clave pública se guarda pero todavía no la usan las apps.
- La conciliación de un rango que cruza un reemplazo de cuenta sólo trae los movimientos de la cuenta
  vigente.
- Al regenerar un checkout (todavía no existe), el intento de cobro a tomar tiene que filtrarse por cuenta.
- El caso feliz de la carga sólo está probado con Mercado Pago simulado: falta probarlo con una cuenta real.
