# Índice de imágenes para el Drive

Cada imagen lleva el código y el nombre del caso de uso, para ubicarla sin abrir el archivo.
Las imágenes están en `diagramas/png/` y `diagramas/uml/`; hay una versión vectorial de cada
una en `svg/`, que conviene si hay que ampliarla.

## Dónde va cada tipo

| Imagen | Documento | Sección |
|---|---|---|
| `CU_Sistema_*` | 0 — Plan del Proyecto · 1 — Requisitos | §6 · §3 |
| `CU_SS-*` | 1 — Requisitos | §4.3 Diagramas de Casos de Uso por Subsistema |
| `DSS_*` | 2 — Análisis | §2.1 Diagramas de Secuencia del Sistema |
| `DSD_*` | 3 — Diseño | §4 Diagramas de Interacción |

## Diagramas en notación UML

| Archivo |
|---|
| `CU_SS-01_Autenticacion-Y-Usuarios.png` |
| `CU_SS-02_Gestion-De-Pedidos_Parte-1.png` |
| `CU_SS-02_Gestion-De-Pedidos_Parte-2.png` |
| `CU_SS-03_Despacho-Y-Asignacion.png` |
| `CU_SS-04_Seguimiento-En-Tiempo-Real.png` |
| `CU_SS-05_Reclamos.png` |
| `CU_SS-06_Reportes-Y-Dashboard.png` |
| `CU_SS-07_Choferes.png` |
| `CU_SS-07_Costos-Siniestros-Y-Adjuntos.png` |
| `CU_SS-07_Vehiculos.png` |
| `CU_SS-08_Gestion-De-Productos_Parte-1.png` |
| `CU_SS-08_Gestion-De-Productos_Parte-2.png` |
| `CU_SS-09_Franjas-Horarias.png` |
| `CU_SS-10_Multi-Distribuidora.png` |
| `CU_SS-11_Cobertura-Geografica.png` |
| `CU_SS-12_Incidencias-Y-Calidad-De-Servicio.png` |
| `CU_SS-13_Trazabilidad-De-Envases.png` |
| `CU_SS-14_Pagos-Y-Conciliacion.png` |
| `CU_SS-15_Reservas-Programadas.png` |
| `CU_SS-16_Administracion-De-Cuentas-Y-Roles.png` |
| `CU_SS-17_Notificaciones-Y-Mensajeria.png` |
| `CU_SS-18_Observabilidad-Y-Operacion.png` |
| `CU_SS-19_Personal-Y-Legajos.png` |
| `CU_SS-20_Compras.png` |
| `CU_SS-21_Caja-Rendiciones-Y-Cuentas-Corrientes.png` |
| `CU_Sistema_Actores.png` |
| `CU_Sistema_Completo-Lamina-01_Cliente_Parte-1.png` |
| `CU_Sistema_Completo-Lamina-02_Cliente_Parte-2.png` |
| `CU_Sistema_Completo-Lamina-03_Cliente_Parte-3.png` |
| `CU_Sistema_Completo-Lamina-04_Chofer_Parte-1.png` |
| `CU_Sistema_Completo-Lamina-05_Chofer_Parte-2.png` |
| `CU_Sistema_Completo-Lamina-06_Administrador_Parte-1.png` |
| `CU_Sistema_Completo-Lamina-07_Administrador_Parte-2.png` |
| `CU_Sistema_Completo-Lamina-08_Administrador_Parte-3.png` |
| `CU_Sistema_Completo-Lamina-09_Administrador_Parte-4.png` |
| `CU_Sistema_Completo-Lamina-10_Administrador_Parte-5.png` |
| `CU_Sistema_Completo-Lamina-11_Administrador_Parte-6.png` |
| `CU_Sistema_Completo-Lamina-12_Administrador_Parte-7.png` |
| `CU_Sistema_Completo-Lamina-13_Administrador_Parte-8.png` |
| `CU_Sistema_Completo-Lamina-14_Administrador_Parte-9.png` |
| `CU_Sistema_Completo-Lamina-15_Administrador_Parte-10.png` |
| `CU_Sistema_Completo-Lamina-16_Administrador_Parte-11.png` |
| `CU_Sistema_Completo-Lamina-17_Administrador_Parte-12.png` |
| `CU_Sistema_Completo-Lamina-18_Administrador-General_Parte-1.png` |
| `CU_Sistema_Completo-Lamina-19_Administrador-General_Parte-2.png` |
| `CU_Sistema_Completo-Lamina-20_Administrador-General_Parte-3.png` |
| `CU_Sistema_Completo-Lamina-21_Sistema-Automatico.png` |
| `CU_Sistema_Completo-Lamina-22_Operador-Tecnico.png` |
| `CU_Sistema_Completo-Lamina-23_MercadoPago.png` |
| `CU_Sistema_Completo-Lamina-24_Firebase.png` |
| `CU_Sistema_Completo-Lamina-25_Servicio-De-Correo.png` |
| `CU_Sistema_Completo-Lamina-26_Plataforma-De-Despliegue.png` |
| `CU_Sistema_Diagrama-Completo.png` |
| `CU_Sistema_Diagrama-De-Contexto.png` |
| `CU_Sistema_Diagrama-De-Subsistemas.png` |
| `CU_Sistema_Mapa.png` |
| `CU_Sistema_Subsistemas.png` |

## Por caso de uso

