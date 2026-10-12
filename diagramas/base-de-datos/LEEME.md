# Modelo de datos de SPLG — qué es cada archivo

Todo lo que hay en esta carpeta lo genera `generar-modelo-datos.py`, que está en
la raíz del repo y lee la base en ejecución (contenedor `splg-bd`). No se
edita nada a mano: si cambia la base, se vuelve a correr.

```bash
python3 generar-modelo-datos.py
```

## Los archivos

| Archivo | Qué es | Para qué sirve |
|---|---|---|
| `SPLG-base-de-datos.sql` | Volcado de `pg_dump`, esquema completo | Recrear la base tal cual está |
| `SPLG-base-de-datos-portable.sql` | Sólo lo implementado, en SQL portable | Diagramar el estado actual |
| `SPLG-base-de-datos-propuesta.sql` | Sólo lo planificado (los módulos de gestión) | Boceto de las migraciones que faltan |
| `SPLG-base-de-datos-completa-portable.sql` | Actual + planificado, en SQL portable | Ver todo el modelo en un solo SQL |
| `fisico/SPLG-fisico-NN-<contexto>.png` / `.svg` | Entidad-relación con tablas y columnas, una lámina por contexto de negocio | Las láminas técnicas |
| `conceptual/SPLG-der-NN-<área>.png` / `.svg` | Entidad-relación conceptual: una entidad por concepto del modelo conceptual, con sus atributos y las relaciones con su nombre | Las láminas para la defensa |
| `SPLG-der-mermaid.md` | El físico en Mermaid, por contexto | Lo que se pega en el Documento 3 §7.4.2 |
| `SPLG-modelo-de-datos.md` | Diccionario de datos y sustento escrito | El texto del informe |

En las láminas físicas, lo que ya está implementado va en blanco con borde oscuro y lo
propuesto —columnas planificadas que todavía no están en la base— en celeste, con el
marcador `<<propuesto>>`. Una tabla en gris es de otro contexto y sólo se muestra su nombre.
Los nombres reflejan la base real: conviven camelCase (`paymentMethod`) y snake_case
(`scheduled_date`), y la tabla `claims` está en plural; unificarlos exigiría renombrar
columnas en una base en uso.

Las láminas conceptuales usan el vocabulario del modelo conceptual (Documento 2, §1) y no el
de las tablas: la entidad se llama como el concepto y lleva sus atributos. La relación con
`distributor` de cada tabla no se dibuja; sí las que el modelo conceptual nombra.

## Correspondencia entre el modelo conceptual y el modelo de datos

