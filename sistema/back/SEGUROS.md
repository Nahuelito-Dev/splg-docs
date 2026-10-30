# Seguros de los vehículos

La distribuidora paga el seguro de cada vehículo mes a mes. El sistema guarda la aseguradora, la
póliza y su plan de cuotas, avisa antes de cada vencimiento y registra cada pago como un egreso de
Caja, con el comprobante asociado al vehículo.

## El circuito

1. **Aviso** (bandeja del admin y mail, a la hora del aviso de flota de cada distribuidora):
   - una cuota pendiente que vence en 5 días o menos;
   - una cuota con la gracia vencida;
   - una póliza que vence en 30 días o menos sin otra que la reemplace sin hueco.
   Cada aviso lleva a la pestaña **Seguro** de la ficha del vehículo.
2. **Pagar**: abre en otra pestaña el enlace de pago de la aseguradora y muestra el código de pago
   electrónico para copiar.
3. **Registrar pago**: el admin sube el comprobante (PDF, JPG, PNG o WEBP, hasta 10 MB) y **se escanea
   solo al subirlo**. El formulario aparece precargado con la fecha, el importe y el número de operación
   leídos. Sin escaneo («Escaneo no disponible: cargá los datos») se carga a mano.
4. **Guardar**: elige la caja o cuenta de la que salió el pago (efectivo con sesión abierta, banco o
   billetera). En una sola transacción la cuota queda paga y se registra el egreso en la categoría de
   sistema **Seguros**, con referencia a la cuota y el detalle «Seguro <patente> — <aseguradora>, cuota
   n/N». Una cuota paga es definitiva.

## Póliza y cuotas

- Una sola póliza vigente por vehículo en cada período: la base rechaza dos que se solapen.
- Al cargarla se generan las cuotas mensuales del plan: cantidad, importe, primer vencimiento y días
  de gracia. Vencen el mismo día de cada mes (si el mes no lo tiene, el último) y se pagan en término
  hasta el fin de la gracia. Una cuota pendiente se puede corregir: si cambia sólo el vencimiento, la
  gracia se corre igual.
- Cancelar una póliza (con motivo, baja lógica) cancela sus cuotas pendientes y conserva las pagas.
- Una aseguradora se da de baja sólo sin pólizas vigentes ni cuotas pendientes. Dada de baja, sigue
  apareciendo con su nombre en el historial.

## Integración con Flota

El seguro es un documento del vehículo en los planes de flota: un seguro vencido bloquea el despacho.
Al cargar una póliza, la tarea de seguro del vehículo queda con el vencimiento de la póliza.

- **Renovación sin hueco:** se cierra la tarea anterior y se crea la nueva.
- **Renovación que empieza más tarde:** no se toca nada. El período sin seguro bloquea, como
  corresponde. El aviso diario completa el cambio el día que empieza la nueva póliza.
- **Póliza ya vencida:** cargarla como historial no toca la flota.
- **Cancelar la póliza:** deshace lo que hizo en flota. Cancela la tarea que creó y reabre la anterior;
  si alguien la cambió mientras tanto, no la pisa y lo informa.

## API (v2)

| Endpoint | Para |
|---|---|
| `GET/POST/PATCH/DELETE /api/v2/insurers` | Aseguradoras (con enlace de pago; baja lógica) |
| `POST /api/v2/insurance-policies` | Póliza con su plan de cuotas; responde qué pasó en Flota |
| `PATCH /api/v2/insurance-policies/:id` · `POST …/:id/cancel` | Editar · cancelar con motivo |
| `GET /api/v2/cars/:carId/insurance` | Póliza vigente con sus cuotas e historial |
| `GET /api/v2/insurance-installments` · `PATCH …/:id` | Cuotas (por estado, fechas o vehículo) · corregir una pendiente |
| `POST /api/v2/insurance-installments/:id/receipt` | Subir el comprobante: guarda y escanea |
| `POST /api/v2/insurance-installments/:id/pay` | Pagar (con `Idempotency-Key`) |

El comprobante de una cuota entra sólo por su endpoint: el de adjuntos genéricos no lo acepta ni lo
da de baja. El escaneo tiene un tope de 30 segundos; si se pasa, el comprobante queda guardado igual.

## Panel

- Ficha del vehículo, pestaña **Seguro**: póliza vigente, código y enlace de pago, cuotas con su
  estado, «Pagar» y «Registrar pago». Las pagas muestran el comprobante y el movimiento de caja.
- **Flota → Aseguradoras**: alta, edición y baja.
- Carga de póliza con una vista previa de las cuotas, que marca en rojo si alguna cae fuera de la
  vigencia.

Probado el 28/10/2026 contra la API y en el panel, en escritorio y a 320 px:
- Seguros Rivadavia y la póliza 67/02/400118 de la Hilux AF218KT, con 6 cuotas de $29.958 que vencen
  el 22 con gracia hasta el 27;
- «Pagar» abrió el enlace;
- el comprobante se subió y mostró «Escaneo no disponible»;
- la cuota 1/6 quedó paga con un egreso de $29.958 por transferencia desde la cuenta «Banco Nación».

El escaneo real queda para cuando la API de Claude tenga crédito.