| CU | Caso de uso | DSS | DSD |
|---|---|---|---|
| CU-001 | Iniciar Sesión | `DSS_CU-001_Iniciar-Sesion.png` | `DSD_CU-001_iniciarSesion.png` |
| CU-002 | Registrarse como Cliente | `DSS_CU-002_Registrarse-Como-Cliente.png` | `DSD_CU-002_registrarse.png` |
| CU-004 | Consultar el Perfil de Usuario | `DSS_CU-004_Consultar-el-Perfil-de-Usuario.png` | `DSD_CU-004_consultarPerfil.png` · `DSD_CU-004_consultarPerfilCliente.png` |
| CU-005 | Crear un Pedido | `DSS_CU-005_Crear-un-Pedido.png` | `DSD_CU-005_crearPedido.png` |
| CU-006 | Consultar el Detalle de un Pedido | `DSS_CU-006_Consultar-el-Detalle-de-un-Pedido.png` | `DSD_CU-006_consultarPedido.png` |
| CU-007 | Consultar el Historial de Pedidos | `DSS_CU-007_Consultar-el-Historial-de-Pedidos.png` | `DSD_CU-007_consultarHistorialDePedidos.png` |
| CU-008 | Cancelar un Pedido (Cliente) | `DSS_CU-008_Cancelar-un-Pedido.png` | `DSD_CU-008_cancelarMiPedido.png` |
| CU-009 | Liberar un Pedido (Chofer) | `DSS_CU-009_Liberar-un-Pedido.png` | `DSD_CU-009_liberarPedido.png` |
| CU-010 | Cancelar un Pedido (Administrador) | `DSS_CU-010_Cancelar-un-Pedido.png` | `DSD_CU-010_cancelarPedido.png` |
| CU-011 | Consultar Todos los Pedidos | `DSS_CU-011_Consultar-Todos-Los-Pedidos.png` | `DSD_CU-011_listarPedidos.png` |
| CU-012 | Asignar un Chofer Manualmente | `DSS_CU-012_Asignar-un-Chofer-Manualmente.png` | `DSD_CU-012_asignarChoferAPedido.png` |
| CU-013 | Asignar un Pedido Automáticamente por Proximidad | `DSS_CU-013_Asignar-un-Pedido-Automaticamente-por-Proximidad.png` | `DSD_CU-013_ofrecerAlSiguienteChofer.png` |
| CU-014 | Vencer la Oferta y Ofrecer al Siguiente Chofer | `DSS_CU-014_Vencer-la-Oferta-y-Ofrecer-al-Siguiente-Chofer.png` | `DSD_CU-014_vencerOfertasExpiradas.png` |
| CU-015 | Aceptar un Pedido | `DSS_CU-015_Aceptar-un-Pedido.png` | `DSD_CU-015_aceptarPedido.png` |
| CU-016 | Rechazar un Pedido Ofrecido | `DSS_CU-016_Rechazar-un-Pedido-Ofrecido.png` | `DSD_CU-016_rechazarOferta.png` |
| CU-017 | Modificar la Ubicación GPS del Chofer | `DSS_CU-017_Modificar-la-Ubicacion-GPS-del-Chofer.png` | `DSD_CU-017_actualizarUbicacion.png` |
| CU-018 | Marcar un Pedido "En Camino" | `DSS_CU-018_Marcar-un-Pedido-En-Camino.png` | `DSD_CU-018_marcarPedidoEnCamino.png` |
| CU-019 | Avisar la Llegada al Cliente | `DSS_CU-019_Avisar-la-Llegada-al-Cliente.png` | `DSD_CU-019_avisarLlegada.png` |
| CU-020 | Confirmar una Entrega Manualmente | `DSS_CU-020_Confirmar-una-Entrega-Manualmente.png` | `DSD_CU-020_confirmarEntrega.png` |
| CU-022 | Activar la Disponibilidad | `DSS_CU-022_Activar-la-Disponibilidad.png` | `DSD_CU-022_activarDisponibilidad.png` |
| CU-023 | Registrar un Reclamo | `DSS_CU-023_Registrar-un-Reclamo.png` | `DSD_CU-023_registrarReclamo.png` |
| CU-024 | Consultar los Reclamos | `DSS_CU-024_Consultar-los-Reclamos.png` | `DSD_CU-024_listarReclamos.png` |
| CU-025 | Resolver un Reclamo | `DSS_CU-025_Resolver-un-Reclamo.png` | `DSD_CU-025_resolverReclamo.png` |
| CU-026 | Consultar el Tablero General | `DSS_CU-026_Consultar-el-Tablero-General.png` | `DSD_CU-026_consultarGraficoDeVentas.png` · `DSD_CU-026_consultarResumenDePedidos.png` |
| CU-027 | Consultar el Reporte de Ventas por Chofer | `DSS_CU-027_Consultar-el-Reporte-de-Ventas-por-Chofer.png` | `DSD_CU-027_consultarVentasPorChofer.png` |
| CU-028 | Consultar el Reporte de Ventas por Producto | `DSS_CU-028_Consultar-el-Reporte-de-Ventas-por-Producto.png` | `DSD_CU-028_consultarVentasPorProducto.png` |
| CU-029 | Consultar el Reporte por Método de Pago | `DSS_CU-029_Consultar-el-Reporte-por-Metodo-de-Pago.png` | `DSD_CU-029_consultarVentasPorMetodoDePago.png` |
| CU-030 | Consultar el Gráfico de Ventas (últimos 7 días) | `DSS_CU-030_Consultar-el-Grafico-de-Ventas.png` | `DSD_CU-030_consultarEvolucionDeVentas.png` |
| CU-031 | Registrar un Chofer (Gestión de la Flota) | `DSS_CU-031_Registrar-un-Chofer.png` | `DSD_CU-031_registrarChoferEnLaFlota.png` |
| CU-032 | Validar un Chofer | `DSS_CU-032_Validar-un-Chofer.png` | `DSD_CU-032_validarChofer.png` |
| CU-033 | Activar un Chofer | `DSS_CU-033_Activar-un-Chofer.png` | `DSD_CU-033_activarChofer.png` |
| CU-034 | Registrar un Vehículo del Chofer | `DSS_CU-034_Registrar-un-Vehiculo-del-Chofer.png` | `DSD_CU-034_registrarVehiculo.png` |
| CU-035 | Consultar el Listado de Choferes | `DSS_CU-035_Consultar-el-Listado-de-Choferes.png` | `DSD_CU-035_listarChoferes.png` · `DSD_CU-035_listarChoferesActivos.png` |
| CU-036 | Crear un Producto (Garrafa) | `DSS_CU-036_Crear-un-Producto.png` | `DSD_CU-036_crearProducto.png` |
| CU-037 | Modificar el Precio de un Producto | `DSS_CU-037_Modificar-el-Precio-de-un-Producto.png` | `DSD_CU-037_actualizarPrecioDelProducto.png` |
| CU-038 | Modificar el Stock de un Producto | `DSS_CU-038_Modificar-el-Stock-de-un-Producto.png` | `DSD_CU-038_actualizarStock.png` |
| CU-039 | Configurar las Promociones por Cantidad | `DSS_CU-039_Configurar-las-Promociones-por-Cantidad.png` | `DSD_CU-039_configurarPromocionesDelProducto.png` |
| CU-040 | Desactivar un Producto | `DSS_CU-040_Desactivar-un-Producto.png` | `DSD_CU-040_desactivarProducto.png` |
| CU-041 | Consultar el Catálogo de Productos (Cliente) | `DSS_CU-041_Consultar-el-Catalogo-de-Productos-Cliente.png` | `DSD_CU-041_consultarProducto.png` · `DSD_CU-041_consultarProductosDisponibles.png` |
| CU-042 | Crear una Franja Horaria | `DSS_CU-042_Crear-una-Franja-Horaria.png` | `DSD_CU-042_crearFranjaHoraria.png` |
| CU-043 | Modificar una Franja Horaria | `DSS_CU-043_Modificar-una-Franja-Horaria.png` | `DSD_CU-043_modificarFranjaHoraria.png` |
| CU-044 | Seleccionar una Franja Horaria al Crear un Pedido | `DSS_CU-044_Seleccionar-una-Franja-Horaria-al-Crear-un-Pedido.png` | `DSD_CU-044_validarFranjaDelPedido.png` |
| CU-045 | Consultar las Franjas Horarias Disponibles | `DSS_CU-045_Consultar-las-Franjas-Horarias-Disponibles.png` | `DSD_CU-045_consultarDisponibilidadDeFranjas.png` · `DSD_CU-045_listarFranjas.png` |
| CU-046 | Consultar las Direcciones de Entrega del Cliente | `DSS_CU-046_Consultar-las-Direcciones-de-Entrega-del-Cliente.png` | `DSD_CU-046_consultarDireccionesDeEntrega.png` |
| CU-047 | Recuperar la Contraseña | `DSS_CU-047_Recuperar-la-Contrasena.png` | `DSD_CU-047_solicitarRecuperacionDeClave.png` |
| CU-048 | Procesar el Pago con MercadoPago | `DSS_CU-048_Procesar-el-Pago-con-MercadoPago.png` | `DSD_CU-048_crearCheckoutDePago.png` · `DSD_CU-048_notificarResultadoDePago.png` |
| CU-049 | Consultar las Ganancias del Chofer | `DSS_CU-049_Consultar-las-Ganancias-del-Chofer.png` | `DSD_CU-049_consultarPerfilDelChofer.png` |
| CU-050 | Bloquear un Usuario | `DSS_CU-050_Bloquear-un-Usuario.png` | `DSD_CU-050_bloquearUsuario.png` |
| CU-051 | Consultar el Listado de Vehículos | `DSS_CU-051_Consultar-el-Listado-de-Vehiculos.png` | `DSD_CU-051_listarVehiculos.png` |
| CU-052 | Registrar una Distribuidora | `DSS_CU-052_Registrar-una-Distribuidora.png` | `DSD_CU-052_registrarDistribuidora.png` |
| CU-053 | Consultar las Distribuidoras | `DSS_CU-053_Consultar-las-Distribuidoras.png` | `DSD_CU-053_consultarDistribuidora.png` · `DSD_CU-053_listarDistribuidoras.png` |
| CU-054 | Modificar los Datos de una Distribuidora | `DSS_CU-054_Modificar-los-Datos-de-una-Distribuidora.png` | `DSD_CU-054_modificarDistribuidora.png` |
| CU-055 | Dar de Baja una Distribuidora | `DSS_CU-055_Dar-De-Baja-Una-Distribuidora.png` | `DSD_CU-055_darDeBajaDistribuidora.png` |
| CU-056 | Crear un Polígono de Cobertura | `DSS_CU-056_Crear-un-Poligono-de-Cobertura.png` | `DSD_CU-056_definirZonaDeCobertura.png` |
| CU-057 | Consultar los Polígonos de Cobertura | `DSS_CU-057_Consultar-los-Poligonos-de-Cobertura.png` | `DSD_CU-057_listarZonasDeCobertura.png` |
| CU-058 | Validar la Cobertura de una Dirección | `DSS_CU-058_Validar-la-Cobertura-de-una-Direccion.png` | `DSD_CU-058_validarCobertura.png` |
| CU-059 | Dar de Baja un Polígono de Cobertura | `DSS_CU-059_Dar-de-Baja-un-Poligono-de-Cobertura.png` | `DSD_CU-059_eliminarZonaDeCobertura.png` |
| CU-060 | Registrar una Incidencia de Entrega | `DSS_CU-060_Registrar-una-Incidencia-de-Entrega.png` | `DSD_CU-060_registrarIncidencia.png` |
| CU-061 | Consultar las Incidencias | `DSS_CU-061_Consultar-las-Incidencias.png` | `DSD_CU-061_listarIncidencias.png` |
| CU-062 | Consultar las Incidencias de un Pedido | `DSS_CU-062_Consultar-las-Incidencias-de-un-Pedido.png` | `DSD_CU-062_consultarIncidenciasDelPedido.png` |
| CU-063 | Resolver una Incidencia | `DSS_CU-063_Resolver-una-Incidencia.png` | `DSD_CU-063_resolverIncidencia.png` |
| CU-064 | Calificar un Pedido (cliente↔chofer) | `DSS_CU-064_Calificar-un-Pedido.png` | `DSD_CU-064_calificarPedido.png` |
| CU-065 | Consultar el Promedio de Calificaciones de un Usuario | `DSS_CU-065_Consultar-el-Promedio-de-Calificaciones-de-un-Usuario.png` | `DSD_CU-065_consultarResumenDeCalificaciones.png` |
| CU-066 | Consultar el Historial de Calificaciones Recibidas | `DSS_CU-066_Consultar-el-Historial-de-Calificaciones-Recibidas.png` | `DSD_CU-066_consultarHistorialDeCalificaciones.png` |
| CU-067 | Dar de Alta un Envase Físico | `DSS_CU-067_Dar-De-Alta-Un-Envase-Fisico.png` | `DSD_CU-067_darDeAltaEnvase.png` |
| CU-068 | Asignar los Envases a un Pedido | `DSS_CU-068_Asignar-los-Envases-a-un-Pedido.png` | `DSD_CU-068_asignarEnvasesAPedido.png` |
| CU-069 | Consultar el Parque de Envases | `DSS_CU-069_Consultar-El-Parque-De-Envases.png` | `DSD_CU-069_consultarEnvase.png` · `DSD_CU-069_listarEnvases.png` |
| CU-070 | Registrar un Movimiento de Envase (cambio de estado) | `DSS_CU-070_Registrar-un-Movimiento-de-Envase.png` | `DSD_CU-070_registrarMovimientoDeEnvase.png` |
| CU-071 | Consultar el Historial de Movimientos de un Envase | `DSS_CU-071_Consultar-el-Historial-de-Movimientos-de-un-Envase.png` | `DSD_CU-071_consultarHistorialDelEnvase.png` |
| CU-072 | Crear una Reserva Programada con Seña | `DSS_CU-072_Crear-una-Reserva-Programada-con-Sena.png` | `DSD_CU-072_crearReserva.png` |
| CU-073 | Consultar las Reservas y el Estado de la Seña | `DSS_CU-073_Consultar-las-Reservas-y-el-Estado-de-la-Sena.png` | `DSD_CU-073_listarReservas.png` |
| CU-074 | Confirmar la Seña Cobrada en Efectivo | `DSS_CU-074_Confirmar-la-Sena-Cobrada-en-Efectivo.png` | `DSD_CU-074_confirmarSenia.png` |
| CU-075 | Activar las Reservas Vencidas Automáticamente | `DSS_CU-075_Activar-las-Reservas-Vencidas-Automaticamente.png` | `DSD_CU-075_activarReservasDelDia.png` |
| CU-076 | Expirar las Reservas sin Seña Pagada | `DSS_CU-076_Expirar-las-Reservas-sin-Sena-Pagada.png` | `DSD_CU-076_expirarReservasSinSenia.png` |
| CU-077 | Expirar los Pedidos de MercadoPago sin Pagar | `DSS_CU-077_Expirar-los-Pedidos-de-MercadoPago-sin-Pagar.png` | `DSD_CU-077_expirarPedidosSinPagar.png` |
| CU-078 | Consultar el Código de Entrega (QR del chofer) | `DSS_CU-078_Consultar-El-Codigo-De-Entrega.png` | `DSD_CU-078_obtenerCodigoDeEntrega.png` |
| CU-079 | Confirmar una Entrega Escaneando el QR (cliente) | `DSS_CU-079_Confirmar-una-Entrega-Escaneando-el-QR.png` | `DSD_CU-079_confirmarEntregaConCodigo.png` |
| CU-080 | Consultar el Pool de Pedidos Disponibles | `DSS_CU-080_Consultar-El-Pool-De-Pedidos-Disponibles.png` | `DSD_CU-080_consultarPedidosDisponibles.png` |
| CU-081 | Consultar los Pedidos Asignados al Chofer | `DSS_CU-081_Consultar-Los-Pedidos-Asignados-Al-Chofer.png` | `DSD_CU-081_consultarPedidosAsignados.png` |
| CU-082 | Crear un Usuario Base | `DSS_CU-082_Crear-un-Usuario-Base.png` | `DSD_CU-082_crearUsuarioBase.png` |
| CU-083 | Consultar los Usuarios | `DSS_CU-083_Consultar-los-Usuarios.png` | `DSD_CU-083_listarUsuarios.png` |
| CU-085 | Dar de Baja un Usuario | `DSS_CU-085_Dar-de-Baja-un-Usuario.png` | `DSD_CU-085_eliminarUsuario.png` |
| CU-086 | Registrar un Administrador | `DSS_CU-086_Registrar-un-Administrador.png` | `DSD_CU-086_registrarAdministrador.png` |
| CU-087 | Crear el Primer Administrador General | `DSS_CU-087_Crear-el-Primer-Administrador-General.png` | `DSD_CU-087_crearPrimerSuperAdministrador.png` |
| CU-088 | Consultar los Administradores | `DSS_CU-088_Consultar-los-Administradores.png` | `DSD_CU-088_buscarAdministrador.png` · `DSD_CU-088_listarAdministradores.png` |
| CU-089 | Consultar los Roles | `DSS_CU-089_Consultar-los-Roles.png` | `DSD_CU-089_listarRoles.png` |
| CU-092 | Consultar el Listado de Clientes | `DSS_CU-092_Consultar-el-Listado-de-Clientes.png` | `DSD_CU-092_listarClientes.png` |
| CU-094 | Modificar la Ubicación del Cliente | `DSS_CU-094_Modificar-la-Ubicacion-del-Cliente.png` | `DSD_CU-094_actualizarUbicacionDelCliente.png` |
| CU-095 | Dar de Baja un Cliente | `DSS_CU-095_Dar-de-Baja-un-Cliente.png` | `DSD_CU-095_eliminarCliente.png` |
| CU-096 | Modificar el Perfil del Chofer | `DSS_CU-096_Modificar-el-Perfil-del-Chofer.png` | `DSD_CU-096_actualizarPerfilDelChofer.png` |
| CU-097 | Dar de Baja un Chofer | `DSS_CU-097_Dar-de-Baja-un-Chofer.png` | `DSD_CU-097_eliminarChofer.png` |
| CU-100 | Enviar una Notificación de Prueba | `DSS_CU-100_Enviar-una-Notificacion-de-Prueba.png` | `DSD_CU-100_enviarNotificacionDePrueba.png` |
| CU-101 | Reenviar la Notificación de Confirmación de Pedido | `DSS_CU-101_Reenviar-la-Notificacion-de-Confirmacion-de-Pedido.png` | `DSD_CU-101_reenviarConfirmacionDePedido.png` |
| CU-102 | Probar el Servicio de Correo | `DSS_CU-102_Probar-El-Servicio-De-Correo.png` | `DSD_CU-102_probarServicioDeCorreo.png` |
| CU-104 | Verificar la Salud del Sistema (vida y disponibilidad) | `DSS_CU-104_Verificar-La-Salud-Del-Sistema.png` | `DSD_CU-104_verificarDisponibilidad.png` · `DSD_CU-104_verificarSalud.png` · `DSD_CU-104_verificarVida.png` |
| CU-105 | Planificar el Mantenimiento y las Habilitaciones de la Flota | `DSS_CU-105_Planificar-El-Mantenimiento-Y-Las-Habilitaciones-De-La-Flota.png` | `DSD_CU-105_aceptarVentanaDeMantenimiento.png` · `DSD_CU-105_confirmarVentanaDeTaller.png` · `DSD_CU-105_planificarMantenimientoDeFlota.png` |
| CU-106 | Anticipar la Recompra por Consumo Estimado | `DSS_CU-106_Anticipar-La-Recompra-Por-Consumo-Estimado.png` | `DSD_CU-106_aceptarInvitacionDeRecompra.png` · `DSD_CU-106_anticiparRecompras.png` |
| CU-107 | Agrupar Pedidos por Recorrido | `DSS_CU-107_Agrupar-Pedidos-Por-Recorrido.png` | `DSD_CU-107_aceptarRecorrido.png` · `DSD_CU-107_agruparPedidosPorRecorrido.png` |
| CU-108 | Recuperar Envases No Devueltos | `DSS_CU-108_Recuperar-Envases-No-Devueltos.png` | `DSD_CU-108_aceptarRetiroEnLaEntrega.png` · `DSD_CU-108_gestionarEnvasesNoDevueltos.png` · `DSD_CU-108_resolverCasoDeRecupero.png` |
| CU-109 | Consultar el Detalle del Chofer | `DSS_CU-109_Consultar-el-Detalle-del-Chofer.png` | `DSD_CU-109_consultarDetalleDelChofer.png` |
| CU-110 | Buscar un Chofer por Usuario | `DSS_CU-110_Buscar-un-Chofer-por-Usuario.png` | `DSD_CU-110_buscarChoferPorUsuario.png` |
| CU-111 | Modificar un Vehículo | `DSS_CU-111_Modificar-un-Vehiculo.png` | `DSD_CU-111_editarVehiculo.png` |
| CU-112 | Dar de Baja un Vehículo | `DSS_CU-112_Dar-de-Baja-un-Vehiculo.png` | `DSD_CU-112_eliminarVehiculo.png` |
| CU-113 | Consultar el Detalle del Vehículo | `DSS_CU-113_Consultar-el-Detalle-del-Vehiculo.png` | `DSD_CU-113_consultarDetalleDelVehiculo.png` |
| CU-114 | Buscar un Vehículo por Patente | `DSS_CU-114_Buscar-un-Vehiculo-por-Patente.png` | `DSD_CU-114_buscarVehiculoPorPatente.png` |
| CU-115 | Consultar los Vehículos de un Chofer | `DSS_CU-115_Consultar-los-Vehiculos-de-un-Chofer.png` | `DSD_CU-115_consultarVehiculosDelChofer.png` |
| CU-116 | Registrar una Dirección de Entrega | `DSS_CU-116_Registrar-una-Direccion-de-Entrega.png` | `DSD_CU-116_registrarDireccionDeEntrega.png` |
| CU-117 | Consultar Detalle de una Dirección de Entrega | `DSS_CU-117_Consultar-Detalle-de-una-Direccion-de-Entrega.png` | `DSD_CU-117_consultarDireccionDeEntrega.png` |
| CU-118 | Modificar una Dirección de Entrega | `DSS_CU-118_Modificar-una-Direccion-de-Entrega.png` | `DSD_CU-118_editarDireccionDeEntrega.png` |
| CU-119 | Dar de Baja una Dirección de Entrega | `DSS_CU-119_Dar-de-Baja-una-Direccion-de-Entrega.png` | `DSD_CU-119_eliminarDireccionDeEntrega.png` |
| CU-120 | Marcar una Dirección como Predeterminada | `DSS_CU-120_Marcar-una-Direccion-como-Predeterminada.png` | `DSD_CU-120_marcarDireccionPredeterminada.png` |
| CU-121 | Consultar la Dirección Predeterminada | `DSS_CU-121_Consultar-la-Direccion-Predeterminada.png` | `DSD_CU-121_consultarDireccionPredeterminada.png` |
| CU-122 | Agregar un Ítem al Carrito | `DSS_CU-122_Agregar-un-Item-al-Carrito.png` | `DSD_CU-122_agregarItemAlCarrito.png` |
| CU-123 | Modificar la Cantidad de un Ítem del Carrito | `DSS_CU-123_Modificar-la-Cantidad-de-un-Item-del-Carrito.png` | `DSD_CU-123_modificarCantidadDelItem.png` |
| CU-124 | Quitar un Ítem del Carrito | `DSS_CU-124_Quitar-un-Item-del-Carrito.png` | `DSD_CU-124_quitarItemDelCarrito.png` |
| CU-125 | Consultar el Carrito | `DSS_CU-125_Consultar-el-Carrito.png` | `DSD_CU-125_consultarCarrito.png` |
| CU-126 | Vaciar el Carrito | `DSS_CU-126_Vaciar-el-Carrito.png` | `DSD_CU-126_vaciarCarrito.png` |
| CU-127 | Cambiar la Dirección de Entrega del Pedido | `DSS_CU-127_Cambiar-la-Direccion-de-Entrega-del-Pedido.png` | `DSD_CU-127_cambiarDireccionDeEntrega.png` |
| CU-128 | Indicar Quién Recibe el Pedido | `DSS_CU-128_Indicar-Quien-Recibe-el-Pedido.png` | `DSD_CU-128_indicarQuienRecibe.png` |
| CU-129 | Consultar el Detalle del Cliente | `DSS_CU-129_Consultar-el-Detalle-del-Cliente.png` | `DSD_CU-129_consultarDetalleDelCliente.png` |
| CU-130 | Buscar un Cliente por Usuario | `DSS_CU-130_Buscar-un-Cliente-por-Usuario.png` | `DSD_CU-130_buscarClientePorUsuario.png` |
| CU-131 | Modificar los Datos del Cliente | `DSS_CU-131_Modificar-los-Datos-del-Cliente.png` | `DSD_CU-131_editarDatosDelCliente.png` |
| CU-132 | Registrar la Revisión Periódica de un Envase | `DSS_CU-132_Registrar-la-Revision-Periodica-de-un-Envase.png` | `DSD_CU-132_registrarRevisionDeEnvase.png` |
| CU-133 | Consultar la Vigencia de un Envase | `DSS_CU-133_Consultar-la-Vigencia-de-un-Envase.png` | `DSD_CU-133_consultarVigenciaDelEnvase.png` |
| CU-134 | Consultar los Envases Próximos a Vencer | `DSS_CU-134_Consultar-los-Envases-Proximos-a-Vencer.png` | `DSD_CU-134_consultarEnvasesProximosAVencer.png` |
| CU-135 | Bloquear el Despacho de un Envase Vencido | `DSS_CU-135_Bloquear-el-Despacho-de-un-Envase-Vencido.png` | `DSD_CU-135_verificarVigenciaAlAsignar.png` |
| CU-136 | Registrar el Seguro del Vehículo | `DSS_CU-136_Registrar-el-Seguro-del-Vehiculo.png` | `DSD_CU-136_registrarSeguroDelVehiculo.png` |
| CU-137 | Registrar la Verificación Técnica Vehicular | `DSS_CU-137_Registrar-la-Verificacion-Tecnica-Vehicular.png` | `DSD_CU-137_registrarVerificacionTecnica.png` |
| CU-138 | Registrar la Licencia de Conducir del Chofer | `DSS_CU-138_Registrar-la-Licencia-de-Conducir-del-Chofer.png` | `DSD_CU-138_registrarLicenciaDeConducir.png` |
| CU-139 | Consultar los Vencimientos de la Flota | `DSS_CU-139_Consultar-los-Vencimientos-de-la-Flota.png` | `DSD_CU-139_consultarVencimientosDeLaFlota.png` |
| CU-140 | Programar un Mantenimiento de Vehículo | `DSS_CU-140_Programar-un-Mantenimiento-de-Vehiculo.png` | `DSD_CU-140_programarMantenimientoDeVehiculo.png` |
| CU-141 | Registrar un Mantenimiento Realizado | `DSS_CU-141_Registrar-un-Mantenimiento-Realizado.png` | `DSD_CU-141_cerrarTareaDeFlota.png` |
| CU-142 | Avisar los Vencimientos Próximos de la Flota | `DSS_CU-142_Avisar-los-Vencimientos-Proximos-de-la-Flota.png` | `DSD_CU-142_avisarVencimientosDeLaFlota.png` |
| CU-143 | Declarar el Consumo Promedio al Registrarse | `DSS_CU-143_Declarar-el-Consumo-Promedio-al-Registrarse.png` | `DSD_CU-143_declararConsumoPromedio.png` |
| CU-144 | Modificar el Consumo Promedio Declarado | `DSS_CU-144_Modificar-el-Consumo-Promedio-Declarado.png` | `DSD_CU-144_actualizarConsumoPromedio.png` |
| CU-145 | Configurar los Días de Aviso Previo a la Recompra | `DSS_CU-145_Configurar-los-Dias-de-Aviso-Previo-a-la-Recompra.png` | `DSD_CU-145_configurarDiasDeAviso.png` |
| CU-146 | Consultar la Fecha Estimada de Recompra | `DSS_CU-146_Consultar-la-Fecha-Estimada-de-Recompra.png` | `DSD_CU-146_consultarRecomprasEstimadas.png` |
| CU-147 | Realizar una Compra Express | `DSS_CU-147_Realizar-una-Compra-Express.png` | `DSD_CU-147_realizarCompraExpress.png` |
| CU-148 | Elegir la Modalidad de Entrega del Pedido | `DSS_CU-148_Elegir-la-Modalidad-de-Entrega-del-Pedido.png` | `DSD_CU-148_consultarModalidadesDeEntrega.png` |
| CU-149 | Despachar un Pedido Express a un Chofer en Moto | `DSS_CU-149_Despachar-un-Pedido-Express-a-un-Chofer-en-Moto.png` | `DSD_CU-149_despacharPedidoExpress.png` |
| CU-150 | Programar la Vigencia de un Polígono de Cobertura | `DSS_CU-150_Programar-la-Vigencia-de-un-Poligono-de-Cobertura.png` | `DSD_CU-150_programarVigenciaDeZona.png` |
| CU-151 | Desactivar los Polígonos de Cobertura Vencidos | `DSS_CU-151_Desactivar-los-Poligonos-de-Cobertura-Vencidos.png` | `DSD_CU-151_desactivarZonasVencidas.png` |
| CU-152 | Consultar el Registro de Auditoría | `DSS_CU-152_Consultar-El-Registro-De-Auditoria.png` | `DSD_CU-152_consultarAuditoria.png` · `DSD_CU-152_consultarAuditoriaDeDatos.png` |
| CU-154 | Consultar el Listado de Franjas Horarias | `DSS_CU-154_Consultar-el-Listado-de-Franjas-Horarias.png` | `DSD_CU-154_consultarFranjasHorarias.png` |
| CU-155 | Adjuntar un Archivo a una Tarea de Flota | `DSS_CU-155_Adjuntar-un-Archivo-a-una-Tarea-de-Flota.png` | `DSD_CU-155_adjuntarArchivoALaTarea.png` |
| CU-156 | Consultar los Adjuntos de una Tarea de Flota | `DSS_CU-156_Consultar-los-Adjuntos-de-una-Tarea-de-Flota.png` | `DSD_CU-156_consultarAdjuntosDeLaTarea.png` |
| CU-157 | Descargar un Adjunto de Flota | `DSS_CU-157_Descargar-un-Adjunto-de-Flota.png` | `DSD_CU-157_descargarAdjunto.png` |
| CU-158 | Eliminar un Adjunto de Flota | `DSS_CU-158_Eliminar-un-Adjunto-de-Flota.png` | `DSD_CU-158_eliminarAdjunto.png` |
| CU-159 | Almacenar un Archivo | `DSS_CU-159_Almacenar-un-Archivo.png` | `DSD_CU-159_almacenarArchivo.png` |
| CU-160 | Recuperar un Archivo | `DSS_CU-160_Recuperar-un-Archivo.png` | `DSD_CU-160_recuperarArchivo.png` |
| CU-161 | Poner un Vehículo en Uso para un Chofer | `DSS_CU-161_Poner-un-Vehiculo-en-Uso-para-un-Chofer.png` | `DSD_CU-161_ponerVehiculoEnUso.png` |
| CU-162 | Liberar el Vehículo en Uso de un Chofer | `DSS_CU-162_Liberar-el-Vehiculo-en-Uso-de-un-Chofer.png` | `DSD_CU-162_liberarVehiculoEnUso.png` |
| CU-163 | Consultar el Vehículo en Uso de un Chofer | `DSS_CU-163_Consultar-el-Vehiculo-en-Uso-de-un-Chofer.png` | `DSD_CU-163_consultarMiVehiculoEnUso.png` · `DSD_CU-163_consultarVehiculoEnUso.png` |
| CU-164 | Consultar el Historial de Vehículos de un Chofer | `DSS_CU-164_Consultar-el-Historial-de-Vehiculos-de-un-Chofer.png` | `DSD_CU-164_consultarHistorialDeVehiculosDelChofer.png` |
| CU-165 | Consultar el Historial de Choferes de un Vehículo | `DSS_CU-165_Consultar-el-Historial-de-Choferes-de-un-Vehiculo.png` | `DSD_CU-165_consultarHistorialDeChoferesDelVehiculo.png` |
| CU-166 | Tomar un Reclamo Pendiente | `DSS_CU-166_Tomar-un-Reclamo-Pendiente.png` | `DSD_CU-166_tomarReclamo.png` |
| CU-167 | Reabrir un Reclamo | `DSS_CU-167_Reabrir-un-Reclamo.png` | `DSD_CU-167_reabrirReclamo.png` |
| CU-168 | Reintegrar el Pago de un Pedido | `DSS_CU-168_Reintegrar-el-Pago-de-un-Pedido.png` | `DSD_CU-168_reintegrarPagoDelPedido.png` |
| CU-169 | Registrar el Cambio de Estado de un Pedido | `DSS_CU-169_Registrar-el-Cambio-de-Estado-de-un-Pedido.png` | `DSD_CU-169_registrarCambioDeEstado.png` |
| CU-170 | Consultar el Historial de Estados de un Pedido | `DSS_CU-170_Consultar-el-Historial-de-Estados-de-un-Pedido.png` | `DSD_CU-170_consultarHistorialDeEstados.png` |
| CU-171 | Configurar los Parámetros de Despacho de la Distribuidora | `DSS_CU-171_Configurar-los-Parametros-de-Despacho-de-la-Distribuidora.png` | `DSD_CU-171_configurarParametrosDeDespacho.png` |
| CU-172 | Configurar los Parámetros de un Proceso Automático | `DSS_CU-172_Configurar-los-Parametros-de-un-Proceso-Automatico.png` | `DSD_CU-172_configurarParametrosDeProceso.png` |
| CU-173 | Configurar la Frecuencia de las Tareas Programadas | `DSS_CU-173_Configurar-la-Frecuencia-de-las-Tareas-Programadas.png` | `DSD_CU-173_configurarFrecuenciaDeTareas.png` |
| CU-174 | Adjuntar la Fotografía de un Reclamo | `DSS_CU-174_Adjuntar-la-Fotografia-de-un-Reclamo.png` | `DSD_CU-174_adjuntarFotoAlReclamo.png` |
| CU-175 | Consultar la Fotografía de un Reclamo | `DSS_CU-175_Consultar-la-Fotografia-de-un-Reclamo.png` | `DSD_CU-175_consultarFotoDelReclamo.png` |
| CU-176 | Consultar los Puestos de Trabajo | `DSS_CU-176_Consultar-los-Puestos-de-Trabajo.png` | `DSD_CU-176_consultarPuestosDeTrabajo.png` |
| CU-177 | Registrar el Legajo de un Empleado | `DSS_CU-177_Registrar-el-Legajo-de-un-Empleado.png` | `DSD_CU-177_registrarEmpleado.png` |
| CU-178 | Modificar el Legajo de un Empleado | `DSS_CU-178_Modificar-el-Legajo-de-un-Empleado.png` | `DSD_CU-178_modificarEmpleado.png` |
| CU-179 | Consultar el Legajo de un Empleado | `DSS_CU-179_Consultar-el-Legajo-de-un-Empleado.png` | `DSD_CU-179_consultarEmpleado.png` |
| CU-180 | Consultar el Listado de Empleados | `DSS_CU-180_Consultar-el-Listado-de-Empleados.png` | `DSD_CU-180_consultarEmpleados.png` |
| CU-181 | Registrar el Egreso de un Empleado | `DSS_CU-181_Registrar-el-Egreso-de-un-Empleado.png` | `DSD_CU-181_registrarEgresoDelEmpleado.png` |
| CU-182 | Otorgar una Cuenta de Acceso a un Empleado | `DSS_CU-182_Otorgar-una-Cuenta-de-Acceso-a-un-Empleado.png` | `DSD_CU-182_otorgarCuentaDeAcceso.png` |
| CU-183 | Registrar el Curso de Transporte de Mercancías Peligrosas del Empleado | `DSS_CU-183_Registrar-el-Curso-de-Transporte-de-Mercancias-Peligrosas-del-Empleado.png` | `DSD_CU-183_registrarCursoDeMercanciasPeligrosas.png` |
| CU-184 | Registrar el Examen Psicofísico del Empleado | `DSS_CU-184_Registrar-el-Examen-Psicofisico-del-Empleado.png` | `DSD_CU-184_registrarExamenPsicofisico.png` |
| CU-185 | Registrar el Alta en la ART del Empleado | `DSS_CU-185_Registrar-el-Alta-en-la-ART-del-Empleado.png` | `DSD_CU-185_registrarAltaEnLaART.png` |
| CU-186 | Adjuntar un Archivo al Legajo | `DSS_CU-186_Adjuntar-un-Archivo-al-Legajo.png` | `DSD_CU-186_adjuntarArchivoAlLegajo.png` |
| CU-187 | Consultar los Vencimientos del Personal | `DSS_CU-187_Consultar-los-Vencimientos-del-Personal.png` | `DSD_CU-187_consultarDocumentacionDelEmpleado.png` · `DSD_CU-187_consultarVencimientosDelPersonal.png` |
| CU-188 | Avisar los Vencimientos Próximos del Personal | `DSS_CU-188_Avisar-los-Vencimientos-Proximos-del-Personal.png` | `DSD_CU-188_avisarVencimientosDelPersonal.png` |
| CU-189 | Registrar la Asistencia de un Empleado | `DSS_CU-189_Registrar-la-Asistencia-de-un-Empleado.png` | `DSD_CU-189_registrarAsistencia.png` |
| CU-190 | Registrar el Inicio de la Jornada | `DSS_CU-190_Registrar-el-Inicio-de-la-Jornada.png` | `DSD_CU-190_registrarInicioDeJornada.png` |
| CU-191 | Registrar una Licencia o Ausencia | `DSS_CU-191_Registrar-una-Licencia-o-Ausencia.png` | `DSD_CU-191_registrarLicencia.png` |
| CU-192 | Aprobar una Solicitud de Licencia | `DSS_CU-192_Aprobar-una-Solicitud-de-Licencia.png` | `DSD_CU-192_aprobarLicencia.png` |
| CU-193 | Consultar el Saldo de Vacaciones de un Empleado | `DSS_CU-193_Consultar-el-Saldo-de-Vacaciones-de-un-Empleado.png` | `DSD_CU-193_consultarSaldoDeVacaciones.png` |
| CU-194 | Consultar el Tablero de Personal | `DSS_CU-194_Consultar-el-Tablero-de-Personal.png` | `DSD_CU-194_consultarTableroDePersonal.png` |
| CU-195 | Registrar una Carga de Combustible | `DSS_CU-195_Registrar-una-Carga-de-Combustible.png` | `DSD_CU-195_registrarCargaDeCombustible.png` |
| CU-196 | Consultar el Consumo de Combustible de un Vehículo | `DSS_CU-196_Consultar-el-Consumo-de-Combustible-de-un-Vehiculo.png` | `DSD_CU-196_consultarConsumoDeCombustible.png` |
| CU-197 | Registrar la Habilitación para Transportar Mercancías Peligrosas | `DSS_CU-197_Registrar-la-Habilitacion-para-Transportar-Mercancias-Peligrosas.png` | `DSD_CU-197_registrarHabilitacionDeMercanciasPeligrosas.png` |
| CU-198 | Registrar una Multa de Tránsito | `DSS_CU-198_Registrar-una-Multa-de-Transito.png` | `DSD_CU-198_registrarMultaDeTransito.png` |
| CU-199 | Registrar el Pago de una Multa | `DSS_CU-199_Registrar-el-Pago-de-una-Multa.png` | `DSD_CU-199_registrarPagoDeMulta.png` |
| CU-200 | Imputar una Multa al Chofer | `DSS_CU-200_Imputar-una-Multa-al-Chofer.png` | `DSD_CU-200_imputarMultaAlChofer.png` |
| CU-201 | Registrar un Siniestro | `DSS_CU-201_Registrar-un-Siniestro.png` | `DSD_CU-201_registrarSiniestro.png` |
| CU-202 | Cerrar un Siniestro | `DSS_CU-202_Cerrar-un-Siniestro.png` | `DSD_CU-202_cerrarSiniestro.png` |
| CU-203 | Consultar el Costo Total de un Vehículo | `DSS_CU-203_Consultar-el-Costo-Total-de-un-Vehiculo.png` | `DSD_CU-203_consultarCostoDeUnVehiculo.png` |
| CU-204 | Consultar el Tablero de Costos de la Flota | `DSS_CU-204_Consultar-el-Tablero-de-Costos-de-la-Flota.png` | `DSD_CU-204_consultarTableroDeCostosDeLaFlota.png` |
| CU-205 | Registrar un Neumático | `DSS_CU-205_Registrar-un-Neumatico.png` | `DSD_CU-205_registrarNeumatico.png` |
| CU-206 | Registrar un Movimiento de Neumático | `DSS_CU-206_Registrar-un-Movimiento-de-Neumatico.png` | `DSD_CU-206_registrarMovimientoDeNeumatico.png` |
| CU-207 | Consultar los Depósitos | `DSS_CU-207_Consultar-los-Depositos.png` | `DSD_CU-207_consultarDeposito.png` · `DSD_CU-207_consultarDepositos.png` |
| CU-208 | Consultar el Stock por Ubicación | `DSS_CU-208_Consultar-el-Stock-por-Ubicacion.png` | `DSD_CU-208_consultarStockPorUbicacion.png` · `DSD_CU-208_consultarUbicacionesDeStock.png` |
| CU-209 | Consultar los Movimientos de Stock | `DSS_CU-209_Consultar-los-Movimientos-de-Stock.png` | `DSD_CU-209_consultarMovimientosDeStock.png` |
| CU-210 | Configurar el Stock Mínimo | `DSS_CU-210_Configurar-el-Stock-Minimo.png` | `DSD_CU-210_configurarStockMinimo.png` |
| CU-211 | Avisar el Stock Bajo | `DSS_CU-211_Avisar-el-Stock-Bajo.png` | `DSD_CU-211_avisarStockBajo.png` |
| CU-212 | Transferir Stock entre Depósitos | `DSS_CU-212_Transferir-Stock-entre-Depositos.png` | `DSD_CU-212_transferirStock.png` |
| CU-213 | Registrar un Ajuste o una Merma de Stock | `DSS_CU-213_Registrar-un-Ajuste-o-una-Merma-de-Stock.png` | `DSD_CU-213_registrarAjusteDeStock.png` |
| CU-214 | Consultar los Proveedores | `DSS_CU-214_Consultar-los-Proveedores.png` | `DSD_CU-214_consultarProveedor.png` · `DSD_CU-214_consultarProveedores.png` |
| CU-215 | Emitir una Orden de Compra | `DSS_CU-215_Emitir-una-Orden-de-Compra.png` | `DSD_CU-215_emitirOrdenDeCompra.png` |
| CU-216 | Cancelar una Orden de Compra | `DSS_CU-216_Cancelar-una-Orden-de-Compra.png` | `DSD_CU-216_cancelarOrdenDeCompra.png` |
| CU-217 | Registrar la Recepción de una Compra | `DSS_CU-217_Registrar-la-Recepcion-de-una-Compra.png` | `DSD_CU-217_registrarRecepcionDeCompra.png` |
| CU-218 | Registrar la Carga del Camión | `DSS_CU-218_Registrar-la-Carga-del-Camion.png` | `DSD_CU-218_registrarCargaDelCamion.png` |
| CU-219 | Registrar la Salida del Camión | `DSS_CU-219_Registrar-la-Salida-del-Camion.png` | `DSD_CU-219_registrarSalidaDelCamion.png` |
| CU-220 | Descontar del Stock Físico lo Entregado | `DSS_CU-220_Descontar-del-Stock-Fisico-lo-Entregado.png` | `DSD_CU-220_descontarStockDeLaEntrega.png` |
| CU-221 | Registrar el Regreso del Camión | `DSS_CU-221_Registrar-el-Regreso-del-Camion.png` | `DSD_CU-221_registrarRegresoDelCamion.png` |
| CU-222 | Cerrar la Rendición de Stock del Camión | `DSS_CU-222_Cerrar-la-Rendicion-de-Stock-del-Camion.png` | `DSD_CU-222_cerrarRendicionDeStock.png` |
| CU-223 | Consultar la Carga Actual del Camión | `DSS_CU-223_Consultar-la-Carga-Actual-del-Camion.png` | `DSD_CU-223_consultarCargaActual.png` |
| CU-224 | Conciliar el Stock Vendible con el Físico | `DSS_CU-224_Conciliar-el-Stock-Vendible-con-el-Fisico.png` | `DSD_CU-224_conciliarStock.png` · `DSD_CU-224_consultarConciliacionDeStock.png` |
| CU-225 | Crear una Caja | `DSS_CU-225_Crear-una-Caja.png` | `DSD_CU-225_crearCaja.png` |
| CU-226 | Abrir la Caja | `DSS_CU-226_Abrir-la-Caja.png` | `DSD_CU-226_abrirCaja.png` |
| CU-227 | Cerrar la Caja con Arqueo | `DSS_CU-227_Cerrar-la-Caja-con-Arqueo.png` | `DSD_CU-227_cerrarCajaConArqueo.png` |
| CU-228 | Registrar una Entrada de Dinero en la Caja | `DSS_CU-228_Registrar-una-Entrada-de-Dinero-en-la-Caja.png` | `DSD_CU-228_registrarEntradaDeDinero.png` |
| CU-229 | Anular un Movimiento de Caja | `DSS_CU-229_Anular-un-Movimiento-de-Caja.png` | `DSD_CU-229_anularMovimientoDeCaja.png` |
| CU-230 | Crear una Categoría de Ingresos y Gastos | `DSS_CU-230_Crear-una-Categoria-de-Ingresos-y-Gastos.png` | `DSD_CU-230_crearCategoriaDeCaja.png` |
| CU-231 | Generar la Rendición Diaria del Chofer | `DSS_CU-231_Generar-la-Rendicion-Diaria-del-Chofer.png` | `DSD_CU-231_generarRendicionesDelDia.png` |
| CU-232 | Declarar el Efectivo Rendido | `DSS_CU-232_Declarar-el-Efectivo-Rendido.png` | `DSD_CU-232_declararEfectivoRendido.png` |
| CU-233 | Aprobar la Rendición del Chofer | `DSS_CU-233_Aprobar-la-Rendicion-del-Chofer.png` | `DSD_CU-233_aprobarRendicion.png` |
| CU-234 | Avisar las Rendiciones sin Cerrar | `DSS_CU-234_Avisar-las-Rendiciones-sin-Cerrar.png` | `DSD_CU-234_avisarRendicionesSinCerrar.png` |
| CU-235 | Habilitar la Cuenta Corriente de un Cliente | `DSS_CU-235_Habilitar-la-Cuenta-Corriente-de-un-Cliente.png` | `DSD_CU-235_habilitarCuentaCorriente.png` |
| CU-236 | Vender a Cuenta Corriente | `DSS_CU-236_Vender-a-Cuenta-Corriente.png` | `DSD_CU-236_venderACuentaCorriente.png` |
| CU-237 | Registrar un Pago de Cuenta Corriente | `DSS_CU-237_Registrar-un-Pago-de-Cuenta-Corriente.png` | `DSD_CU-237_registrarPagoDeCuentaCorriente.png` |
| CU-238 | Consultar el Estado de Cuenta de un Cliente | `DSS_CU-238_Consultar-el-Estado-de-Cuenta-de-un-Cliente.png` | `DSD_CU-238_consultarEstadoDeCuenta.png` |
| CU-239 | Consultar la Antigüedad de la Deuda | `DSS_CU-239_Consultar-la-Antiguedad-de-la-Deuda.png` | `DSD_CU-239_consultarAntiguedadDeDeuda.png` |
| CU-240 | Crear una Regla de Comisión por Entrega | `DSS_CU-240_Crear-una-Regla-de-Comision-por-Entrega.png` | `DSD_CU-240_crearReglaDeComision.png` |
| CU-241 | Registrar la Comisión de una Entrega | `DSS_CU-241_Registrar-la-Comision-de-una-Entrega.png` | `DSD_CU-241_registrarComisionDeEntrega.png` |
| CU-242 | Liquidar las Comisiones de un Chofer | `DSS_CU-242_Liquidar-las-Comisiones-de-un-Chofer.png` | `DSD_CU-242_liquidarComisionesDelChofer.png` |
| CU-243 | Registrar el Pago de una Liquidación | `DSS_CU-243_Registrar-el-Pago-de-una-Liquidacion.png` | `DSD_CU-243_pagarLiquidacion.png` |
| CU-244 | Consultar Mis Comisiones | `DSS_CU-244_Consultar-Mis-Comisiones.png` | `DSD_CU-244_consultarMisComisiones.png` |
| CU-245 | Consultar el Tablero Financiero | `DSS_CU-245_Consultar-el-Tablero-Financiero.png` | `DSD_CU-245_consultarTableroFinanciero.png` |
| CU-246 | Verificar la Habilitación Laboral del Chofer | `DSS_CU-246_Verificar-la-Habilitacion-Laboral-del-Chofer.png` | `DSD_CU-246_verificarHabilitacionLaboral.png` |
| CU-247 | Reactivar un Vehículo | `DSS_CU-247_Reactivar-un-Vehiculo.png` | `DSD_CU-247_reactivarVehiculo.png` |
| CU-248 | Verificar la Carga de Camión Abierta del Chofer | `DSS_CU-248_Verificar-la-Carga-de-Camion-Abierta-del-Chofer.png` | `DSD_CU-248_verificarCargaDeCamionAbierta.png` |
| CU-249 | Configurar el Control de Carga de Camión Abierta | `DSS_CU-249_Configurar-el-Control-de-Carga-de-Camion-Abierta.png` | `DSD_CU-249_configurarControlDeCargaAbierta.png` |
| CU-250 | Aplicar un Movimiento de Stock | `DSS_CU-250_Aplicar-un-Movimiento-de-Stock.png` | `DSD_CU-250_aplicarMovimientoDeStock.png` |
| CU-251 | Modificar el Perfil de Usuario | `DSS_CU-251_Modificar-el-Perfil-de-Usuario.png` | `DSD_CU-251_actualizarPerfil.png` |
| CU-252 | Crear un Rol | `DSS_CU-252_Crear-un-Rol.png` | `DSD_CU-252_crearRol.png` |
| CU-253 | Modificar un Rol | `DSS_CU-253_Modificar-un-Rol.png` | `DSD_CU-253_actualizarRol.png` |
| CU-254 | Dar de Baja un Rol | `DSS_CU-254_Dar-de-Baja-un-Rol.png` | `DSD_CU-254_eliminarRol.png` |
| CU-255 | Crear un Puesto de Trabajo | `DSS_CU-255_Crear-un-Puesto-de-Trabajo.png` | `DSD_CU-255_crearPuestoDeTrabajo.png` |
| CU-256 | Modificar un Puesto de Trabajo | `DSS_CU-256_Modificar-un-Puesto-de-Trabajo.png` | `DSD_CU-256_modificarPuestoDeTrabajo.png` |
| CU-257 | Dar de Baja un Puesto de Trabajo | `DSS_CU-257_Dar-de-Baja-un-Puesto-de-Trabajo.png` | `DSD_CU-257_eliminarPuestoDeTrabajo.png` |
| CU-258 | Registrar un Depósito | `DSS_CU-258_Registrar-un-Deposito.png` | `DSD_CU-258_registrarDeposito.png` |
| CU-259 | Modificar un Depósito | `DSS_CU-259_Modificar-un-Deposito.png` | `DSD_CU-259_actualizarDeposito.png` |
| CU-260 | Dar de Baja un Depósito | `DSS_CU-260_Dar-de-Baja-un-Deposito.png` | `DSD_CU-260_darDeBajaDeposito.png` |
| CU-261 | Registrar un Proveedor | `DSS_CU-261_Registrar-un-Proveedor.png` | `DSD_CU-261_registrarProveedor.png` |
| CU-262 | Modificar un Proveedor | `DSS_CU-262_Modificar-un-Proveedor.png` | `DSD_CU-262_actualizarProveedor.png` |
| CU-263 | Dar de Baja un Proveedor | `DSS_CU-263_Dar-de-Baja-un-Proveedor.png` | `DSD_CU-263_darDeBajaProveedor.png` |
| CU-264 | Modificar una Caja | `DSS_CU-264_Modificar-una-Caja.png` | `DSD_CU-264_modificarCaja.png` |
| CU-265 | Modificar una Categoría de Ingresos y Gastos | `DSS_CU-265_Modificar-una-Categoria-de-Ingresos-y-Gastos.png` | `DSD_CU-265_modificarCategoriaDeCaja.png` |
| CU-266 | Desactivar la Disponibilidad | `DSS_CU-266_Desactivar-la-Disponibilidad.png` | `DSD_CU-266_desactivarDisponibilidad.png` |
| CU-267 | Desactivar un Chofer | `DSS_CU-267_Desactivar-un-Chofer.png` | `DSD_CU-267_desactivarChofer.png` |
| CU-268 | Reactivar un Producto | `DSS_CU-268_Reactivar-un-Producto.png` | `DSD_CU-268_reactivarProducto.png` |
| CU-269 | Consultar los Productos Inactivos | `DSS_CU-269_Consultar-los-Productos-Inactivos.png` | `DSD_CU-269_consultarProductosInactivos.png` |
| CU-270 | Desbloquear un Usuario | `DSS_CU-270_Desbloquear-un-Usuario.png` | `DSD_CU-270_desbloquearUsuario.png` |
| CU-271 | Invalidar un Chofer | `DSS_CU-271_Invalidar-un-Chofer.png` | `DSD_CU-271_invalidarChofer.png` |
| CU-272 | Buscar un Usuario | `DSS_CU-272_Buscar-un-Usuario.png` | `DSD_CU-272_buscarUsuarioPorCorreo.png` · `DSD_CU-272_buscarUsuarioPorTelefono.png` |
| CU-273 | Marcar el Depósito Predeterminado | `DSS_CU-273_Marcar-el-Deposito-Predeterminado.png` | `DSD_CU-273_marcarDepositoPredeterminado.png` |
| CU-274 | Registrar el Conteo Inicial de un Depósito | `DSS_CU-274_Registrar-el-Conteo-Inicial-de-un-Deposito.png` | `DSD_CU-274_registrarConteoInicial.png` |
| CU-275 | Consultar los Ajustes de Stock | `DSS_CU-275_Consultar-los-Ajustes-de-Stock.png` | `DSD_CU-275_consultarAjusteDeStock.png` · `DSD_CU-275_consultarAjustesDeStock.png` |
| CU-276 | Anular una Transferencia de Stock | `DSS_CU-276_Anular-una-Transferencia-de-Stock.png` | `DSD_CU-276_anularTransferenciaDeStock.png` |
| CU-277 | Registrar un Ajuste de Conciliación del Vendible | `DSS_CU-277_Registrar-un-Ajuste-de-Conciliacion-del-Vendible.png` | `DSD_CU-277_registrarAjusteDeConciliacion.png` |
| CU-278 | Reaplicar las Entregas sin Movimiento de Stock | `DSS_CU-278_Reaplicar-las-Entregas-sin-Movimiento-de-Stock.png` | `DSD_CU-278_reaplicarEntregasDeStock.png` |
| CU-279 | Consultar el Resumen de Stock | `DSS_CU-279_Consultar-el-Resumen-de-Stock.png` | `DSD_CU-279_consultarResumenDeStock.png` |
| CU-280 | Anular una Recepción de Compra | `DSS_CU-280_Anular-una-Recepcion-de-Compra.png` | `DSD_CU-280_anularRecepcionDeCompra.png` |
| CU-281 | Marcar el Pago de una Recepción | `DSS_CU-281_Marcar-el-Pago-de-una-Recepcion.png` | `DSD_CU-281_marcarPagoDeRecepcion.png` |
| CU-282 | Cerrar una Orden de Compra con Faltante | `DSS_CU-282_Cerrar-una-Orden-de-Compra-con-Faltante.png` | `DSD_CU-282_cerrarOrdenDeCompraConFaltante.png` |
| CU-283 | Consultar las Órdenes de Compra | `DSS_CU-283_Consultar-las-Ordenes-de-Compra.png` | `DSD_CU-283_consultarOrdenDeCompra.png` · `DSD_CU-283_consultarOrdenesDeCompra.png` · `DSD_CU-283_consultarPendienteDeRecibir.png` |
| CU-284 | Consultar las Recepciones de Compra | `DSS_CU-284_Consultar-las-Recepciones-de-Compra.png` | `DSD_CU-284_consultarRecepcionDeCompra.png` · `DSD_CU-284_consultarRecepcionesDeCompra.png` |
| CU-285 | Consultar el Costo Promedio de las Garrafas | `DSS_CU-285_Consultar-el-Costo-Promedio-de-las-Garrafas.png` | `DSD_CU-285_consultarCostoPromedio.png` |
| CU-286 | Consultar el Historial de Compras de un Proveedor | `DSS_CU-286_Consultar-el-Historial-de-Compras-de-un-Proveedor.png` | `DSD_CU-286_consultarHistorialDeCompras.png` |
| CU-287 | Modificar una Orden de Compra | `DSS_CU-287_Modificar-una-Orden-de-Compra.png` | `DSD_CU-287_modificarOrdenDeCompra.png` |
| CU-288 | Enviar una Orden de Compra | `DSS_CU-288_Enviar-una-Orden-de-Compra.png` | `DSD_CU-288_enviarOrdenDeCompra.png` |
| CU-289 | Cancelar una Carga del Camión | `DSS_CU-289_Cancelar-una-Carga-del-Camion.png` | `DSD_CU-289_cancelarCargaDelCamion.png` |
| CU-290 | Consultar las Cargas del Camión | `DSS_CU-290_Consultar-las-Cargas-del-Camion.png` | `DSD_CU-290_consultarCargasDelCamion.png` |
| CU-291 | Consultar una Carga del Camión | `DSS_CU-291_Consultar-una-Carga-del-Camion.png` | `DSD_CU-291_consultarCargaDelCamion.png` |
| CU-292 | Confirmar el Cobro en Efectivo | `DSS_CU-292_Confirmar-el-Cobro-en-Efectivo.png` | `DSD_CU-292_confirmarCobroEnEfectivo.png` |
| CU-293 | Informar el Cobro Impago | `DSS_CU-293_Informar-el-Cobro-Impago.png` | `DSD_CU-293_informarCobroImpago.png` |
| CU-294 | Resolver un Cobro Impago | `DSS_CU-294_Resolver-un-Cobro-Impago.png` | `DSD_CU-294_resolverCobroImpago.png` |
| CU-295 | Corregir los Renglones de una Carga del Camión | `DSS_CU-295_Corregir-los-Renglones-de-una-Carga-del-Camion.png` | `DSD_CU-295_corregirRenglonesDeLaCarga.png` |
| CU-296 | Reponer una Carga del Camión | `DSS_CU-296_Reponer-una-Carga-del-Camion.png` | `DSD_CU-296_reponerCargaDelCamion.png` |
| CU-297 | Consultar el Stock Mínimo | `DSS_CU-297_Consultar-el-Stock-Minimo.png` | `DSD_CU-297_consultarStockMinimo.png` |
| CU-298 | Consultar el Control de Carga de Camión Abierta | `DSS_CU-298_Consultar-el-Control-de-Carga-de-Camion-Abierta.png` | `DSD_CU-298_consultarControlDeCargaAbierta.png` |
| CU-299 | Registrar el Cobro en Efectivo como Administrador | `DSS_CU-299_Registrar-el-Cobro-en-Efectivo-como-Administrador.png` | `DSD_CU-299_registrarCobroEnEfectivoPorAdmin.png` |
| CU-300 | Registrar el Cobro Impago como Administrador | `DSS_CU-300_Registrar-el-Cobro-Impago-como-Administrador.png` | `DSD_CU-300_registrarCobroImpagoPorAdmin.png` |
| CU-301 | Confirmar una Transferencia | `DSS_CU-301_Confirmar-una-Transferencia.png` | `DSD_CU-301_confirmarTransferencia.png` |
| CU-302 | Cotizar un Pedido | `DSS_CU-302_Cotizar-un-Pedido.png` | `DSD_CU-302_cotizarPedido.png` |
| CU-303 | Consultar la Ruta de un Pedido | `DSS_CU-303_Consultar-la-Ruta-de-un-Pedido.png` | `DSD_CU-303_consultarRutaDelPedido.png` |
| CU-304 | Consultar los Cobros Pendientes | `DSS_CU-304_Consultar-los-Cobros-Pendientes.png` | `DSD_CU-304_consultarCobrosPendientes.png` |
| CU-305 | Modificar un Polígono de Cobertura | `DSS_CU-305_Modificar-un-Poligono-de-Cobertura.png` | `DSD_CU-305_modificarZonaDeCobertura.png` |
| CU-306 | Consultar un Polígono de Cobertura | `DSS_CU-306_Consultar-un-Poligono-de-Cobertura.png` | `DSD_CU-306_consultarZonaDeCobertura.png` |
| CU-307 | Activar un Polígono de Cobertura | `DSS_CU-307_Activar-un-Poligono-de-Cobertura.png` | `DSD_CU-307_activarZonaDeCobertura.png` |
| CU-308 | Desactivar un Polígono de Cobertura | `DSS_CU-308_Desactivar-un-Poligono-de-Cobertura.png` | `DSD_CU-308_desactivarZonaDeCobertura.png` |
| CU-309 | Registrar una Salida de Dinero de la Caja | `DSS_CU-309_Registrar-una-Salida-de-Dinero-de-la-Caja.png` | `DSD_CU-309_registrarSalidaDeDinero.png` |
| CU-310 | Transferir Fondos entre Cajas | `DSS_CU-310_Transferir-Fondos-entre-Cajas.png` | `DSD_CU-310_transferirEntreCajas.png` |
| CU-311 | Dar de Baja el Legajo de un Empleado | `DSS_CU-311_Dar-de-Baja-el-Legajo-de-un-Empleado.png` | `DSD_CU-311_eliminarEmpleado.png` |
| CU-312 | Reingresar a un Empleado | `DSS_CU-312_Reingresar-a-un-Empleado.png` | `DSD_CU-312_reingresarEmpleado.png` |
| CU-313 | Corregir la Asistencia de un Empleado | `DSS_CU-313_Corregir-la-Asistencia-de-un-Empleado.png` | `DSD_CU-313_corregirAsistencia.png` |
| CU-314 | Consultar la Asistencia de los Empleados | `DSS_CU-314_Consultar-la-Asistencia-de-los-Empleados.png` | `DSD_CU-314_consultarAsistencias.png` |
| CU-315 | Registrar el Fin de la Jornada | `DSS_CU-315_Registrar-el-Fin-de-la-Jornada.png` | `DSD_CU-315_registrarFinDeJornada.png` |
| CU-316 | Modificar una Licencia o Ausencia | `DSS_CU-316_Modificar-una-Licencia-o-Ausencia.png` | `DSD_CU-316_modificarLicencia.png` |
| CU-317 | Cancelar una Licencia o Ausencia | `DSS_CU-317_Cancelar-una-Licencia-o-Ausencia.png` | `DSD_CU-317_cancelarLicencia.png` |
| CU-318 | Rechazar una Solicitud de Licencia | `DSS_CU-318_Rechazar-una-Solicitud-de-Licencia.png` | `DSD_CU-318_rechazarLicencia.png` |
| CU-319 | Consultar las Licencias | `DSS_CU-319_Consultar-las-Licencias.png` | `DSD_CU-319_consultarLicencias.png` |
| CU-320 | Modificar una Carga de Combustible | `DSS_CU-320_Modificar-una-Carga-de-Combustible.png` | `DSD_CU-320_modificarCargaDeCombustible.png` |
| CU-321 | Anular una Carga de Combustible | `DSS_CU-321_Anular-una-Carga-de-Combustible.png` | `DSD_CU-321_anularCargaDeCombustible.png` |
| CU-322 | Consultar las Cargas de Combustible | `DSS_CU-322_Consultar-las-Cargas-de-Combustible.png` | `DSD_CU-322_consultarCargasDeCombustible.png` |
| CU-323 | Modificar una Multa de Tránsito | `DSS_CU-323_Modificar-una-Multa-de-Transito.png` | `DSD_CU-323_modificarMultaDeTransito.png` |
| CU-324 | Anular una Multa de Tránsito | `DSS_CU-324_Anular-una-Multa-de-Transito.png` | `DSD_CU-324_anularMultaDeTransito.png` |
| CU-325 | Consultar las Multas de Tránsito | `DSS_CU-325_Consultar-las-Multas-de-Transito.png` | `DSD_CU-325_consultarMultasDeTransito.png` |
| CU-326 | Avisar las Multas por Vencer | `DSS_CU-326_Avisar-las-Multas-por-Vencer.png` | `DSD_CU-326_avisarMultasPorVencer.png` |
| CU-327 | Modificar un Siniestro | `DSS_CU-327_Modificar-un-Siniestro.png` | `DSD_CU-327_modificarSiniestro.png` |
| CU-328 | Consultar los Siniestros | `DSS_CU-328_Consultar-los-Siniestros.png` | `DSD_CU-328_consultarSiniestros.png` |
| CU-329 | Registrar un Ajuste de Cuenta Corriente | `DSS_CU-329_Registrar-un-Ajuste-de-Cuenta-Corriente.png` | `DSD_CU-329_registrarAjusteDeCuentaCorriente.png` |
| CU-330 | Reabrir la Rendición del Chofer | `DSS_CU-330_Reabrir-la-Rendicion-del-Chofer.png` | `DSD_CU-330_reabrirRendicion.png` |
| CU-331 | Modificar la Cuenta Corriente de un Cliente | `DSS_CU-331_Modificar-la-Cuenta-Corriente-de-un-Cliente.png` | `DSD_CU-331_modificarCuentaCorriente.png` |
| CU-332 | Asentar el Cargo de una Venta a Cuenta Corriente | `DSS_CU-332_Asentar-el-Cargo-de-una-Venta-a-Cuenta-Corriente.png` | `DSD_CU-332_registrarCargoDeCuentaCorriente.png` |
| CU-333 | Modificar una Regla de Comisión por Entrega | `DSS_CU-333_Modificar-una-Regla-de-Comision-por-Entrega.png` | `DSD_CU-333_modificarReglaDeComision.png` |
| CU-334 | Aprobar una Liquidación de Comisiones | `DSS_CU-334_Aprobar-una-Liquidacion-de-Comisiones.png` | `DSD_CU-334_aprobarLiquidacion.png` |
| CU-335 | Anular una Liquidación de Comisiones | `DSS_CU-335_Anular-una-Liquidacion-de-Comisiones.png` | `DSD_CU-335_anularLiquidacion.png` |
| CU-336 | Cambiar el Correo del Usuario | `DSS_CU-336_Cambiar-el-Correo-del-Usuario.png` | `DSD_CU-336_cambiarCorreo.png` |
| CU-337 | Ajustar el Saldo del Chofer | `DSS_CU-337_Ajustar-el-Saldo-del-Chofer.png` | `DSD_CU-337_ajustarSaldoDelChofer.png` |
| CU-338 | Retomar el Pedido en Curso | `DSS_CU-338_Retomar-el-Pedido-en-Curso.png` | `DSD_CU-338_consultarPedidoEnCurso.png` |
| CU-339 | Modificar un Pedido Pendiente (Administrador) | `DSS_CU-339_Modificar-un-Pedido-Pendiente.png` | `DSD_CU-339_modificarPedido.png` |
| CU-340 | Consultar los Movimientos de Caja | `DSS_CU-340_Consultar-los-Movimientos-de-Caja.png` | `DSD_CU-340_consultarMovimientosDeCaja.png` |
| CU-341 | Modificar un Pedido Pendiente (Cliente) | `DSS_CU-341_Modificar-un-Pedido-Pendiente.png` | `DSD_CU-341_modificarMiPedido.png` |
| CU-342 | Activar una Franja Horaria | `DSS_CU-342_Activar-una-Franja-Horaria.png` | `DSD_CU-342_activarFranjaHoraria.png` |
| CU-343 | Desactivar una Franja Horaria | `DSS_CU-343_Desactivar-una-Franja-Horaria.png` | `DSD_CU-343_desactivarFranjaHoraria.png` |
| CU-344 | Consultar el Catálogo de Productos (Administrador) | `DSS_CU-344_Consultar-el-Catalogo-de-Productos-Administrador.png` | `DSD_CU-344_consultarCatalogo.png` · `DSD_CU-344_consultarDetalleDelProducto.png` |
| CU-345 | Modificar un Administrador | `DSS_CU-345_Modificar-un-Administrador.png` | `DSD_CU-345_modificarAdministrador.png` |
| CU-346 | Dar de Baja un Administrador | `DSS_CU-346_Dar-de-Baja-un-Administrador.png` | `DSD_CU-346_darDeBajaAdministrador.png` |
| CU-347 | Anular el Pago de una Liquidación | `DSS_CU-347_Anular-el-Pago-de-una-Liquidación.png` | `DSD_CU-347_anularPagoDeLiquidacion.png` |
| CU-348 | Consultar el Reintegro de un Pedido | `DSS_CU-348_Consultar-el-Reintegro-de-un-Pedido.png` | `DSD_CU-348_consultarReintegroDelPedido.png` |

