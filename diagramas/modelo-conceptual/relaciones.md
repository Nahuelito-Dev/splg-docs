| Relación | Concepto A | Concepto B | Tipo | Multiplicidad | Categoría (Larman) |
|----------|-----------|-----------|------|---------------|---------------------|
| Es un tipo de | Cliente | Usuario | Especialización | — | — |
| Es un tipo de | Chofer | Usuario | Especialización | — | — |
| Es un tipo de | Administrador | Usuario | Especialización | — | — |
| Es un tipo de | OfertaDespacho | PropuestaConVigencia | Especialización | — | — |
| Es un tipo de | OfertaLote | PropuestaConVigencia | Especialización | — | — |
| Es un tipo de | PropuestaVentanaTaller | PropuestaConVigencia | Especialización | — | — |
| Es un tipo de | InvitacionRecompra | PropuestaConVigencia | Especialización | — | — |
| Es un tipo de | AvisoRecupero | PropuestaConVigencia | Especialización | — | — |
| Tiene asignado | Usuario | Rol | Asociación | 0..* a 0..1 | Descripción para |
| Emplea | Distribuidora | Chofer | Asociación | 1 a 0..* | Es miembro de / empleado de |
| Emplea | Distribuidora | Administrador | Asociación | 0..1 a 0..* | Es miembro de / empleado de |
| Emplea | Distribuidora | Empleado | Asociación | 1 a 0..* | Es miembro de / empleado de |
| Define | Distribuidora | PuestoDeTrabajo | Composición | 1 a 0..* | Parte lógica de |
| Comercializa | Distribuidora | Producto | Asociación | 1 a 0..* | Usa o gestiona |
| Posee | Distribuidora | Envase | Asociación | 1 a 0..* | Es propiedad de |
| Gestiona | Distribuidora | Pedido | Asociación | 1 a 0..* | Usa o gestiona |
| Define | Distribuidora | ZonaCobertura | Composición | 1 a 0..* | Parte lógica de |
| Define | Distribuidora | FranjaHoraria | Composición | 1 a 0..* | Parte lógica de |
| Parametriza | Distribuidora | ConfiguracionModulo | Composición | 1 a 0..* | Descripción para |
| Origina | Usuario | AsientoAuditoria | Asociación | 0..1 a 0..* | Es un registro de |
| Realiza | Usuario | Auditoria | Asociación | 0..1 a 0..* | Es un registro de |
| Delimita | Distribuidora | Auditoria | Asociación | 0..1 a 0..* | Es un registro de |
| Detalla con | Auditoria | DetalleAuditoria | Composición | 1 a 0..* | Es una línea de transacción de |
| Clasifica | TipoAccionAuditoria | Auditoria | Asociación | 1 a 0..* | Descripción para |
| Registra | Cliente | DireccionEntrega | Composición | 1 a 0..* | Parte lógica de |
| Realiza | Cliente | Pedido | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Arma | Cliente | Carrito | Composición | 1 a 0..* | Está relacionado con una transacción |
| Recibe | Cliente | InvitacionRecompra | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Usa habitualmente | Cliente | Producto | Asociación | 0..* a 0..1 | Usa o gestiona |
| Se convierte en | InvitacionRecompra | Pedido | Asociación | 0..1 a 0..1 | Está relacionado con una transacción |
| Sugiere | InvitacionRecompra | ItemSugerido | Composición | 1 a 1..* | Es una línea de transacción de |
| Sugiere entregar en | InvitacionRecompra | DireccionEntrega | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Corresponde a | ItemSugerido | Producto | Asociación | 0..* a 1 | Descripción para |
| Contiene | Carrito | ItemCarrito | Composición | 1 a 0..* | Es una línea de transacción de |
| Corresponde a | ItemCarrito | Producto | Asociación | 0..* a 1 | Descripción para |
| Contiene | Pedido | ItemPedido | Composición | 1 a 1..* | Es una línea de transacción de |
| Corresponde a | ItemPedido | Producto | Asociación | 0..* a 1 | Descripción para |
| Se entrega en | Pedido | DireccionEntrega | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Se programa en | Pedido | FranjaHoraria | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Aplica el recargo de | Pedido | ZonaCobertura | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Registra | Pedido | CambioEstadoPedido | Composición | 1 a 0..* | Es un registro de |
| Efectúa | Usuario | CambioEstadoPedido | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Confirmó el cobro de | Usuario | Pedido | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Resolvió el cobro de | Usuario | Pedido | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Registra | Pedido | CambioDireccion | Composición | 1 a 0..* | Es un registro de |
| Cambia desde | CambioDireccion | DireccionEntrega | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Cambia hacia | CambioDireccion | DireccionEntrega | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Realiza | Usuario | CambioDireccion | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Entrega | Chofer | Pedido | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Se salda con | Pedido | Pago | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Genera | Pedido | OfertaDespacho | Composición | 1 a 0..* | Está relacionado con una transacción |
| Se dirige a | OfertaDespacho | Chofer | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Se compone de | LoteRecorrido | ParadaLote | Composición | 1 a 1..* | Parte física de |
| Atiende | ParadaLote | Pedido | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Genera | LoteRecorrido | OfertaLote | Composición | 1 a 0..* | Está relacionado con una transacción |
| Se dirige a | OfertaLote | Chofer | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Acepta | Chofer | LoteRecorrido | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Tiene registrado | Chofer | Vehiculo | Asociación (clase de asociación AsignacionVehiculo) | 1 a 0..* | Usa o gestiona |
| Usa | Chofer | Vehiculo | Asociación (clase de asociación AsignacionVehiculo) | 0..* a 0..* | Usa o gestiona |
| Se ubica en | Chofer | UbicacionGPS | Asociación | 1 a 0..1 | Descripción para |
| Genera | PlanMantenimiento | TareaMantenimiento | Asociación | 1 a 0..* | Es un registro de |
| Habilita | TareaMantenimiento | Vehiculo | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Habilita | TareaMantenimiento | Chofer | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Origina | TareaMantenimiento | PropuestaVentanaTaller | Composición | 1 a 0..* | Está relacionado con una transacción |
| Adjunta | TareaMantenimiento | AdjuntoTarea | Composición | 1 a 0..* | Parte lógica de |
| Se dirige a | PropuestaVentanaTaller | Chofer | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Acumula | Vehiculo | RegistroUsoVehiculo | Composición | 1 a 0..* | Es un registro de |
| Ofrece | Producto | Promocion | Composición | 1 a 0..* | Descripción para |
| Describe | Producto | Envase | Asociación | 0..1 a 0..* | Descripción para |
| Registra | Envase | MovimientoEnvase | Composición | 1 a 0..* | Es un registro de |
| Se somete a | Envase | RevisionEnvase | Composición | 1 a 0..* | Es un registro de |
| Origina | Pedido | MovimientoEnvase | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Ejecuta | Usuario | MovimientoEnvase | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Tiene en su poder | Cliente | Envase | Asociación | 0..1 a 0..* | Es propiedad de / está en poder de |
| Despacha | Pedido | Envase | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Motiva | Envase | CasoRecupero | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Se abre contra | CasoRecupero | Cliente | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Resuelve | Usuario | CasoRecupero | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Emite | CasoRecupero | AvisoRecupero | Composición | 1 a 0..* | Es un registro de |
| Ocupa | Empleado | PuestoDeTrabajo | Asociación | 0..* a 1 | Descripción para |
| Accede con | Empleado | Usuario | Asociación | 0..1 a 0..1 | Usa o gestiona |
| Registra | Empleado | JornadaDeTrabajo | Composición | 1 a 0..* | Es un registro de |
| Solicita | Empleado | LicenciaLaboral | Composición | 1 a 0..* | Está relacionado con una transacción |
| Resuelve | Usuario | LicenciaLaboral | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Conserva | Empleado | Adjunto | Composición | 1 a 0..* | Parte lógica de |
| Habilita | TareaMantenimiento | Empleado | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Registra | Vehiculo | CargaCombustible | Composición | 1 a 0..* | Es un registro de |
| Acumula | Vehiculo | MultaTransito | Composición | 1 a 0..* | Es un registro de |
| Sufre | Vehiculo | Siniestro | Composición | 1 a 0..* | Es un registro de |
| Monta | Vehiculo | Neumatico | Asociación | 0..1 a 0..* | Usa o gestiona |
| Posee | Distribuidora | Neumatico | Composición | 1 a 0..* | Es propiedad de |
| Registra | Neumatico | MovimientoNeumatico | Composición | 1 a 0..* | Es un registro de |
| Ocurre en | MovimientoNeumatico | Vehiculo | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Carga | Empleado | CargaCombustible | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Responde por | Empleado | MultaTransito | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Interviene en | Empleado | Siniestro | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Origina | Pedido | Reclamo | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Presenta | Cliente | Reclamo | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Origina | Pedido | Incidencia | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Reporta | Usuario | Incidencia | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Recibe | Pedido | Calificacion | Asociación | 1 a 0..2 | Está relacionado con una transacción |
| Emite | Usuario | Calificacion | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Recibe | Usuario | Calificacion | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Dispone de | Distribuidora | Deposito | Asociación | 1 a 0..* | Es propiedad de |
| Compra a | Distribuidora | Proveedor | Asociación | 1 a 0..* | Usa o gestiona |
| Se registra como {xor} | Deposito | UbicacionDeStock | Asociación | 1 a 0..1 | Descripción para |
| Se registra como {xor} | Vehiculo | UbicacionDeStock | Asociación | 1 a 0..1 | Descripción para |
| Acumula | UbicacionDeStock | SaldoDeStock | Composición | 1 a 0..* | Es un registro de |
| Corresponde a | SaldoDeStock | Producto | Asociación | 0..* a 1 | Descripción para |
| Corresponde a | MovimientoDeStock | Producto | Asociación | 0..* a 1 | Descripción para |
| Sale de | MovimientoDeStock | UbicacionDeStock | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Entra en | MovimientoDeStock | UbicacionDeStock | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Ejecuta | Usuario | MovimientoDeStock | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Fija | Deposito | UmbralDeStock | Composición | 1 a 0..* | Parte lógica de |
| Controla | UmbralDeStock | Producto | Asociación | 0..* a 1 | Descripción para |
| Se corrige con | UbicacionDeStock | AjusteDeStock | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Contiene | AjusteDeStock | ItemAjusteDeStock | Composición | 1 a 1..* | Es una línea de transacción de |
| Corresponde a | ItemAjusteDeStock | Producto | Asociación | 0..* a 1 | Descripción para |
| Registra | Usuario | AjusteDeStock | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Corrige a | MovimientoDeStock | MovimientoDeStock | Asociación | 0..1 a 0..1 | Está relacionado con una transacción |
| Recibe | Proveedor | OrdenDeCompra | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Se destina a | OrdenDeCompra | Deposito | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Contiene | OrdenDeCompra | ItemOrdenDeCompra | Composición | 1 a 1..* | Es una línea de transacción de |
| Corresponde a | ItemOrdenDeCompra | Producto | Asociación | 0..* a 1 | Descripción para |
| Emite | Usuario | OrdenDeCompra | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Entrega | Proveedor | RecepcionDeCompra | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Se cumple con | OrdenDeCompra | RecepcionDeCompra | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Ingresa en | RecepcionDeCompra | Deposito | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Contiene | RecepcionDeCompra | ItemRecepcion | Composición | 1 a 1..* | Es una línea de transacción de |
| Corresponde a | ItemRecepcion | Producto | Asociación | 0..* a 1 | Descripción para |
| Registra | Usuario | RecepcionDeCompra | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Transporta | Vehiculo | CargaDeCamion | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Reparte con | Chofer | CargaDeCamion | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Parte de | CargaDeCamion | UbicacionDeStock | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Contiene | CargaDeCamion | ItemCarga | Composición | 1 a 1..* | Es una línea de transacción de |
| Corresponde a | ItemCarga | Producto | Asociación | 0..* a 1 | Descripción para |
| Abre | Usuario | CargaDeCamion | Asociación | 1 a 0..* | Está relacionado con una transacción |
| Cierra | Usuario | CargaDeCamion | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Ayuda en | Empleado | CargaDeCamion | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Define | Distribuidora | Caja | Composición | 1 a 0..* | Parte lógica de |
| Define | Distribuidora | CategoriaDeCaja | Composición | 1 a 0..* | Parte lógica de |
| Lleva | Distribuidora | CuentaCorriente | Composición | 1 a 0..* | Parte lógica de |
| Define | Distribuidora | ReglaComision | Composición | 1 a 0..* | Parte lógica de |
| Registra | Caja | SesionDeCaja | Composición | 1 a 0..* | Es un registro de |
| Asienta | Caja | MovimientoDeCaja | Composición | 1 a 0..* | Es un registro de |
| Agrupa | SesionDeCaja | MovimientoDeCaja | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Clasifica | CategoriaDeCaja | MovimientoDeCaja | Asociación | 1 a 0..* | Descripción para |
| Anula a | MovimientoDeCaja | MovimientoDeCaja | Asociación | 0..1 a 0..1 | Está relacionado con una transacción |
| Presenta | Chofer | RendicionChofer | Composición | 1 a 0..* | Está relacionado con una transacción |
| Ingresa en | RendicionChofer | Caja | Asociación | 0..* a 0..1 | Está relacionado con una transacción |
| Genera | RendicionChofer | MovimientoDeCaja | Asociación | 0..1 a 0..1 | Está relacionado con una transacción |
| Rinde | RendicionChofer | PedidoRendido | Composición | 1 a 0..* | Es una línea de transacción de |
| Corresponde a | PedidoRendido | Pedido | Asociación | 0..1 a 1 | Descripción para |
| Declara | RendicionChofer | GastoDeRendicion | Composición | 1 a 0..* | Es una línea de transacción de |
| Se clasifica en | GastoDeRendicion | CategoriaDeCaja | Asociación | 0..* a 1 | Descripción para |
| Tiene habilitada | Cliente | CuentaCorriente | Asociación | 1 a 0..* | Usa o gestiona |
| Registra | CuentaCorriente | AsientoCuentaCorriente | Composición | 1 a 0..* | Es un registro de |
| Origina | Pedido | AsientoCuentaCorriente | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Se asienta en | AsientoCuentaCorriente | MovimientoDeCaja | Asociación | 0..1 a 0..1 | Está relacionado con una transacción |
| Cobra | Chofer | AsientoCuentaCorriente | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Incluye | RendicionChofer | AsientoCuentaCorriente | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Anula a | AsientoCuentaCorriente | AsientoCuentaCorriente | Asociación | 0..1 a 0..1 | Está relacionado con una transacción |
| Salda | ImputacionCuentaCorriente | AsientoCuentaCorriente | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Se aplica con | ImputacionCuentaCorriente | AsientoCuentaCorriente | Asociación | 0..* a 1 | Está relacionado con una transacción |
| Se aplica a | ReglaComision | Empleado | Asociación | 0..* a 0..1 | Descripción para |
| Se aplica a | ReglaComision | Producto | Asociación | 0..* a 0..1 | Descripción para |
| Devenga | Empleado | AsientoComision | Composición | 1 a 0..* | Es un registro de |
| Percibe | Empleado | LiquidacionComisiones | Composición | 1 a 0..* | Está relacionado con una transacción |
| Actúa como | Empleado | Chofer | Asociación | 0..1 a 0..1 | Usa o gestiona |
| Corresponde a | AsientoComision | Pedido | Asociación | 0..* a 0..1 | Descripción para |
| Determina | ReglaComision | AsientoComision | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Incluye | LiquidacionComisiones | AsientoComision | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Origina | RendicionChofer | AsientoComision | Asociación | 0..1 a 0..* | Está relacionado con una transacción |
| Se paga con | LiquidacionComisiones | MovimientoDeCaja | Asociación | 0..1 a 0..1 | Está relacionado con una transacción |
