# Auditoría de Notación UML - Diagramas Mermaid

## R1 (DSS): Lifelines permitidas (solo actor y Sistema)
✅ Sin violaciones.

## R2 (DSS): Mensajes de entrada (operaciones de dominio con firma)
| Archivo | Línea | Qué dice | Qué debería decir |
|---|---|---|---|
| DSS_CU-105_Planificar-El-Mantenimiento-Y-Las-Habilitaciones-De-La-Flota.mmd | 17 | `                CHO->>SIS: aceptar la ventana propuesta` | Debe ser una operación del sistema con firma, ej: nombreOperacion() |
| DSS_CU-105_Planificar-El-Mantenimiento-Y-Las-Habilitaciones-De-La-Flota.mmd | 26 | `            ADM->>SIS: confirmar la ventana y el gasto del taller` | Debe ser una operación del sistema con firma, ej: nombreOperacion() |
| DSS_CU-106_Anticipar-La-Recompra-Por-Consumo-Estimado.mmd | 16 | `                CLI->>SIS: aceptar la invitacion` | Debe ser una operación del sistema con firma, ej: nombreOperacion() |
| DSS_CU-107_Agrupar-Pedidos-Por-Recorrido.mmd | 16 | `                CHO->>SIS: aceptar el recorrido` | Debe ser una operación del sistema con firma, ej: nombreOperacion() |
| DSS_CU-108_Recuperar-Envases-No-Devueltos.mmd | 21 | `                    CLI->>SIS: aceptar o no responder` | Debe ser una operación del sistema con firma, ej: nombreOperacion() |
| DSS_CU-108_Recuperar-Envases-No-Devueltos.mmd | 30 | `            ADM->>SIS: cobrar el deposito, dar de baja el envase o cerrar sin cargo` | Debe ser una operación del sistema con firma, ej: nombreOperacion() |


## R3 (DSS/DSD): Flechas de retorno (deben ser punteadas -->>)
| Archivo | Línea | Qué dice | Qué debería decir |
|---|---|---|---|
| DSD_CU-018_Marcar-Pedido-En-Camino.mmd | 38 | `                    UC->>UC: devuelve null sin activar tracking` | Cambiar '->>' por '-->>' para retornos |


## R4 (DSS/DSD): Fragmentos combinados sin guarda
✅ Sin violaciones.