## Módulos de gestión planificados: modelos y estados

Las imágenes de los cuatro módulos (personal, flota ampliada, stock y compras, caja y rendición): modelo conceptual, modelo físico, entidad-relación conceptual, clases de dominio y de diseño, y diagramas de estados. Las tablas planificadas se dibujan con el estereotipo «propuesto».

### Personal y legajos (iteración C-08)

| Imagen | Qué es |
|---|---|
| `diagramas/modelo-conceptual/MC_Personal.png` | Modelo conceptual: personal |
| `modelos/base-de-datos/fisico/SPLG-fisico-09-personal.png` | Modelo físico — Personal |
| `modelos/base-de-datos/conceptual/SPLG-der-06-personal.png` | Modelo entidad-relación conceptual — Personal |
| `diagramas/uml/UML_Estados_Empleado.png` | Diagrama de estados — Empleado (egreso y reingreso construidos; «de licencia» planificado, C-08) |
| `diagramas/uml/UML_Estados_Licencia.png` | Diagrama de estados — Licencia laboral (planificado, C-08) |
| `diagramas/uml/UML_Estados_Jornada.png` | Diagrama de estados — Jornada de trabajo (planificado, C-08) |

### Flota ampliada (iteración C-18)

| Imagen | Qué es |
|---|---|
| `diagramas/modelo-conceptual/MC_Gastos-de-flota.png` | Modelo conceptual: gastos de flota |
| `modelos/base-de-datos/fisico/SPLG-fisico-10-gastos-de-la-flota.png` | Modelo físico — Gastos de la flota |
| `modelos/base-de-datos/conceptual/SPLG-der-08-gastos-de-la-flota.png` | Modelo entidad-relación conceptual — Gastos de la flota |
| `diagramas/uml/UML_Estados_CargaCombustible.png` | Diagrama de estados — Carga de combustible (planificado, C-18) |
| `diagramas/uml/UML_Estados_MultaTransito.png` | Diagrama de estados — Multa de tránsito (planificado, C-18) |
| `diagramas/uml/UML_Estados_Siniestro.png` | Diagrama de estados — Siniestro (planificado, C-18) |
| `diagramas/uml/UML_Estados_Neumatico.png` | Diagrama de estados — Neumático (planificado, C-18, opcional) |
| `diagramas/uml/UML_Estados_PolizaDelVehiculo.png` | Diagrama de estados — Vigencia de la póliza y de la habilitación (planificado, C-18) |

