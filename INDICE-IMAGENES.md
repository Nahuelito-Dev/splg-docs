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
| `CU_SS-02_Gestion-De-Pedidos.png` |
| `CU_SS-03_Despacho-Y-Asignacion.png` |
| `CU_SS-04_Seguimiento-En-Tiempo-Real.png` |
| `CU_SS-05_Reclamos.png` |
| `CU_SS-06_Reportes-Y-Dashboard.png` |
| `CU_SS-07_Gestion-De-Choferes-Y-Vehiculos.png` |
| `CU_SS-08_Gestion-De-Productos.png` |
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
| `CU_Sistema_Actores.png` |
| `CU_Sistema_Diagrama-Completo.png` |
| `CU_Sistema_Diagrama-De-Contexto.png` |
| `CU_Sistema_Mapa.png` |
| `CU_Sistema_Subsistemas.png` |

## Por caso de uso

| CU | Caso de uso | DSS | DSD |
|---|---|---|---|
| CU-001 | Iniciar Sesión | `DSS_CU-001_Iniciar-Sesion.png` | `DSD_CU-001_Iniciar-Sesion.png` |
| CU-002 | Registrarse como Cliente | `DSS_CU-002_Registrarse-Como-Cliente.png` | `DSD_CU-002_Registrarse-Como-Cliente.png` |
| CU-003 | Registrar Chofer | `DSS_CU-003_Registrar-Chofer.png` | `DSD_CU-003_Registrar-Chofer.png` |
| CU-004 | Gestionar Perfil de Usuario | `DSS_CU-004_Gestionar-Perfil-De-Usuario.png` | `DSD_CU-004_Gestionar-Perfil-De-Usuario.png` |
| CU-005 | Crear Pedido | `DSS_CU-005_Crear-Pedido.png` | `DSD_CU-005_Crear-Pedido.png` |
| CU-006 | Consultar Detalle de Pedido | `DSS_CU-006_Consultar-Detalle-De-Pedido.png` | `DSD_CU-006_Consultar-Detalle-De-Pedido.png` |
| CU-007 | Consultar Historial de Pedidos | `DSS_CU-007_Consultar-Historial-De-Pedidos.png` | `DSD_CU-007_Consultar-Historial-De-Pedidos.png` |
| CU-008 | Cancelar Pedido (Cliente) | `DSS_CU-008_Cancelar-Pedido.png` | `DSD_CU-008_Cancelar-Pedido.png` |
| CU-009 | Cancelar Pedido (Chofer) | `DSS_CU-009_Cancelar-Pedido.png` | `DSD_CU-009_Cancelar-Pedido.png` |
| CU-010 | Cancelar Pedido (Administrador) | `DSS_CU-010_Cancelar-Pedido.png` | `DSD_CU-010_Cancelar-Pedido.png` |
| CU-011 | Listar Todos los Pedidos | `DSS_CU-011_Listar-Todos-Los-Pedidos.png` | `DSD_CU-011_Listar-Todos-Los-Pedidos.png` |
| CU-012 | Asignar Chofer Manualmente | `DSS_CU-012_Asignar-Chofer-Manualmente.png` | `DSD_CU-012_Asignar-Chofer-Manualmente.png` |
| CU-013 | Asignar Pedido Automáticamente por Proximidad | `DSS_CU-013_Asignar-Pedido-Automaticamente-Por-Proximidad.png` | `DSD_CU-013_Asignar-Pedido-Automaticamente-Por-Proximidad_Oferta-Al-Mas-Cercano.png` |
| CU-014 | Reintentar Asignación con Radio Expandido (Cron) | `DSS_CU-014_Reintentar-Asignacion-Con-Radio-Expandido.png` | `DSD_CU-014_Reintentar-Asignacion-Con-Radio-Expandido.png` |
| CU-015 | Aceptar Pedido | `DSS_CU-015_Aceptar-Pedido.png` | `DSD_CU-015_CU-016_Aceptar-Pedido.png` |
| CU-016 | Rechazar / Ignorar Pedido | `DSS_CU-016_Rechazar-Ignorar-Pedido.png` | `DSD_CU-015_CU-016_Aceptar-Pedido.png` |
| CU-017 | Actualizar Ubicación GPS del Chofer | `DSS_CU-017_Actualizar-Ubicacion-Gps-Del-Chofer.png` | `DSD_CU-017_Actualizar-Ubicacion-Gps-Del-Chofer.png` |
| CU-018 | Marcar Pedido "En Camino" | `DSS_CU-018_Marcar-Pedido-En-Camino.png` | `DSD_CU-018_Marcar-Pedido-En-Camino.png` |
| CU-019 | Avisar Llegada al Cliente | `DSS_CU-019_Avisar-Llegada-Al-Cliente.png` | `DSD_CU-019_Avisar-Llegada-Al-Cliente.png` |
| CU-020 | Confirmar Entrega | `DSS_CU-020_Confirmar-Entrega.png` | `DSD_CU-020_Confirmar-Entrega.png` |
| CU-021 | Recibir Notificaciones en Tiempo Real | `DSS_CU-021_Recibir-Notificaciones-En-Tiempo-Real.png` | `DSD_CU-021_Recibir-Notificaciones-En-Tiempo-Real.png` |
| CU-022 | Activar / Desactivar Disponibilidad (Chofer) | `DSS_CU-022_Activar-Desactivar-Disponibilidad.png` | `DSD_CU-022_Activar-Desactivar-Disponibilidad.png` |
| CU-023 | Registrar Reclamo | `DSS_CU-023_Registrar-Reclamo.png` | `DSD_CU-023_Registrar-Reclamo.png` |
| CU-024 | Listar Reclamos | `DSS_CU-024_Listar-Reclamos.png` | `DSD_CU-024_Listar-Reclamos.png` |
| CU-025 | Resolver Reclamo | `DSS_CU-025_Resolver-Reclamo.png` | `DSD_CU-025_Resolver-Reclamo.png` |
| CU-026 | Ver Dashboard General | `DSS_CU-026_Ver-Dashboard-General.png` | `DSD_CU-026_Ver-Dashboard-General.png` |
| CU-027 | Ver Reporte de Ventas por Chofer | `DSS_CU-027_Ver-Reporte-De-Ventas-Por-Chofer.png` | `DSD_CU-027_Ver-Reporte-De-Ventas-Por-Chofer.png` |
| CU-028 | Ver Reporte de Ventas por Producto | `DSS_CU-028_Ver-Reporte-De-Ventas-Por-Producto.png` | `DSD_CU-028_Ver-Reporte-De-Ventas-Por-Producto.png` |
| CU-029 | Ver Reporte por Método de Pago | `DSS_CU-029_Ver-Reporte-Por-Metodo-De-Pago.png` | `DSD_CU-029_Ver-Reporte-Por-Metodo-De-Pago.png` |
| CU-030 | Ver Gráfico de Ventas (últimos 7 días) | `DSS_CU-030_Ver-Grafico-De-Ventas.png` | `DSD_CU-030_Ver-Grafico-De-Ventas.png` |
| CU-031 | Registrar Chofer | `DSS_CU-031_Registrar-Chofer.png` | `DSD_CU-031_Registrar-Chofer.png` |
| CU-032 | Validar / Invalidar Chofer | `DSS_CU-032_Validar-Invalidar-Chofer.png` | `DSD_CU-032_Validar-Invalidar-Chofer.png` |
| CU-033 | Activar / Desactivar Chofer (Admin) | `DSS_CU-033_Activar-Desactivar-Chofer.png` | `DSD_CU-033_Activar-Desactivar-Chofer.png` |
| CU-034 | Registrar Vehículo del Chofer | `DSS_CU-034_Registrar-Vehiculo-Del-Chofer.png` | `DSD_CU-034_Registrar-Vehiculo-Del-Chofer.png` |
| CU-035 | Consultar Listado de Choferes | `DSS_CU-035_Consultar-Listado-De-Choferes.png` | `DSD_CU-035_Consultar-Listado-De-Choferes.png` |
| CU-036 | Crear Producto (Garrafa) | `DSS_CU-036_Crear-Producto.png` | `DSD_CU-036_Crear-Producto.png` |
| CU-037 | Actualizar Precio de Producto | `DSS_CU-037_Actualizar-Precio-De-Producto.png` | `DSD_CU-037_Actualizar-Precio-De-Producto.png` |
| CU-038 | Actualizar Stock de Producto | `DSS_CU-038_Actualizar-Stock-De-Producto.png` | `DSD_CU-038_Actualizar-Stock-De-Producto.png` |
| CU-039 | Configurar Promociones por Cantidad | `DSS_CU-039_Configurar-Promociones-Por-Cantidad.png` | `DSD_CU-039_Configurar-Promociones-Por-Cantidad.png` |
| CU-040 | Activar / Desactivar Producto | `DSS_CU-040_Activar-Desactivar-Producto.png` | `DSD_CU-040_Activar-Desactivar-Producto.png` |
| CU-041 | Consultar Catálogo de Productos | `DSS_CU-041_Consultar-Catalogo-De-Productos.png` | `DSD_CU-041_Consultar-Catalogo-De-Productos.png` |
| CU-042 | Crear Franja Horaria | `DSS_CU-042_Crear-Franja-Horaria.png` | `DSD_CU-042_Crear-Franja-Horaria.png` |
| CU-043 | Modificar Capacidad de Franja Horaria | `DSS_CU-043_Modificar-Capacidad-De-Franja-Horaria.png` | `DSD_CU-043_Modificar-Capacidad-De-Franja-Horaria.png` |
| CU-044 | Seleccionar Franja Horaria al Crear Pedido | `DSS_CU-044_Seleccionar-Franja-Horaria-Al-Crear-Pedido.png` | `DSD_CU-044_Seleccionar-Franja-Horaria-Al-Crear-Pedido.png` |
| CU-045 | Consultar Franjas Horarias Disponibles | `DSS_CU-045_Consultar-Franjas-Horarias-Disponibles.png` | `DSD_CU-045_Consultar-Franjas-Horarias-Disponibles.png` |
| CU-046 | Consultar Direcciones de Entrega del Cliente | `DSS_CU-046_Consultar-Direcciones-De-Entrega-Del-Cliente.png` | `DSD_CU-046_Consultar-Direcciones-De-Entrega-Del-Cliente.png` |
| CU-047 | Recuperar Contraseña | `DSS_CU-047_Recuperar-Contrasena.png` | `DSD_CU-047_Recuperar-Contrasena.png` |
| CU-048 | Procesar Pago con MercadoPago | `DSS_CU-048_Procesar-Pago-Con-Mercadopago.png` | `DSD_CU-048_Procesar-Pago-Con-Mercadopago.png` |
| CU-049 | Consultar Balance / Ganancias del Chofer | `DSS_CU-049_Consultar-Balance-Ganancias-Del-Chofer.png` | `DSD_CU-049_Consultar-Balance-Ganancias-Del-Chofer.png` |
| CU-050 | Bloquear / Desbloquear Usuario | `DSS_CU-050_Bloquear-Desbloquear-Usuario.png` | `DSD_CU-050_Bloquear-Desbloquear-Usuario.png` |
| CU-051 | Consultar Listado de Vehículos | `DSS_CU-051_Gestionar-Vehiculos.png` | `DSD_CU-051_Gestionar-Vehiculos.png` |
| CU-052 | Registrar Distribuidora | `DSS_CU-052_Registrar-Distribuidora.png` | `DSD_CU-052_Registrar-Distribuidora.png` |
| CU-053 | Consultar Distribuidoras | `DSS_CU-053_Consultar-Distribuidoras.png` | `DSD_CU-053_Consultar-Distribuidoras.png` |
| CU-054 | Modificar Datos de la Distribuidora | `DSS_CU-054_Modificar-Datos-De-La-Distribuidora.png` | `DSD_CU-054_Modificar-Datos-De-La-Distribuidora.png` |
| CU-055 | Dar de Baja una Distribuidora | `DSS_CU-055_Dar-De-Baja-Una-Distribuidora.png` | `DSD_CU-055_Dar-De-Baja-Una-Distribuidora.png` |
| CU-056 | Definir Zona de Cobertura | `DSS_CU-056_Definir-Zona-De-Cobertura.png` | `DSD_CU-056_Definir-Zona-De-Cobertura.png` |
| CU-057 | Consultar Zonas de Cobertura | `DSS_CU-057_Consultar-Zonas-De-Cobertura.png` | `DSD_CU-057_Consultar-Zonas-De-Cobertura.png` |
| CU-058 | Validar Cobertura de una Dirección | `DSS_CU-058_Validar-Cobertura-De-Una-Direccion.png` | `DSD_CU-058_CU-005_Validar-Cobertura-De-Una-Direccion.png` |
| CU-059 | Eliminar Zona de Cobertura | `DSS_CU-059_Eliminar-Zona-De-Cobertura.png` | `DSD_CU-059_Eliminar-Zona-De-Cobertura.png` |
| CU-060 | Registrar Incidencia de Entrega | `DSS_CU-060_Registrar-Incidencia-De-Entrega.png` | `DSD_CU-060_Registrar-Incidencia-De-Entrega.png` |
| CU-061 | Listar Incidencias | `DSS_CU-061_Listar-Incidencias.png` | `DSD_CU-061_Listar-Incidencias.png` |
| CU-062 | Consultar Incidencias de un Pedido | `DSS_CU-062_Consultar-Incidencias-De-Un-Pedido.png` | `DSD_CU-062_Consultar-Incidencias-De-Un-Pedido.png` |
| CU-063 | Resolver Incidencia | `DSS_CU-063_Resolver-Incidencia.png` | `DSD_CU-063_Resolver-Incidencia.png` |
| CU-064 | Calificar Pedido (cliente↔chofer) | `DSS_CU-064_Calificar-Pedido.png` | `DSD_CU-064_CU-065_Calificar-Pedido.png` |
| CU-065 | Consultar Promedio de Calificaciones de un Usuario | `DSS_CU-065_Consultar-Promedio-De-Calificaciones-De-Un-Usuario.png` | `DSD_CU-064_CU-065_Calificar-Pedido.png` |
| CU-066 | Consultar Historial de Calificaciones Recibidas | `DSS_CU-066_Consultar-Historial-De-Calificaciones-Recibidas.png` | `DSD_CU-066_Consultar-Historial-De-Calificaciones-Recibidas.png` |
| CU-067 | Dar de Alta un Envase Físico | `DSS_CU-067_Dar-De-Alta-Un-Envase-Fisico.png` | `DSD_CU-067_Dar-De-Alta-Un-Envase-Fisico.png` |
| CU-068 | Asignar Envases a un Pedido | `DSS_CU-068_Asignar-Envases-A-Un-Pedido.png` | `DSD_CU-068_CU-070_Asignar-Envases-A-Un-Pedido.png` |
| CU-069 | Consultar el Parque de Envases | `DSS_CU-069_Consultar-El-Parque-De-Envases.png` | `DSD_CU-069_Consultar-El-Parque-De-Envases.png` |
| CU-070 | Registrar Movimiento de Envase (cambio de estado) | `DSS_CU-070_Registrar-Movimiento-De-Envase.png` | `DSD_CU-068_CU-070_Asignar-Envases-A-Un-Pedido.png` |
| CU-071 | Consultar Historial de Movimientos de un Envase | `DSS_CU-071_Consultar-Historial-De-Movimientos-De-Un-Envase.png` | `DSD_CU-071_Consultar-Historial-De-Movimientos-De-Un-Envase.png` |
| CU-072 | Crear Reserva Programada con Seña | `DSS_CU-072_Crear-Reserva-Programada-Con-Sena.png` | `DSD_CU-072_Crear-Reserva-Programada-Con-Sena.png` |
| CU-073 | Listar Reservas y Estado de la Seña | `DSS_CU-073_Listar-Reservas-Y-Estado-De-La-Sena.png` | `DSD_CU-073_Listar-Reservas-Y-Estado-De-La-Sena.png` |
| CU-074 | Confirmar Seña Cobrada en Efectivo | `DSS_CU-074_Confirmar-Sena-Cobrada-En-Efectivo.png` | `DSD_CU-074_Confirmar-Sena-Cobrada-En-Efectivo.png` |
| CU-075 | Activar Reservas Vencidas Automaticamente (Cron) | `DSS_CU-075_Activar-Reservas-Vencidas-Automaticamente.png` | `DSD_CU-075_CU-076_CU-077_Activar-Reservas-Vencidas-Automaticamente.png` |
| CU-076 | Expirar Reservas sin Seña Pagada (Cron) | `DSS_CU-076_Expirar-Reservas-Sin-Sena-Pagada.png` | `DSD_CU-075_CU-076_CU-077_Activar-Reservas-Vencidas-Automaticamente.png` |
| CU-077 | Expirar Pedidos de MercadoPago sin Pagar (Cron) | `DSS_CU-077_Expirar-Pedidos-De-Mercadopago-Sin-Pagar.png` | `DSD_CU-075_CU-076_CU-077_Activar-Reservas-Vencidas-Automaticamente.png` |
| CU-078 | Obtener el Código de Entrega (QR del chofer) | `DSS_CU-078_Obtener-El-Codigo-De-Entrega.png` | `DSD_CU-078_CU-079_Obtener-El-Codigo-De-Entrega.png` |
| CU-079 | Confirmar Entrega Escaneando el QR (cliente) | `DSS_CU-079_Confirmar-Entrega-Escaneando-El-Qr.png` | `DSD_CU-078_CU-079_Obtener-El-Codigo-De-Entrega.png` |
| CU-080 | Consultar el Pool de Pedidos Disponibles | `DSS_CU-080_Consultar-El-Pool-De-Pedidos-Disponibles.png` | `DSD_CU-080_Consultar-El-Pool-De-Pedidos-Disponibles.png` |
| CU-081 | Consultar los Pedidos Asignados al Chofer | `DSS_CU-081_Consultar-Los-Pedidos-Asignados-Al-Chofer.png` | `DSD_CU-081_Consultar-Los-Pedidos-Asignados-Al-Chofer.png` |
| CU-082 | Crear Usuario Base | — (caso incluido, sin diagrama propio) | `DSD_CU-082_Crear-Usuario-Base.png` |
| CU-083 | Buscar / Listar Usuarios | `DSS_CU-083_Buscar-Listar-Usuarios.png` | `DSD_CU-083_Buscar-Listar-Usuarios.png` |
| CU-084 | Verificar Existencia de Usuario (pre-registro) | `DSS_CU-084_Verificar-Existencia-De-Usuario.png` | `DSD_CU-084_Verificar-Existencia-De-Usuario.png` |
| CU-085 | Eliminar Usuario (baja lógica) | `DSS_CU-085_Eliminar-Usuario.png` | `DSD_CU-085_Eliminar-Usuario.png` |
| CU-086 | Registrar Administrador | `DSS_CU-086_Registrar-Administrador.png` | `DSD_CU-086_Registrar-Administrador.png` |
| CU-087 | Crear el Primer Super Administrador (bootstrap) | `DSS_CU-087_Crear-El-Primer-Super-Administrador.png` | `DSD_CU-087_Crear-El-Primer-Super-Administrador.png` |
| CU-088 | Consultar Administradores | `DSS_CU-088_Consultar-Administradores.png` | `DSD_CU-088_Consultar-Administradores.png` |
| CU-089 | Gestionar Roles del Sistema | `DSS_CU-089_Gestionar-Roles-Del-Sistema.png` | `DSD_CU-089_Gestionar-Roles-Del-Sistema.png` |
| CU-090 | Sembrar los Roles Iniciales | `DSS_CU-090_Sembrar-Los-Roles-Iniciales.png` | `DSD_CU-090_Sembrar-Los-Roles-Iniciales.png` |
| CU-091 | Validar Vigencia del Token de Sesión | `DSS_CU-091_Validar-Vigencia-Del-Token-De-Sesion.png` | `DSD_CU-091_Validar-Vigencia-Del-Token-De-Sesion.png` |
| CU-092 | Consultar Listado de Clientes | `DSS_CU-092_Consultar-Listado-De-Clientes.png` | `DSD_CU-092_Consultar-Listado-De-Clientes.png` |
| CU-094 | Actualizar Ubicación del Cliente | `DSS_CU-094_Actualizar-Ubicacion-Del-Cliente.png` | `DSD_CU-094_Actualizar-Ubicacion-Del-Cliente.png` |
| CU-095 | Eliminar Cliente (baja lógica) | `DSS_CU-095_Eliminar-Cliente.png` | `DSD_CU-095_Eliminar-Cliente.png` |
| CU-096 | Actualizar Perfil del Chofer | `DSS_CU-096_Actualizar-Perfil-Del-Chofer.png` | `DSD_CU-096_Actualizar-Perfil-Del-Chofer.png` |
| CU-097 | Eliminar Chofer (baja lógica) | `DSS_CU-097_Eliminar-Chofer.png` | `DSD_CU-097_Eliminar-Chofer.png` |
| CU-098 | Registrar el Token de Notificaciones del Dispositivo | `DSS_CU-098_Registrar-El-Token-De-Notificaciones-Del-Dispositivo.png` | `DSD_CU-098_Registrar-El-Token-De-Notificaciones-Del-Dispositivo.png` |
| CU-099 | Consultar los Tokens de un Usuario | `DSS_CU-099_Consultar-Los-Tokens-De-Un-Usuario.png` | `DSD_CU-099_Consultar-Los-Tokens-De-Un-Usuario.png` |
| CU-100 | Enviar Notificación de Prueba | `DSS_CU-100_Enviar-Notificacion-De-Prueba.png` | `DSD_CU-100_Enviar-Notificacion-De-Prueba.png` |
| CU-101 | Reenviar Notificación de Confirmación de Pedido | `DSS_CU-101_Reenviar-Notificacion-De-Confirmacion-De-Pedido.png` | `DSD_CU-101_Reenviar-Notificacion-De-Confirmacion-De-Pedido.png` |
| CU-102 | Probar el Servicio de Correo | `DSS_CU-102_Probar-El-Servicio-De-Correo.png` | `DSD_CU-102_Probar-El-Servicio-De-Correo.png` |
| CU-103 | Eliminar Franja Horaria | `DSS_CU-103_Eliminar-Franja-Horaria.png` | `DSD_CU-103_Eliminar-Franja-Horaria.png` |
| CU-104 | Verificar la Salud del Sistema (liveness / readiness) | `DSS_CU-104_Verificar-La-Salud-Del-Sistema.png` | `DSD_CU-104_Verificar-La-Salud-Del-Sistema.png` |
| CU-105 | Planificar el mantenimiento y las habilitaciones de la flota | `DSS_CU-105_Planificar-El-Mantenimiento-Y-Las-Habilitaciones-De-La-Flota.png` | `DSD_CU-105_Planificar-El-Mantenimiento-Y-Las-Habilitaciones-De-La-Flota.png` |
| CU-106 | Anticipar la recompra por consumo estimado | `DSS_CU-106_Anticipar-La-Recompra-Por-Consumo-Estimado.png` | `DSD_CU-106_Anticipar-La-Recompra-Por-Consumo-Estimado.png` |
| CU-107 | Agrupar pedidos por recorrido | `DSS_CU-107_Agrupar-Pedidos-Por-Recorrido.png` | `DSD_CU-107_Agrupar-Pedidos-Por-Recorrido.png` |
| CU-108 | Recuperar envases no devueltos | `DSS_CU-108_Recuperar-Envases-No-Devueltos.png` | `DSD_CU-108_Recuperar-Envases-No-Devueltos.png` |
| CU-109 | Consultar Detalle del Chofer | `DSS_CU-109_Consultar-Detalle-Del-Chofer.png` | `DSD_CU-109_Consultar-Detalle-Del-Chofer.png` |
| CU-110 | Buscar Chofer por Usuario | `DSS_CU-110_Buscar-Chofer-Por-Usuario.png` | `DSD_CU-110_Buscar-Chofer-Por-Usuario.png` |
| CU-111 | Editar Vehículo | `DSS_CU-111_Editar-Vehiculo.png` | `DSD_CU-111_Editar-Vehiculo.png` |
| CU-112 | Eliminar Vehículo | `DSS_CU-112_Eliminar-Vehiculo.png` | `DSD_CU-112_Eliminar-Vehiculo.png` |
| CU-113 | Consultar Detalle del Vehículo | `DSS_CU-113_Consultar-Detalle-Del-Vehiculo.png` | `DSD_CU-113_Consultar-Detalle-Del-Vehiculo.png` |
| CU-114 | Buscar Vehículo por Patente | `DSS_CU-114_Buscar-Vehiculo-Por-Patente.png` | `DSD_CU-114_Buscar-Vehiculo-Por-Patente.png` |
| CU-115 | Consultar Vehículos de un Chofer | `DSS_CU-115_Consultar-Vehiculos-De-Un-Chofer.png` | `DSD_CU-115_Consultar-Vehiculos-De-Un-Chofer.png` |
| CU-116 | Registrar Dirección de Entrega | `DSS_CU-116_Registrar-Direccion-de-Entrega.png` | `DSD_CU-116_Registrar-Direccion-de-Entrega.png` |
| CU-117 | Consultar Detalle de una Dirección de Entrega | `DSS_CU-117_Consultar-Detalle-de-una-Direccion-de-Entrega.png` | `DSD_CU-117_Consultar-Detalle-de-una-Direccion-de-Entrega.png` |
| CU-118 | Editar Dirección de Entrega | `DSS_CU-118_Editar-Direccion-de-Entrega.png` | `DSD_CU-118_Editar-Direccion-de-Entrega.png` |
| CU-119 | Eliminar Dirección de Entrega | `DSS_CU-119_Eliminar-Direccion-de-Entrega.png` | `DSD_CU-119_Eliminar-Direccion-de-Entrega.png` |
| CU-120 | Marcar una Dirección como Predeterminada | `DSS_CU-120_Marcar-una-Direccion-como-Predeterminada.png` | `DSD_CU-120_Marcar-una-Direccion-como-Predeterminada.png` |
| CU-121 | Consultar la Dirección Predeterminada | `DSS_CU-121_Consultar-la-Direccion-Predeterminada.png` | `DSD_CU-121_Consultar-la-Direccion-Predeterminada.png` |
| CU-122 | Agregar Ítem al Carrito | `DSS_CU-122_Agregar-Item-al-Carrito.png` | `DSD_CU-122_Agregar-Item-al-Carrito.png` |
| CU-123 | Modificar la Cantidad de un Ítem del Carrito | `DSS_CU-123_Modificar-la-Cantidad-de-un-Item-del-Carrito.png` | `DSD_CU-123_Modificar-la-Cantidad-de-un-Item-del-Carrito.png` |
| CU-124 | Quitar Ítem del Carrito | `DSS_CU-124_Quitar-Item-del-Carrito.png` | `DSD_CU-124_Quitar-Item-del-Carrito.png` |
| CU-125 | Consultar el Carrito | `DSS_CU-125_Consultar-el-Carrito.png` | `DSD_CU-125_Consultar-el-Carrito.png` |
| CU-126 | Vaciar el Carrito | `DSS_CU-126_Vaciar-el-Carrito.png` | `DSD_CU-126_Vaciar-el-Carrito.png` |
| CU-127 | Cambiar la Dirección de Entrega del Pedido | `DSS_CU-127_Cambiar-la-Direccion-de-Entrega-del-Pedido.png` | `DSD_CU-127_Cambiar-la-Direccion-de-Entrega-del-Pedido.png` |
| CU-128 | Indicar Quién Recibe el Pedido | `DSS_CU-128_Indicar-Quien-Recibe-el-Pedido.png` | `DSD_CU-128_Indicar-Quien-Recibe-el-Pedido.png` |
| CU-129 | Consultar Detalle del Cliente | `DSS_CU-129_Consultar-Detalle-del-Cliente.png` | `DSD_CU-129_Consultar-Detalle-del-Cliente.png` |
| CU-130 | Buscar Cliente por Usuario | `DSS_CU-130_Buscar-Cliente-por-Usuario.png` | `DSD_CU-130_Buscar-Cliente-por-Usuario.png` |
| CU-131 | Editar Datos del Cliente | `DSS_CU-131_Editar-Datos-del-Cliente.png` | `DSD_CU-131_Editar-Datos-del-Cliente.png` |
| CU-132 | Registrar la Revisión Periódica de un Envase | `DSS_CU-132_Registrar-la-Revision-Periodica-de-un-Envase.png` | `DSD_CU-132_Registrar-la-Revision-Periodica-de-un-Envase.png` |
| CU-133 | Consultar la Vigencia de un Envase | `DSS_CU-133_Consultar-la-Vigencia-de-un-Envase.png` | `DSD_CU-133_Consultar-la-Vigencia-de-un-Envase.png` |
| CU-134 | Consultar los Envases Próximos a Vencer | `DSS_CU-134_Consultar-los-Envases-Proximos-a-Vencer.png` | `DSD_CU-134_Consultar-los-Envases-Proximos-a-Vencer.png` |
| CU-135 | Bloquear el Despacho de un Envase Vencido | `DSS_CU-135_Bloquear-el-Despacho-de-un-Envase-Vencido.png` | `DSD_CU-135_Bloquear-el-Despacho-de-un-Envase-Vencido.png` |
| CU-136 | Registrar el Seguro del Vehículo | `DSS_CU-136_Registrar-el-Seguro-del-Vehiculo.png` | `DSD_CU-136_Registrar-el-Seguro-del-Vehiculo.png` |
| CU-137 | Registrar la Verificación Técnica Vehicular | `DSS_CU-137_Registrar-la-Verificacion-Tecnica-Vehicular.png` | `DSD_CU-137_Registrar-la-Verificacion-Tecnica-Vehicular.png` |
| CU-138 | Registrar la Licencia de Conducir del Chofer | `DSS_CU-138_Registrar-la-Licencia-de-Conducir-del-Chofer.png` | `DSD_CU-138_Registrar-la-Licencia-de-Conducir-del-Chofer.png` |
| CU-139 | Consultar los Vencimientos de la Flota | `DSS_CU-139_Consultar-los-Vencimientos-de-la-Flota.png` | `DSD_CU-139_Consultar-los-Vencimientos-de-la-Flota.png` |
| CU-140 | Programar un Mantenimiento de Vehículo | `DSS_CU-140_Programar-un-Mantenimiento-de-Vehiculo.png` | `DSD_CU-140_Programar-un-Mantenimiento-de-Vehiculo.png` |
| CU-141 | Registrar un Mantenimiento Realizado | `DSS_CU-141_Registrar-un-Mantenimiento-Realizado.png` | `DSD_CU-141_Registrar-un-Mantenimiento-Realizado.png` |
| CU-142 | Avisar los Vencimientos Próximos de la Flota | `DSS_CU-142_Avisar-los-Vencimientos-Proximos-de-la-Flota.png` | `DSD_CU-142_Avisar-los-Vencimientos-Proximos-de-la-Flota.png` |
| CU-143 | Declarar el Consumo Promedio al Registrarse | `DSS_CU-143_Declarar-el-Consumo-Promedio-al-Registrarse.png` | `DSD_CU-143_Declarar-el-Consumo-Promedio-al-Registrarse.png` |
| CU-144 | Actualizar el Consumo Promedio Declarado | `DSS_CU-144_Actualizar-el-Consumo-Promedio-Declarado.png` | `DSD_CU-144_Actualizar-el-Consumo-Promedio-Declarado.png` |
| CU-145 | Configurar los Días de Aviso Previo a la Recompra | `DSS_CU-145_Configurar-los-Dias-de-Aviso-Previo-a-la-Recompra.png` | `DSD_CU-145_Configurar-los-Dias-de-Aviso-Previo-a-la-Recompra.png` |
| CU-146 | Consultar la Fecha Estimada de Recompra | `DSS_CU-146_Consultar-la-Fecha-Estimada-de-Recompra.png` | `DSD_CU-146_Consultar-la-Fecha-Estimada-de-Recompra.png` |
| CU-147 | Realizar una Compra Express | `DSS_CU-147_Realizar-una-Compra-Express.png` | `DSD_CU-147_Realizar-una-Compra-Express.png` |
| CU-148 | Elegir la Modalidad de Entrega del Pedido | `DSS_CU-148_Elegir-la-Modalidad-de-Entrega-del-Pedido.png` | `DSD_CU-148_Elegir-la-Modalidad-de-Entrega-del-Pedido.png` |
| CU-149 | Despachar un Pedido Express a un Chofer en Moto | `DSS_CU-149_Despachar-un-Pedido-Express-a-un-Chofer-en-Moto.png` | `DSD_CU-149_Despachar-un-Pedido-Express-a-un-Chofer-en-Moto.png` |
| CU-150 | Programar la Vigencia de una Zona de Cobertura | `DSS_CU-150_Programar-La-Vigencia-De-Una-Zona-De-Cobertura.png` | `DSD_CU-150_Programar-La-Vigencia-De-Una-Zona-De-Cobertura.png` |
| CU-151 | Desactivar las Zonas de Cobertura Vencidas | `DSS_CU-151_Desactivar-Las-Zonas-De-Cobertura-Vencidas.png` | `DSD_CU-151_Desactivar-Las-Zonas-De-Cobertura-Vencidas.png` |
| CU-152 | Consultar el Registro de Auditoría | `DSS_CU-152_Consultar-El-Registro-De-Auditoria.png` | `DSD_CU-152_Consultar-El-Registro-De-Auditoria.png` |
| CU-153 | Registrar Toda Operación de Escritura | `DSS_CU-153_Registrar-Toda-Operacion-De-Escritura.png` | `DSD_CU-153_Registrar-Toda-Operacion-De-Escritura.png` |
| CU-154 | Consultar Listado de Franjas Horarias | `DSS_CU-154_Consultar-Listado-de-Franjas-Horarias.png` | `DSD_CU-154_Consultar-Listado-de-Franjas-Horarias.png` |
| CU-155 | Adjuntar Archivo a una Tarea de Flota | `DSS_CU-155_Adjuntar-Archivo-a-una-Tarea-de-Flota.png` | `DSD_CU-155_Adjuntar-Archivo-a-una-Tarea-de-Flota.png` |
| CU-156 | Consultar Adjuntos de una Tarea de Flota | `DSS_CU-156_Consultar-Adjuntos-de-una-Tarea-de-Flota.png` | `DSD_CU-156_Consultar-Adjuntos-de-una-Tarea-de-Flota.png` |
| CU-157 | Descargar un Adjunto de Flota | `DSS_CU-157_Descargar-un-Adjunto-de-Flota.png` | `DSD_CU-157_Descargar-un-Adjunto-de-Flota.png` |
| CU-158 | Eliminar un Adjunto de Flota | `DSS_CU-158_Eliminar-un-Adjunto-de-Flota.png` | `DSD_CU-158_Eliminar-un-Adjunto-de-Flota.png` |
| CU-159 | Almacenar Archivo | — (caso incluido, sin diagrama propio) | `DSD_CU-159_Almacenar-Archivo.png` |
| CU-160 | Recuperar Archivo | — (caso incluido, sin diagrama propio) | `DSD_CU-160_Recuperar-Archivo.png` |
| CU-161 | Poner un Vehículo en Uso para un Chofer | `DSS_CU-161_Poner-un-Vehiculo-en-Uso-para-un-Chofer.png` | `DSD_CU-161_Poner-un-Vehiculo-en-Uso-para-un-Chofer.png` |
| CU-162 | Liberar el Vehículo en Uso de un Chofer | `DSS_CU-162_Liberar-el-Vehiculo-en-Uso-de-un-Chofer.png` | `DSD_CU-162_Liberar-el-Vehiculo-en-Uso-de-un-Chofer.png` |
| CU-163 | Consultar el Vehículo en Uso de un Chofer | `DSS_CU-163_Consultar-el-Vehiculo-en-Uso-de-un-Chofer.png` | `DSD_CU-163_Consultar-el-Vehiculo-en-Uso-de-un-Chofer.png` |
| CU-164 | Consultar el Historial de Vehículos de un Chofer | `DSS_CU-164_Consultar-el-Historial-de-Vehiculos-de-un-Chofer.png` | `DSD_CU-164_Consultar-el-Historial-de-Vehiculos-de-un-Chofer.png` |
| CU-165 | Consultar el Historial de Choferes de un Vehículo | `DSS_CU-165_Consultar-el-Historial-de-Choferes-de-un-Vehiculo.png` | `DSD_CU-165_Consultar-el-Historial-de-Choferes-de-un-Vehiculo.png` |
| CU-166 | Tomar un Reclamo Pendiente | `DSS_CU-166_Tomar-un-Reclamo-Pendiente.png` | `DSD_CU-166_Tomar-un-Reclamo-Pendiente.png` |
| CU-167 | Reabrir un Reclamo | `DSS_CU-167_Reabrir-un-Reclamo.png` | `DSD_CU-167_Reabrir-un-Reclamo.png` |
| CU-168 | Reintegrar el Pago de un Pedido | `DSS_CU-168_Reintegrar-el-Pago-de-un-Pedido.png` | `DSD_CU-168_Reintegrar-el-Pago-de-un-Pedido.png` |
| CU-169 | Registrar el Cambio de Estado de un Pedido | `DSS_CU-169_Registrar-el-Cambio-de-Estado-de-un-Pedido.png` | `DSD_CU-169_Registrar-el-Cambio-de-Estado-de-un-Pedido.png` |
| CU-170 | Consultar el Historial de Estados de un Pedido | `DSS_CU-170_Consultar-el-Historial-de-Estados-de-un-Pedido.png` | `DSD_CU-170_Consultar-el-Historial-de-Estados-de-un-Pedido.png` |
| CU-171 | Configurar los Parámetros de Despacho de la Distribuidora | `DSS_CU-171_Configurar-los-Parametros-de-Despacho-de-la-Distribuidora.png` | `DSD_CU-171_Configurar-los-Parametros-de-Despacho-de-la-Distribuidora.png` |
| CU-172 | Configurar los Parámetros de un Proceso Automático | `DSS_CU-172_Configurar-los-Parametros-de-un-Proceso-Automatico.png` | `DSD_CU-172_Configurar-los-Parametros-de-un-Proceso-Automatico.png` |
| CU-173 | Configurar la Frecuencia de las Tareas Programadas | `DSS_CU-173_Configurar-la-Frecuencia-de-las-Tareas-Programadas.png` | `DSD_CU-173_Configurar-la-Frecuencia-de-las-Tareas-Programadas.png` |
| CU-174 | Adjuntar la Fotografía de un Reclamo | `DSS_CU-174_Adjuntar-la-Fotografia-de-un-Reclamo.png` | `DSD_CU-174_Adjuntar-la-Fotografia-de-un-Reclamo.png` |
| CU-175 | Consultar la Fotografía de un Reclamo | `DSS_CU-175_Consultar-la-Fotografia-de-un-Reclamo.png` | `DSD_CU-175_Consultar-la-Fotografia-de-un-Reclamo.png` |