## R5 (DSS/DSD): Falta autonumber o title
| Archivo | Línea | Qué dice | Qué debería decir |
|---|---|---|---|
| DSD_CU-001_Iniciar-Sesion.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-002_Registrarse-Como-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-003_Registrar-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-004_Gestionar-Perfil-De-Usuario.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-005_Crear-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-006_Consultar-Detalle-De-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-007_Consultar-Historial-De-Pedidos.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-008_Cancelar-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-009_Cancelar-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-010_Cancelar-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-011_Listar-Todos-Los-Pedidos.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-012_Asignar-Chofer-Manualmente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-013_Asignar-Pedido-Automaticamente-Por-Proximidad_Oferta-Al-Mas-Cercano.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-013_Asignar-Pedido-Automaticamente-Por-Proximidad_Vista-General.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-014_Reintentar-Asignacion-Con-Radio-Expandido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-015_CU-016_Aceptar-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-017_Actualizar-Ubicacion-Gps-Del-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-018_Marcar-Pedido-En-Camino.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-019_Avisar-Llegada-Al-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-020_Confirmar-Entrega.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-021_Recibir-Notificaciones-En-Tiempo-Real.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-022_Activar-Desactivar-Disponibilidad.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-023_Registrar-Reclamo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-024_Listar-Reclamos.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-025_Resolver-Reclamo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-026_Ver-Dashboard-General.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-027_Ver-Reporte-De-Ventas-Por-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-028_Ver-Reporte-De-Ventas-Por-Producto.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-029_Ver-Reporte-Por-Metodo-De-Pago.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-030_Ver-Grafico-De-Ventas.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-031_Registrar-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-032_Validar-Invalidar-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-033_Activar-Desactivar-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-034_Registrar-Vehiculo-Del-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-035_Consultar-Listado-De-Choferes.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-036_Crear-Producto.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-037_Actualizar-Precio-De-Producto.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-038_Actualizar-Stock-De-Producto.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-039_Configurar-Promociones-Por-Cantidad.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-040_Activar-Desactivar-Producto.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-041_Consultar-Catalogo-De-Productos.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-042_Crear-Franja-Horaria.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-043_Modificar-Capacidad-De-Franja-Horaria.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-044_Seleccionar-Franja-Horaria-Al-Crear-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-045_Consultar-Franjas-Horarias-Disponibles.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-046_Consultar-Direcciones-De-Entrega-Del-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-047_Recuperar-Contrasena.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-048_Procesar-Pago-Con-Mercadopago.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-049_Consultar-Balance-Ganancias-Del-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-050_Bloquear-Desbloquear-Usuario.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-051_Gestionar-Vehiculos.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-052_Registrar-Distribuidora.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-053_Consultar-Distribuidoras.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-054_Modificar-Datos-De-La-Distribuidora.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-055_Dar-De-Baja-Una-Distribuidora.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-056_Definir-Zona-De-Cobertura.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-057_Consultar-Zonas-De-Cobertura.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-058_CU-005_Validar-Cobertura-De-Una-Direccion.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-059_Eliminar-Zona-De-Cobertura.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-060_Registrar-Incidencia-De-Entrega.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-061_Listar-Incidencias.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-062_Consultar-Incidencias-De-Un-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-063_Resolver-Incidencia.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-064_CU-065_Calificar-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-066_Consultar-Historial-De-Calificaciones-Recibidas.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-067_Dar-De-Alta-Un-Envase-Fisico.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-068_CU-070_Asignar-Envases-A-Un-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-069_Consultar-El-Parque-De-Envases.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-071_Consultar-Historial-De-Movimientos-De-Un-Envase.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-072_Crear-Reserva-Programada-Con-Sena.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-073_Listar-Reservas-Y-Estado-De-La-Sena.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-074_Confirmar-Sena-Cobrada-En-Efectivo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-075_CU-076_CU-077_Activar-Reservas-Vencidas-Automaticamente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-078_CU-079_Obtener-El-Codigo-De-Entrega.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-080_Consultar-El-Pool-De-Pedidos-Disponibles.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-081_Consultar-Los-Pedidos-Asignados-Al-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-082_Crear-Usuario-Base.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-083_Buscar-Listar-Usuarios.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-084_Verificar-Existencia-De-Usuario.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-085_Eliminar-Usuario.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-086_Registrar-Administrador.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-087_Crear-El-Primer-Super-Administrador.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-088_Consultar-Administradores.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-089_Gestionar-Roles-Del-Sistema.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-090_Sembrar-Los-Roles-Iniciales.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-091_Validar-Vigencia-Del-Token-De-Sesion.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-092_Consultar-Listado-De-Clientes.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-093_Validar-Invalidar-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-094_Actualizar-Ubicacion-Del-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-095_Eliminar-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-096_Actualizar-Perfil-Del-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-097_Eliminar-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-098_Registrar-El-Token-De-Notificaciones-Del-Dispositivo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-099_Consultar-Los-Tokens-De-Un-Usuario.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-100_Enviar-Notificacion-De-Prueba.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-101_Reenviar-Notificacion-De-Confirmacion-De-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-102_Probar-El-Servicio-De-Correo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-103_Eliminar-Franja-Horaria.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-104_Verificar-La-Salud-Del-Sistema.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-105_Planificar-El-Mantenimiento-Y-Las-Habilitaciones-De-La-Flota.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-106_Anticipar-La-Recompra-Por-Consumo-Estimado.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-107_Agrupar-Pedidos-Por-Recorrido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-108_Recuperar-Envases-No-Devueltos.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-109_Consultar-Detalle-Del-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-110_Buscar-Chofer-Por-Usuario.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-111_Editar-Vehiculo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-112_Eliminar-Vehiculo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-113_Consultar-Detalle-Del-Vehiculo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-114_Buscar-Vehiculo-Por-Patente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-115_Consultar-Vehiculos-De-Un-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-116_Registrar-Direccion-de-Entrega.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-117_Consultar-Detalle-de-una-Direccion-de-Entrega.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-118_Editar-Direccion-de-Entrega.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-119_Eliminar-Direccion-de-Entrega.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-120_Marcar-una-Direccion-como-Predeterminada.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-121_Consultar-la-Direccion-Predeterminada.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-122_Agregar-Item-al-Carrito.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-123_Modificar-la-Cantidad-de-un-Item-del-Carrito.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-124_Quitar-Item-del-Carrito.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-125_Consultar-el-Carrito.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-126_Vaciar-el-Carrito.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-127_Cambiar-la-Direccion-de-Entrega-del-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-128_Indicar-Quien-Recibe-el-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-129_Consultar-Detalle-del-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-130_Buscar-Cliente-por-Usuario.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-131_Editar-Datos-del-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-132_Registrar-la-Revision-Periodica-de-un-Envase.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-133_Consultar-la-Vigencia-de-un-Envase.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-134_Consultar-los-Envases-Proximos-a-Vencer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-135_Bloquear-el-Despacho-de-un-Envase-Vencido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-136_Registrar-el-Seguro-del-Vehiculo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-137_Registrar-la-Verificacion-Tecnica-Vehicular.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-138_Registrar-la-Licencia-de-Conducir-del-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-139_Consultar-los-Vencimientos-de-la-Flota.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-140_Programar-un-Mantenimiento-de-Vehiculo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-141_Registrar-un-Mantenimiento-Realizado.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-142_Avisar-los-Vencimientos-Proximos-de-la-Flota.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-143_Declarar-el-Consumo-Promedio-al-Registrarse.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-144_Actualizar-el-Consumo-Promedio-Declarado.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-145_Configurar-los-Dias-de-Aviso-Previo-a-la-Recompra.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-146_Consultar-la-Fecha-Estimada-de-Recompra.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-147_Realizar-una-Compra-Express.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-148_Elegir-la-Modalidad-de-Entrega-del-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSD_CU-149_Despachar-un-Pedido-Express-a-un-Chofer-en-Moto.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-001_Iniciar-Sesion.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-002_Registrarse-Como-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-003_Registrar-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-004_Gestionar-Perfil-De-Usuario.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-005_Crear-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-006_Consultar-Detalle-De-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-007_Consultar-Historial-De-Pedidos.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-008_Cancelar-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-009_Cancelar-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-010_Cancelar-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-011_Listar-Todos-Los-Pedidos.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-012_Asignar-Chofer-Manualmente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-013_Asignar-Pedido-Automaticamente-Por-Proximidad.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-014_Reintentar-Asignacion-Con-Radio-Expandido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-015_Aceptar-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-016_Rechazar-Ignorar-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-017_Actualizar-Ubicacion-Gps-Del-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-018_Marcar-Pedido-En-Camino.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-019_Avisar-Llegada-Al-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-020_Confirmar-Entrega.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-021_Recibir-Notificaciones-En-Tiempo-Real.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-022_Activar-Desactivar-Disponibilidad.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-023_Registrar-Reclamo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-024_Listar-Reclamos.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-025_Resolver-Reclamo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-026_Ver-Dashboard-General.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-027_Ver-Reporte-De-Ventas-Por-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-028_Ver-Reporte-De-Ventas-Por-Producto.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-029_Ver-Reporte-Por-Metodo-De-Pago.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-030_Ver-Grafico-De-Ventas.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-031_Registrar-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-032_Validar-Invalidar-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-033_Activar-Desactivar-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-034_Registrar-Vehiculo-Del-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-035_Consultar-Listado-De-Choferes.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-036_Crear-Producto.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-037_Actualizar-Precio-De-Producto.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-038_Actualizar-Stock-De-Producto.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-039_Configurar-Promociones-Por-Cantidad.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-040_Activar-Desactivar-Producto.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-041_Consultar-Catalogo-De-Productos.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-042_Crear-Franja-Horaria.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-043_Modificar-Capacidad-De-Franja-Horaria.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-044_Seleccionar-Franja-Horaria-Al-Crear-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-045_Consultar-Franjas-Horarias-Disponibles.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-046_Consultar-Direcciones-De-Entrega-Del-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-047_Recuperar-Contrasena.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-048_Procesar-Pago-Con-Mercadopago.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-049_Consultar-Balance-Ganancias-Del-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-050_Bloquear-Desbloquear-Usuario.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-051_Gestionar-Vehiculos.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-052_Registrar-Distribuidora.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-053_Consultar-Distribuidoras.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-054_Modificar-Datos-De-La-Distribuidora.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-055_Dar-De-Baja-Una-Distribuidora.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-056_Definir-Zona-De-Cobertura.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-057_Consultar-Zonas-De-Cobertura.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-058_Validar-Cobertura-De-Una-Direccion.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-059_Eliminar-Zona-De-Cobertura.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-060_Registrar-Incidencia-De-Entrega.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-061_Listar-Incidencias.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-062_Consultar-Incidencias-De-Un-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-063_Resolver-Incidencia.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-064_Calificar-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-065_Consultar-Promedio-De-Calificaciones-De-Un-Usuario.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-066_Consultar-Historial-De-Calificaciones-Recibidas.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-067_Dar-De-Alta-Un-Envase-Fisico.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-068_Asignar-Envases-A-Un-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-069_Consultar-El-Parque-De-Envases.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-070_Registrar-Movimiento-De-Envase.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-071_Consultar-Historial-De-Movimientos-De-Un-Envase.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-072_Crear-Reserva-Programada-Con-Sena.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-073_Listar-Reservas-Y-Estado-De-La-Sena.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-074_Confirmar-Sena-Cobrada-En-Efectivo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-075_Activar-Reservas-Vencidas-Automaticamente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-076_Expirar-Reservas-Sin-Sena-Pagada.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-077_Expirar-Pedidos-De-Mercadopago-Sin-Pagar.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-078_Obtener-El-Codigo-De-Entrega.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-079_Confirmar-Entrega-Escaneando-El-Qr.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-080_Consultar-El-Pool-De-Pedidos-Disponibles.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-081_Consultar-Los-Pedidos-Asignados-Al-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-082_Crear-Usuario-Base.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-083_Buscar-Listar-Usuarios.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-084_Verificar-Existencia-De-Usuario.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-085_Eliminar-Usuario.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-086_Registrar-Administrador.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-087_Crear-El-Primer-Super-Administrador.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-088_Consultar-Administradores.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-089_Gestionar-Roles-Del-Sistema.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-090_Sembrar-Los-Roles-Iniciales.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-091_Validar-Vigencia-Del-Token-De-Sesion.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-092_Consultar-Listado-De-Clientes.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-093_Validar-Invalidar-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-094_Actualizar-Ubicacion-Del-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-095_Eliminar-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-096_Actualizar-Perfil-Del-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-097_Eliminar-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-098_Registrar-El-Token-De-Notificaciones-Del-Dispositivo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-099_Consultar-Los-Tokens-De-Un-Usuario.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-100_Enviar-Notificacion-De-Prueba.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-101_Reenviar-Notificacion-De-Confirmacion-De-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-102_Probar-El-Servicio-De-Correo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-103_Eliminar-Franja-Horaria.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-104_Verificar-La-Salud-Del-Sistema.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-105_Planificar-El-Mantenimiento-Y-Las-Habilitaciones-De-La-Flota.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-106_Anticipar-La-Recompra-Por-Consumo-Estimado.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-107_Agrupar-Pedidos-Por-Recorrido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-108_Recuperar-Envases-No-Devueltos.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-109_Consultar-Detalle-Del-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-110_Buscar-Chofer-Por-Usuario.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-111_Editar-Vehiculo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-112_Eliminar-Vehiculo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-113_Consultar-Detalle-Del-Vehiculo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-114_Buscar-Vehiculo-Por-Patente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-115_Consultar-Vehiculos-De-Un-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-116_Registrar-Direccion-de-Entrega.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-117_Consultar-Detalle-de-una-Direccion-de-Entrega.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-118_Editar-Direccion-de-Entrega.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-119_Eliminar-Direccion-de-Entrega.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-120_Marcar-una-Direccion-como-Predeterminada.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-121_Consultar-la-Direccion-Predeterminada.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-122_Agregar-Item-al-Carrito.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-123_Modificar-la-Cantidad-de-un-Item-del-Carrito.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-124_Quitar-Item-del-Carrito.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-125_Consultar-el-Carrito.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-126_Vaciar-el-Carrito.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-127_Cambiar-la-Direccion-de-Entrega-del-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-128_Indicar-Quien-Recibe-el-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-129_Consultar-Detalle-del-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-130_Buscar-Cliente-por-Usuario.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-131_Editar-Datos-del-Cliente.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-132_Registrar-la-Revision-Periodica-de-un-Envase.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-133_Consultar-la-Vigencia-de-un-Envase.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-134_Consultar-los-Envases-Proximos-a-Vencer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-135_Bloquear-el-Despacho-de-un-Envase-Vencido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-136_Registrar-el-Seguro-del-Vehiculo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-137_Registrar-la-Verificacion-Tecnica-Vehicular.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-138_Registrar-la-Licencia-de-Conducir-del-Chofer.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-139_Consultar-los-Vencimientos-de-la-Flota.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-140_Programar-un-Mantenimiento-de-Vehiculo.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-141_Registrar-un-Mantenimiento-Realizado.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-142_Avisar-los-Vencimientos-Proximos-de-la-Flota.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-143_Declarar-el-Consumo-Promedio-al-Registrarse.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-144_Actualizar-el-Consumo-Promedio-Declarado.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-145_Configurar-los-Dias-de-Aviso-Previo-a-la-Recompra.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-146_Consultar-la-Fecha-Estimada-de-Recompra.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-147_Realizar-una-Compra-Express.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-148_Elegir-la-Modalidad-de-Entrega-del-Pedido.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |
| DSS_CU-149_Despachar-un-Pedido-Express-a-un-Chofer-en-Moto.mmd | 1 | `(Falta title en el archivo)` | Agregar 'title Nombre del Caso de Uso' al inicio |