### Stock y compras (iteración C-09)

| Imagen | Qué es |
|---|---|
| `diagramas/modelo-conceptual/MC_Stock.png` | Modelo conceptual: stock |
| `diagramas/modelo-conceptual/MC_Carga-del-camion.png` | Modelo conceptual: carga del camión |
| `diagramas/modelo-conceptual/MC_Compras.png` | Modelo conceptual: compras |
| `modelos/base-de-datos/fisico/SPLG-fisico-11-stock-fisico-y-carga-del-camion.png` | Modelo físico — Stock físico y carga del camión |
| `modelos/base-de-datos/fisico/SPLG-fisico-12-compras.png` | Modelo físico — Compras |
| `modelos/base-de-datos/conceptual/SPLG-der-09-stock-fisico.png` | Modelo entidad-relación conceptual — Stock físico |
| `modelos/base-de-datos/conceptual/SPLG-der-10-carga-del-camion.png` | Modelo entidad-relación conceptual — Carga del camión |
| `modelos/base-de-datos/conceptual/SPLG-der-11-compras.png` | Modelo entidad-relación conceptual — Compras |
| `diagramas/uml/UML_Estados_OrdenDeCompra.png` | Diagrama de estados — Orden de compra |
| `diagramas/uml/UML_Estados_RecepcionDeCompra.png` | Diagrama de estados — Recepción de compra |
| `diagramas/uml/UML_Estados_CargaDeCamion.png` | Diagrama de estados — Carga de camión |

