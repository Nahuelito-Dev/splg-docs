# Ampliaciones v2

Los siguientes casos de uso amplían la documentación funcional de la versión 2. Se presentan fuera del catálogo y de los documentos numerados, que permanecen congelados.

## CU-349 — Configurar el Precio de un Envase

**Actores:** Administrador, Administrador General  
**Importancia:** Importante

### CUA — Caso de uso de alto nivel

| Campo | Detalle |
|---|---|
| Descripción | El administrador define el precio de venta del envase por tipo. |
| Subsistema | Catálogo e Inventario |

### CUE — Caso de uso expandido

| Campo | Detalle |
|---|---|
| Precondición | El administrador está identificado y el tipo pertenece a su distribuidora. |
| Postcondición | El precio de venta del envase queda vigente para los cobros posteriores. |
| Excepción | Si el tipo no existe, es ajeno o el importe no es válido, la operación se rechaza sin cambios. |
| Rendimiento | 1 segundo. |

**Secuencia normal**

1. El administrador indica el tipo de envase y su nuevo precio.
2. El sistema valida el importe y el alcance de la distribuidora.
3. El sistema guarda el precio vigente y muestra el tipo actualizado.

### Contrato del sistema

| Campo | Detalle |
|---|---|
| Operación | `configurarPrecioDeEnvase(tipoId, importe)` |
| Responsabilidad | Validar el tipo y actualizar su precio de envase. |
| Postcondición | El importe queda asociado al tipo de envase seleccionado. |

## CU-350 — Consultar la Cuenta de Envases de un Cliente

**Actores:** Administrador, Administrador General  
**Importancia:** Importante

### CUA — Caso de uso de alto nivel

| Campo | Detalle |
|---|---|
| Descripción | Consulta el saldo propio y el historial de envases del cliente por tipo. |
| Subsistema | Trazabilidad de Envases |

### CUE — Caso de uso expandido

| Campo | Detalle |
|---|---|
| Precondición | El administrador está identificado. |
| Postcondición | El administrador ve la cuenta; no se modifica ningún saldo. |
| Excepción | Si el cliente no existe o es ajeno, el sistema informa que no fue encontrado. |
| Rendimiento | 1 segundo. |

**Secuencia normal**

1. El administrador selecciona un cliente.
2. El sistema verifica que pertenezca a la distribuidora.
3. El sistema muestra saldo propio, envases pendientes y el historial por tipo.

### Contrato del sistema

No corresponde: la consulta no crea ni modifica información del modelo conceptual.

## CU-351 — Ajustar la Cuenta de Envases de un Cliente

**Actores:** Administrador, Administrador General  
**Importancia:** Importante

### CUA — Caso de uso de alto nivel

| Campo | Detalle |
|---|---|
| Descripción | Corrige el saldo con un movimiento inmutable y motivo. |
| Subsistema | Trazabilidad de Envases |

### CUE — Caso de uso expandido

| Campo | Detalle |
|---|---|
| Precondición | El administrador está identificado y el cliente pertenece a su distribuidora. |
| Postcondición | La cuenta refleja el ajuste y conserva el movimiento que lo justifica. |
| Excepción | Si faltan datos, el tipo o cliente es ajeno, el sistema rechaza el ajuste sin escribir. |
| Rendimiento | 1 segundo. |

**Secuencia normal**

1. El administrador indica cliente, tipo, ajuste y motivo.
2. El sistema valida los datos y el alcance.
3. El sistema registra el movimiento y recalcula el saldo.

### Contrato del sistema

| Campo | Detalle |
|---|---|
| Operación | `ajustarCuentaDeEnvases(clienteId, tipoId, cantidad, motivo)` |
| Responsabilidad | Registrar un movimiento de ajuste con su motivo. |
| Postcondición | Se crea un movimiento y el saldo de la cuenta se recalcula. |

## CU-352 — Cobrar los Envases Faltantes de un Pedido

**Actores:** Cliente, Administrador, Administrador General  
**Importancia:** Crítico

### CUA — Caso de uso de alto nivel

| Campo | Detalle |
|---|---|
| Descripción | Calcula y cobra los envases faltantes que pasan a ser propios del cliente. |
| Subsistema | Gestión de Pedidos |

### CUE — Caso de uso expandido

| Campo | Detalle |
|---|---|
| Precondición | Existe un pedido operable con envases faltantes. |
| Postcondición | Los envases cobrados dejan de ser reclamables y el cobro queda registrado. |
| Excepción | Si el pedido no admite el cobro, las cantidades no coinciden o el pago no se confirma, no se modifica la cuenta. |
| Rendimiento | 2 segundos, sin incluir el medio de pago. |

**Secuencia normal**