## R6 (DSD): Lifelines con rótulos genéricos (Sistema, Backend, etc.)
| Archivo | Línea | Qué dice | Qué debería decir |
|---|---|---|---|
| DSD_CU-017_Actualizar-Ubicacion-Gps-Del-Chofer.mmd | 3 | `    participant APP as App Chofer` | Usar nombre de clase/objeto real, no rótulos genéricos |
| DSD_CU-078_CU-079_Obtener-El-Codigo-De-Entrega.mmd | 3 | `    participant CHO as App Chofer` | Usar nombre de clase/objeto real, no rótulos genéricos |
| DSD_CU-078_CU-079_Obtener-El-Codigo-De-Entrega.mmd | 4 | `    participant CLI as App Cliente` | Usar nombre de clase/objeto real, no rótulos genéricos |
| DSD_CU-098_Registrar-El-Token-De-Notificaciones-Del-Dispositivo.mmd | 3 | `    participant APP as App Cliente o App Chofer` | Usar nombre de clase/objeto real, no rótulos genéricos |


## R8 (DSD): Actor invoca directamente a Repositorio/DB
✅ Sin violaciones.

## RESUMEN CONTABLE
- **Total de archivos auditados:** 293
- **Archivos que cumplen TODAS las reglas:** 0

### Conteo por Regla
| Regla | Archivos Afectados | Ocurrencias |
|---|---|---|
| R1 | 0 | 0 |
| R2 | 4 | 6 |
| R3 | 1 | 1 |
| R4 | 0 | 0 |
| R5 | 293 | 293 |
| R6 | 3 | 4 |
| R8 | 0 | 0 |