| Concepto | Entidad | Tabla |
|---|---|---|
| Distribuidora | Distribuidora | `distributor` |
| Usuario | Usuario | `user` |
| Rol | Rol | `role` |
| Administrador | Administrador | `admin` |
| ConfiguracionModulo | ConfiguracionModulo | `module_config` |
| AsientoAuditoria | AsientoAuditoria | `audit_log` |
| Auditoria | Auditoria | `audit` |
| DetalleAuditoria | DetalleAuditoria | `audit_detail` |
| TipoAccionAuditoria | TipoAccionAuditoria | `audit_action_type` |
| Cliente | Cliente | `customer` |
| DireccionEntrega | DireccionEntrega | `user_address` |
| InvitacionRecompra | InvitacionRecompra | `repurchase_invitation` |
| ItemSugerido | — | — |
| Producto | Producto | `gas_cylinder` |
| Promocion | Promocion | `gas_cylinder_promotion` |
| Envase | Envase | `cylinder` |
| MovimientoEnvase | MovimientoEnvase | `cylinder_movement` |
| RevisionEnvase | RevisionEnvase | `cylinder_inspection` |
| CasoRecupero | CasoRecupero | `cylinder_recovery_case` |
| AvisoRecupero | AvisoRecupero | `cylinder_recovery_notice` |
| Carrito | Carrito | `cart` |
| ItemCarrito | ItemCarrito | `cart_item` |
| Pedido | Pedido | `order` |
| ItemPedido | ItemPedido | `order_item` |
| CambioEstadoPedido | CambioEstadoPedido | `order_status_history` |
| CambioDireccion | CambioDireccion | `order_address_change` |
| ZonaCobertura | ZonaCobertura | `coverage_zone` |
| FranjaHoraria | FranjaHoraria | `time_slot` |
| Pago | Pago | `payment` |
| PropuestaConVigencia | — | — |
| OfertaDespacho | OfertaDespacho | `order_dispatch_offer` |
| LoteRecorrido | LoteRecorrido | `route_batch` |
| ParadaLote | ParadaLote | `route_batch_stop` |
| OfertaLote | OfertaLote | `route_batch_offer` |
| Chofer | Chofer | `delivery` |
| Vehiculo | Vehiculo | `car` |
| AsignacionVehiculo | AsignacionVehiculo | `vehicle_assignment` |
| PlanMantenimiento | PlanMantenimiento | `maintenance_plan` |
| TareaMantenimiento | TareaMantenimiento | `maintenance_task` |
| AdjuntoTarea | AdjuntoTarea | `maintenance_task_attachment` |
| PropuestaVentanaTaller | PropuestaVentanaTaller | `maintenance_window_proposal` |
| UbicacionGPS | — | — |
| RegistroUsoVehiculo | RegistroUsoVehiculo | `vehicle_usage_log` |
| Reclamo | Reclamo | `claims` |
| Incidencia | Incidencia | `incident` |
| Calificacion | Calificacion | `rating` |
| PuestoDeTrabajo | PuestoDeTrabajo | `job_position` |
| Empleado | Empleado | `employee` |
| JornadaDeTrabajo | JornadaDeTrabajo | `employee_attendance` |
| LicenciaLaboral | LicenciaLaboral | `employee_leave` |
| Adjunto | Adjunto | `attachment` |
| CargaCombustible | CargaCombustible | `fuel_load` |
| MultaTransito | MultaTransito | `traffic_fine` |
| Siniestro | Siniestro | `vehicle_accident` |
| Neumatico | Neumatico | `tire` |
| MovimientoNeumatico | MovimientoNeumatico | `tire_event` |
| Deposito | Deposito | `warehouse` |
| UbicacionDeStock | UbicacionDeStock | `stock_location` |
| SaldoDeStock | SaldoDeStock | `stock_balance` |
| MovimientoDeStock | MovimientoDeStock | `stock_movement` |
| UmbralDeStock | UmbralDeStock | `stock_threshold` |
| AjusteDeStock | AjusteDeStock | `stock_adjustment` |
| ItemAjusteDeStock | ItemAjusteDeStock | `stock_adjustment_item` |
| CargaDeCamion | CargaDeCamion | `truck_load` |
| ItemCarga | ItemCarga | `truck_load_item` |
| Proveedor | Proveedor | `supplier` |
| OrdenDeCompra | OrdenDeCompra | `purchase_order` |
| ItemOrdenDeCompra | ItemOrdenDeCompra | `purchase_order_item` |
| RecepcionDeCompra | RecepcionDeCompra | `purchase_receipt` |
| ItemRecepcion | ItemRecepcion | `purchase_receipt_item` |
| Caja | Caja | `cash_box` |
| SesionDeCaja | SesionDeCaja | `cash_session` |
| CategoriaDeCaja | CategoriaDeCaja | `cash_category` |
| MovimientoDeCaja | MovimientoDeCaja | `cash_movement` |
| RendicionChofer | RendicionChofer | `driver_settlement` |
| PedidoRendido | PedidoRendido | `driver_settlement_order` |
| GastoDeRendicion | GastoDeRendicion | `driver_settlement_expense` |
| CuentaCorriente | CuentaCorriente | `customer_account` |
| AsientoCuentaCorriente | AsientoCuentaCorriente | `customer_account_entry` |
| ImputacionCuentaCorriente | ImputacionCuentaCorriente | `customer_account_allocation` |
| ReglaComision | ReglaComision | `commission_rule` |
| AsientoComision | AsientoComision | `commission_entry` |
| LiquidacionComisiones | LiquidacionComisiones | `driver_liquidation` |

Los conceptos sin tabla son PropuestaConVigencia (abstracto), UbicacionGPS (la columna
`delivery.actual_location`) e ItemSugerido (JSON dentro de `repurchase_invitation`).
`material-de-trabajo/verificar-mc-der.py` comprueba esta correspondencia contra la base.

`SPLG-base-de-datos-propuesta.sql` es PostgreSQL válido: agrega tipos, columnas
y tablas sobre el esquema que ya está, sin tocar los datos existentes.

## Diagramas en draw.io

Los cuatro modelos (conceptual, DER, base de datos físico y clases de diseño) están en `drawio/`, generados por
`generar-drawio.py` a partir de `SPLG-modelo.json`, que escribe este script leyendo la base. Ver `drawio/LEEME.md`.

## Qué pegarle a Gemini

Para que revise el modelo, el archivo que conviene pasarle es
**`SPLG-modelo-de-datos.md`**: es el único que trae, en un solo texto, el
diccionario de datos, las relaciones que faltan declarar y los agregados
pedidos, cada uno con el motivo por el que está.

Si además se quiere que revise el DDL, sumar
**`SPLG-base-de-datos-completa-portable.sql`**, que es el modelo entero en
menos de 55 KB.
No conviene pegar `SPLG-base-de-datos.sql`: son 137 KB
en su mayoría de índices y funciones de PostGIS que no aportan al análisis del
modelo.

Un pedido que funciona bien:

> Adjunto el modelo de datos de un sistema de pedidos y logística de garrafas de
> gas. Revisá normalización, integridad referencial, cardinalidades y nombres.
> Señalá redundancias y relaciones que falten. Tené en cuenta que la sección
> «Modelo propuesto» todavía no está implementada.