1. El cliente o administrador indica qué faltantes se cobrarán.
2. El sistema calcula las unidades y el precio vigente.
3. El solicitante confirma el medio de pago.
4. El sistema registra el cobro y acredita los envases como propios del cliente.

### Contrato del sistema

| Campo | Detalle |
|---|---|
| Operación | `cobrarEnvasesFaltantes(pedidoId, cantidades, medioPago)` |
| Responsabilidad | Registrar el cobro y acreditar la propiedad de los envases. |
| Postcondición | El cobro y los movimientos de la cuenta quedan registrados conjuntamente. |

## CU-353 — Declarar las Vacías Recibidas en una Entrega

**Actores:** Chofer  
**Importancia:** Importante

### CUA — Caso de uso de alto nivel

| Campo | Detalle |
|---|---|
| Descripción | Declara las vacías recibidas antes de confirmar la entrega. |
| Subsistema | Trazabilidad de Envases |

### CUE — Caso de uso expandido

| Campo | Detalle |
|---|---|
| Precondición | El chofer está asignado al pedido. |
| Postcondición | Las vacías declaradas quedan asociadas a la entrega y reducen el saldo pendiente. |
| Excepción | Si el pedido no está asignado, no puede entregarse o las cantidades son inválidas, se rechaza la declaración. |
| Rendimiento | 1 segundo. |

**Secuencia normal**

1. El chofer indica las vacías recibidas por tipo.
2. El sistema valida el pedido, su estado y las cantidades.
3. El sistema registra la devolución y actualiza la cuenta del cliente.

### Contrato del sistema

| Campo | Detalle |
|---|---|
| Operación | `declararVaciasRecibidas(pedidoId, cantidades)` |
| Responsabilidad | Registrar las vacías recibidas en una entrega asignada. |
| Postcondición | Se registra la devolución y se actualiza el saldo pendiente. |

## CU-354 — Leer y Conciliar Documentos Adjuntos

**Actor:** Sistema Automático  
**Importancia:** Importante

### CUA — Caso de uso de alto nivel

| Campo | Detalle |
|---|---|
| Descripción | Lee adjuntos, los concilia y genera propuestas revisables. |
| Subsistema | Lectura de Documentos |

### CUE — Caso de uso expandido

| Campo | Detalle |
|---|---|
| Precondición | Existe un adjunto admitido pendiente de lectura. |
| Postcondición | La lectura queda registrada; ningún efecto de negocio se ejecuta sin decisión administrativa. |
| Excepción | Sin lector disponible o sin conciliación posible, la corrida queda registrada para revisión. |
| Rendimiento | Proceso periódico que respeta el lote configurado. |

**Secuencia normal**

1. El proceso toma adjuntos pendientes dentro del lote configurado.
2. El sistema obtiene la lectura o registra que falló, es ilegible o duplicada.
3. El sistema concilia los datos con el dueño de la misma distribuidora.
4. Si corresponde, guarda una propuesta pendiente y avisa al administrador.

### Contrato del sistema

| Campo | Detalle |
|---|---|
| Operación | `leerYConciliarDocumentosAdjuntos()` |
| Responsabilidad | Registrar la lectura y proponer una acción revisable cuando corresponde. |
| Postcondición | La lectura queda registrada y una propuesta pendiente queda disponible para su decisión. |

## CU-355 — Resolver una Propuesta de Lectura

**Actores:** Administrador, Administrador General  
**Importancia:** Importante

### CUA — Caso de uso de alto nivel

| Campo | Detalle |
|---|---|
| Descripción | Confirma, corrige o rechaza una propuesta de lectura. |
| Subsistema | Lectura de Documentos |

### CUE — Caso de uso expandido

| Campo | Detalle |
|---|---|
| Precondición | El administrador está identificado y la propuesta pertenece a su distribuidora. |
| Postcondición | La propuesta queda resuelta; un pago confirmado y su egreso quedan juntos. |
| Excepción | Si la lectura es ajena, inexistente, vencida o ya fue resuelta, la operación se rechaza sin escribir. |
| Rendimiento | 2 segundos, sin contar reintentos del cliente. |

**Secuencia normal**

1. El administrador abre una propuesta pendiente.
2. Confirma los datos, los corrige o rechaza la propuesta con motivo.
3. El sistema valida los datos y la pertenencia.
4. El sistema registra la decisión y, si corresponde, sus efectos en una transacción.

### Contrato del sistema

| Campo | Detalle |
|---|---|
| Operación | `resolverPropuestaDeLectura(lecturaId, decision, datos)` |
| Responsabilidad | Validar la propuesta pendiente, registrar su decisión y ejecutar el efecto que corresponda. |
| Postcondición | La propuesta queda confirmada, corregida o rechazada; si hay pago, la decisión y el egreso quedan juntos. |