### Caja y rendición (iteración C-20)

| Imagen | Qué es |
|---|---|
| `diagramas/modelo-conceptual/MC_Caja.png` | Modelo conceptual: caja |
| `diagramas/modelo-conceptual/MC_Rendiciones.png` | Modelo conceptual: rendiciones |
| `diagramas/modelo-conceptual/MC_Cuentas-corrientes.png` | Modelo conceptual: cuentas corrientes |
| `diagramas/modelo-conceptual/MC_Comisiones.png` | Modelo conceptual: comisiones |
| `modelos/base-de-datos/fisico/SPLG-fisico-14-caja-y-finanzas.png` | Modelo físico — Caja y finanzas |
| `modelos/base-de-datos/conceptual/SPLG-der-12-caja-y-movimientos.png` | Modelo entidad-relación conceptual — Caja y movimientos |
| `modelos/base-de-datos/conceptual/SPLG-der-13-rendiciones-de-choferes.png` | Modelo entidad-relación conceptual — Rendiciones de choferes |
| `modelos/base-de-datos/conceptual/SPLG-der-14-cuentas-corrientes.png` | Modelo entidad-relación conceptual — Cuentas corrientes |
| `modelos/base-de-datos/conceptual/SPLG-der-15-comisiones-y-liquidaciones.png` | Modelo entidad-relación conceptual — Comisiones y liquidaciones |
| `diagramas/uml/UML_Estados_SesionDeCaja.png` | Diagrama de estados — Sesión de caja |
| `diagramas/uml/UML_Estados_RendicionChofer.png` | Diagrama de estados — Rendición del chofer |
| `diagramas/uml/UML_Estados_LiquidacionComisiones.png` | Diagrama de estados — Liquidación de comisiones |
| `diagramas/uml/UML_Estados_CuentaCorriente.png` | Diagrama de estados — Cuenta corriente |