### Top 20 Archivos más graves
| Archivo | Reglas Violadas | Ocurrencias | Detalle Reglas |
|---|---|---|---|
| DSD_CU-078_CU-079_Obtener-El-Codigo-De-Entrega.mmd | 2 | 3 | R5, R6 |
| DSS_CU-105_Planificar-El-Mantenimiento-Y-Las-Habilitaciones-De-La-Flota.mmd | 2 | 3 | R2, R5 |
| DSS_CU-108_Recuperar-Envases-No-Devueltos.mmd | 2 | 3 | R2, R5 |
| DSD_CU-017_Actualizar-Ubicacion-Gps-Del-Chofer.mmd | 2 | 2 | R5, R6 |
| DSD_CU-018_Marcar-Pedido-En-Camino.mmd | 2 | 2 | R3, R5 |
| DSD_CU-098_Registrar-El-Token-De-Notificaciones-Del-Dispositivo.mmd | 2 | 2 | R5, R6 |
| DSS_CU-106_Anticipar-La-Recompra-Por-Consumo-Estimado.mmd | 2 | 2 | R2, R5 |
| DSS_CU-107_Agrupar-Pedidos-Por-Recorrido.mmd | 2 | 2 | R2, R5 |
| DSD_CU-001_Iniciar-Sesion.mmd | 1 | 1 | R5 |
| DSD_CU-002_Registrarse-Como-Cliente.mmd | 1 | 1 | R5 |
| DSD_CU-003_Registrar-Chofer.mmd | 1 | 1 | R5 |
| DSD_CU-004_Gestionar-Perfil-De-Usuario.mmd | 1 | 1 | R5 |
| DSD_CU-005_Crear-Pedido.mmd | 1 | 1 | R5 |
| DSD_CU-006_Consultar-Detalle-De-Pedido.mmd | 1 | 1 | R5 |
| DSD_CU-007_Consultar-Historial-De-Pedidos.mmd | 1 | 1 | R5 |
| DSD_CU-008_Cancelar-Pedido.mmd | 1 | 1 | R5 |
| DSD_CU-009_Cancelar-Pedido.mmd | 1 | 1 | R5 |
| DSD_CU-010_Cancelar-Pedido.mmd | 1 | 1 | R5 |
| DSD_CU-011_Listar-Todos-Los-Pedidos.mmd | 1 | 1 | R5 |
| DSD_CU-012_Asignar-Chofer-Manualmente.mmd | 1 | 1 | R5 |