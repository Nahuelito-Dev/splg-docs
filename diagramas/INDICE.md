# Índice de Diagramas

**Proyecto:** SPLG — Sistema de Pedidos y Logística de Garrafas de Gas
**Fecha:** 2026-08-30

Cada diagrama está disponible en dos formatos: **PNG** para insertar en los documentos de
texto y **SVG** para conservar la calidad al ampliar. El código fuente de cada uno queda
junto a la imagen, por si hay que retocarlo.

| Carpeta | Contenido |
|---------|-----------|
| `diagramas/png/` | Diagramas de secuencia en PNG (211) |
| `diagramas/svg/` | Los mismos en SVG (211) |
| `diagramas/uml/` | Casos de uso en notación UML, PNG y SVG (19 de cada uno) |
| `diagramas/*.mmd` | Código Mermaid de cada diagrama de secuencia |
| `diagramas/uml/*.puml` | Código PlantUML de cada diagrama de casos de uso |

## Dónde va cada tipo de diagrama

| Diagrama | Documento | Sección |
|----------|-----------|---------|
| Casos de uso en notación UML | Documento 0 y Documento 1 | Diagrama de Casos de Uso del Sistema |
| Diagrama de secuencia del sistema (DSS) | Documento 2 — Análisis | 2.1 Comportamiento del Sistema |
| Diagrama de interacción de diseño (DSD) | Documento 3 — Diseño | 4. Diagramas de Interacción |

---

## Casos de uso en notación UML

| Archivo | Contenido |
|---------|-----------|
| `uml/CU_contexto` | Los cinco actores contra los 18 subsistemas. Delimita el sistema. |
| `uml/CU_SS-01` | SS-01 Autenticación y Usuarios — 11 casos de uso |
| `uml/CU_SS-02` | SS-02 Gestión de Pedidos — 30 casos de uso |
| `uml/CU_SS-03` | SS-03 Despacho y Asignación — 7 casos de uso |
| `uml/CU_SS-04` | SS-04 Seguimiento en Tiempo Real — 8 casos de uso |
| `uml/CU_SS-05` | SS-05 Reclamos — 3 casos de uso |
| `uml/CU_SS-06` | SS-06 Reportes y Dashboard — 5 casos de uso |
| `uml/CU_SS-07` | SS-07 Choferes y Vehículos — 24 casos de uso |
| `uml/CU_SS-08` | SS-08 Catálogo de Productos — 6 casos de uso |
| `uml/CU_SS-09` | SS-09 Franjas Horarias — 5 casos de uso |
| `uml/CU_SS-10` | SS-10 Multi-Distribuidora — 4 casos de uso |
| `uml/CU_SS-11` | SS-11 Cobertura Geográfica — 6 casos de uso |
| `uml/CU_SS-12` | SS-12 Incidencias y Calidad — 7 casos de uso |
| `uml/CU_SS-13` | SS-13 Trazabilidad de Envases — 10 casos de uso |
| `uml/CU_SS-14` | SS-14 Pagos y Conciliación — 1 caso de uso |
| `uml/CU_SS-15` | SS-15 Reservas Programadas — 6 casos de uso |
| `uml/CU_SS-16` | SS-16 Cuentas y Roles — 12 casos de uso |
| `uml/CU_SS-17` | SS-17 Notificaciones — 5 casos de uso |
| `uml/CU_SS-18` | SS-18 Observabilidad — 3 casos de uso |

---

## Diagramas por caso de uso

La columna **Estado** indica si el caso está construido. Los diagramas de los casos
especificados representan el comportamiento previsto, no el actual.

| CU | Caso de uso | Subsistema | Estado | Secuencia del sistema | Interacción de diseño |
|----|-------------|------------|--------|----------------------|----------------------|
| CU-001 | Iniciar Sesión | SS-01 | Implementado | `DSS_CU-001_cu-001-iniciar-sesión` | `DSD_CU-001_cu-001-iniciar-sesión` |
| CU-002 | Registrarse como Cliente | SS-01 | Implementado | `DSS_CU-002_cu-002-registrarse-como-cliente` | `DSD_CU-002_cu-002-registrarse-como-cliente` |
| CU-003 | Registrar Chofer | SS-01 | Implementado | `DSS_CU-003_cu-003-registrarse-como-chofer` | `DSD_CU-003_cu-003-registrar-chofer` |
| CU-004 | Gestionar Perfil de Usuario | SS-01 | Implementado | `DSS_CU-004_cu-004-gestionar-perfil-de-usuario` | `DSD_CU-004_cu-004-gestionar-perfil-de-usuario` |
| CU-005 | Crear Pedido | SS-02 | Implementado | `DSS_CU-005_cu-005-crear-pedido` | `DSD_CU-058_005_cu-058-cu-005-validación-de-zona-de-cobertura-al-crear-un-pe` |
| CU-006 | Consultar Detalle de Pedido | SS-02 | Implementado | `DSS_CU-006_cu-006-consultar-detalle-de-pedido` | `DSD_CU-006_cu-006-consultar-detalle-de-pedido` |
| CU-007 | Consultar Historial de Pedidos | SS-02 | Implementado | `DSS_CU-007_cu-007-consultar-historial-de-pedidos` | `DSD_CU-007_cu-007-consultar-historial-de-pedidos` |
| CU-008 | Cancelar Pedido (Cliente) | SS-02 | Implementado | `DSS_CU-008_cu-008-cancelar-pedido-cliente` | `DSD_CU-008_cu-008-cancelar-pedido-cliente` |
| CU-009 | Cancelar Pedido (Chofer) | SS-02 | Implementado | `DSS_CU-009_cu-009-cancelar-pedido-chofer` | `DSD_CU-009_cu-009-cancelar-pedido-chofer` |
| CU-010 | Cancelar Pedido (Administrador) | SS-02 | Implementado | `DSS_CU-010_cu-010-cancelar-pedido-administrador` | `DSD_CU-010_cu-010-cancelar-pedido-administrador` |
| CU-011 | Consultar Todos los Pedidos | SS-02 | Implementado | `DSS_CU-011_cu-011-listar-todos-los-pedidos` | `DSD_CU-011_cu-011-listar-todos-los-pedidos` |
| CU-012 | Asignar Chofer Manualmente | SS-03 | Implementado | `DSS_CU-012_cu-012-asignar-chofer-manualmente` | `DSD_CU-012_cu-012-asignar-chofer-manualmente` |
| CU-013 | Asignar Pedido Automáticamente por Proximidad | SS-03 | Implementado | `DSS_CU-013_cu-013-ofrecer-el-pedido-al-chofer-más-cercano` | `DSD_CU-013_cu-013-ofrecer-el-pedido-al-chofer-más-cercano-m1` |
| CU-014 | Reintentar Asignación con Radio Expandido (Cron) | SS-03 | Implementado | `DSS_CU-014_cu-014-vencer-la-oferta-y-ofrecer-al-siguiente-chofer` | `DSD_CU-014_cu-014-vencimiento-de-la-oferta-y-re-oferta-al-siguiente-m1-` |
| CU-015 | Aceptar Pedido | SS-03 | Implementado | `DSS_CU-015_cu-015-aceptar-pedido` | `DSD_CU-015_016_cu-015-cu-016-respuesta-del-chofer-a-la-oferta-aceptar-o-rec` |
| CU-016 | Rechazar / Ignorar Pedido | SS-03 | Implementado | `DSS_CU-016_cu-016-rechazar-ignorar-pedido` | `DSD_CU-015_016_cu-015-cu-016-respuesta-del-chofer-a-la-oferta-aceptar-o-rec` |
| CU-017 | Actualizar Ubicación GPS del Chofer | SS-04 | Implementado | `DSS_CU-017_cu-017-actualizar-ubicación-gps-del-chofer` | `DSD_CU-017_cu-017-actualización-de-la-ubicación-del-chofer` |
| CU-018 | Marcar Pedido "En Camino" | SS-04 | Implementado | `DSS_CU-018_cu-018-marcar-pedido-en-camino` | `DSD_CU-018_cu-018-marcar-pedido-en-camino` |
| CU-019 | Avisar Llegada al Cliente | SS-04 | Implementado | `DSS_CU-019_cu-019-avisar-llegada-al-cliente` | `DSD_CU-019_cu-019-avisar-llegada-al-cliente` |
| CU-020 | Confirmar Entrega | SS-04 | Implementado | `DSS_CU-020_cu-020-confirmar-entrega` | `DSD_CU-020_cu-020-confirmar-entrega-declaración-del-chofer` |
| CU-021 | Recibir Notificaciones en Tiempo Real | SS-04 | Implementado | `DSS_CU-021_cu-021-recibir-notificaciones-en-tiempo-real` | `DSD_CU-021_cu-021-recibir-notificaciones-en-tiempo-real` |
| CU-022 | Activar / Desactivar Disponibilidad (Chofer) | SS-04 | Implementado | `DSS_CU-022_cu-022-activar-desactivar-disponibilidad` | `DSD_CU-022_cu-022-activar-desactivar-disponibilidad` |
| CU-023 | Registrar Reclamo | SS-05 | Implementado | `DSS_CU-023_cu-023-registrar-reclamo` | `DSD_CU-023_cu-023-registrar-reclamo` |
| CU-024 | Listar Reclamos | SS-05 | Implementado | `DSS_CU-024_cu-024-listar-reclamos` | `DSD_CU-024_cu-024-listar-reclamos` |
| CU-025 | Resolver Reclamo | SS-05 | Implementado | `DSS_CU-025_cu-025-resolver-reclamo` | `DSD_CU-025_cu-025-resolver-reclamo` |
| CU-026 | Ver Dashboard General | SS-06 | Implementado | `DSS_CU-026_cu-026-ver-dashboard-general` | `DSD_CU-026_cu-026-ver-dashboard-general` |
| CU-027 | Ver Reporte de Ventas por Chofer | SS-06 | Implementado | `DSS_CU-027_cu-027-ver-reporte-de-ventas-por-chofer` | `DSD_CU-027_cu-027-ver-reporte-de-ventas-por-chofer` |
| CU-028 | Ver Reporte de Ventas por Producto | SS-06 | Implementado | `DSS_CU-028_cu-028-ver-reporte-de-ventas-por-producto` | `DSD_CU-028_cu-028-ver-reporte-de-ventas-por-producto` |
| CU-029 | Ver Reporte por Método de Pago | SS-06 | Implementado | `DSS_CU-029_cu-029-ver-reporte-por-método-de-pago` | `DSD_CU-029_cu-029-ver-reporte-por-método-de-pago` |
| CU-030 | Ver Gráfico de Ventas (últimos 7 días) | SS-06 | Implementado | `DSS_CU-030_cu-030-ver-gráfico-de-evolución-de-ventas` | `DSD_CU-030_cu-030-ver-gráfico-de-ventas` |
| CU-031 | Registrar Chofer | SS-07 | Implementado | `DSS_CU-031_cu-031-registrar-chofer` | `DSD_CU-031_cu-031-registrar-chofer` |
| CU-032 | Validar / Invalidar Chofer | SS-07 | Implementado | `DSS_CU-032_cu-032-validar-invalidar-chofer` | `DSD_CU-032_cu-032-validar-invalidar-chofer` |
| CU-033 | Activar / Desactivar Chofer (Admin) | SS-07 | Implementado | `DSS_CU-033_cu-033-activar-desactivar-chofer-administrador` | `DSD_CU-033_cu-033-activar-desactivar-chofer-admin` |
| CU-034 | Registrar Vehículo del Chofer | SS-07 | Implementado | `DSS_CU-034_cu-034-registrar-vehículo-del-chofer` | `DSD_CU-034_cu-034-registrar-vehículo-del-chofer` |
| CU-035 | Consultar Listado de Choferes | SS-07 | Implementado | `DSS_CU-035_cu-035-consultar-listado-de-choferes` | `DSD_CU-035_cu-035-consultar-listado-de-choferes` |
| CU-036 | Crear Producto (Garrafa) | SS-08 | Implementado | `DSS_CU-036_cu-036-crear-producto-garrafa` | `DSD_CU-036_cu-036-crear-producto-garrafa` |
| CU-037 | Actualizar Precio de Producto | SS-08 | Implementado | `DSS_CU-037_cu-037-actualizar-precio-de-producto` | `DSD_CU-037_cu-037-actualizar-precio-de-producto` |
| CU-038 | Actualizar Stock de Producto | SS-08 | Implementado | `DSS_CU-038_cu-038-actualizar-stock-de-producto` | `DSD_CU-038_cu-038-actualizar-stock-de-producto` |
| CU-039 | Configurar Promociones por Cantidad | SS-08 | Implementado | `DSS_CU-039_cu-039-configurar-promociones-por-cantidad` | `DSD_CU-039_cu-039-configurar-promociones-por-cantidad` |
| CU-040 | Activar / Desactivar Producto | SS-08 | Parcial | `DSS_CU-040_cu-040-activar-desactivar-producto` | `DSD_CU-040_cu-040-activar-desactivar-producto` |
| CU-041 | Consultar Catálogo de Productos | SS-08 | Implementado | `DSS_CU-041_cu-041-consultar-catálogo-de-productos` | `DSD_CU-041_cu-041-consultar-catálogo-de-productos` |
| CU-042 | Crear Franja Horaria | SS-09 | Implementado | `DSS_CU-042_cu-042-crear-franja-horaria` | `DSD_CU-042_cu-042-crear-franja-horaria` |
| CU-043 | Modificar Capacidad de Franja Horaria | SS-09 | No implementado | `DSS_CU-043_pendiente-de-construcción-dss-cu-043-modificar-capacidad-de-` | `DSD_CU-043_pendiente-de-construcción-dsd-cu-043-modificar-capacidad-de-` |
| CU-044 | Seleccionar Franja Horaria al Crear Pedido | SS-09 | Implementado | `DSS_CU-044_cu-044-seleccionar-franja-horaria-al-crear-pedido` | `DSD_CU-044_cu-044-seleccionar-franja-horaria-al-crear-pedido` |
| CU-045 | Consultar Franjas Horarias Disponibles | SS-09 | Implementado | `DSS_CU-045_cu-045-consultar-franjas-horarias-disponibles` | `DSD_CU-045_cu-045-consultar-franjas-horarias-disponibles` |
| CU-046 | Gestionar Direcciones de Entrega | SS-02 | Implementado | `DSS_CU-046_cu-046-gestionar-direcciones-de-entrega` | `DSD_CU-046_cu-046-gestionar-direcciones-de-entrega` |
| CU-047 | Recuperar Contraseña | SS-01 | Implementado | `DSS_CU-047_cu-047-recuperar-contraseña` | `DSD_CU-047_cu-047-recuperar-contraseña` |
| CU-048 | Procesar Pago con MercadoPago | SS-14 | Implementado | `DSS_CU-048_cu-048-procesar-pago-con-mercadopago` | `DSD_CU-048_cu-048-pago-con-pasarela-y-confirmación-por-webhook` |
| CU-049 | Consultar Balance / Ganancias del Chofer | SS-07 | Implementado | `DSS_CU-049_cu-049-consultar-balance-ganancias-del-chofer` | `DSD_CU-049_cu-049-consultar-balance-ganancias-del-chofer` |
| CU-050 | Bloquear / Desbloquear Usuario | SS-01 | Implementado | `DSS_CU-050_cu-050-bloquear-desbloquear-usuario` | `DSD_CU-050_cu-050-bloquear-desbloquear-usuario` |
| CU-051 | Gestionar Vehículos (editar / eliminar / consultar) | SS-07 | Implementado | `DSS_CU-051_cu-051-gestionar-vehículos` | `DSD_CU-051_cu-051-gestionar-vehículos-consultar-editar-eliminar` |
| CU-052 | Registrar Distribuidora | SS-10 | Implementado | `DSS_CU-052_cu-052-registrar-distribuidora` | `DSD_CU-052_cu-052-registrar-distribuidora` |
| CU-053 | Consultar Distribuidoras | SS-10 | Implementado | `DSS_CU-053_cu-053-consultar-distribuidoras` | `DSD_CU-053_cu-053-consultar-distribuidoras` |
| CU-054 | Modificar Datos de la Distribuidora | SS-10 | Implementado | `DSS_CU-054_cu-054-modificar-datos-de-la-distribuidora` | `DSD_CU-054_cu-054-modificar-datos-de-la-distribuidora` |
| CU-055 | Dar de Baja una Distribuidora | SS-10 | Implementado | `DSS_CU-055_cu-055-dar-de-baja-una-distribuidora` | `DSD_CU-055_cu-055-dar-de-baja-una-distribuidora` |
| CU-056 | Definir Zona de Cobertura | SS-11 | Implementado | `DSS_CU-056_cu-056-definir-zona-de-cobertura` | `DSD_CU-056_cu-056-definir-zona-de-cobertura` |
| CU-057 | Consultar Zonas de Cobertura | SS-11 | Implementado | `DSS_CU-057_cu-057-consultar-zonas-de-cobertura` | `DSD_CU-057_cu-057-consultar-zonas-de-cobertura` |
| CU-058 | Validar Cobertura de una Dirección | SS-11 | Implementado | `DSS_CU-058_cu-058-validar-cobertura-de-una-dirección` | `DSD_CU-058_005_cu-058-cu-005-validación-de-zona-de-cobertura-al-crear-un-pe` |
| CU-059 | Eliminar Zona de Cobertura | SS-11 | Implementado | `DSS_CU-059_cu-059-eliminar-zona-de-cobertura` | `DSD_CU-059_cu-059-eliminar-zona-de-cobertura` |
| CU-060 | Registrar Incidencia de Entrega | SS-12 | Implementado | `DSS_CU-060_cu-060-registrar-incidencia-de-entrega` | `DSD_CU-060_cu-060-registrar-incidencia-de-entrega` |
| CU-061 | Listar Incidencias | SS-12 | Implementado | `DSS_CU-061_cu-061-listar-incidencias` | `DSD_CU-061_cu-061-listar-incidencias` |
| CU-062 | Consultar Incidencias de un Pedido | SS-12 | Implementado | `DSS_CU-062_cu-062-consultar-incidencias-de-un-pedido` | `DSD_CU-062_cu-062-consultar-incidencias-de-un-pedido` |
| CU-063 | Resolver Incidencia | SS-12 | Implementado | `DSS_CU-063_cu-063-resolver-incidencia` | `DSD_CU-063_cu-063-resolver-incidencia` |
| CU-064 | Calificar Pedido (cliente↔chofer) | SS-12 | Implementado | `DSS_CU-064_cu-064-calificar-pedido` | `DSD_CU-064_065_cu-064-cu-065-calificación-bidireccional-y-recálculo-del-pro` |
| CU-065 | Consultar Promedio de Calificaciones de un Usuario | SS-12 | Implementado | `DSS_CU-065_cu-065-consultar-promedio-de-calificaciones-de-un-usuario` | `DSD_CU-064_065_cu-064-cu-065-calificación-bidireccional-y-recálculo-del-pro` |
| CU-066 | Consultar Historial de Calificaciones Recibidas | SS-12 | Implementado | `DSS_CU-066_cu-066-consultar-historial-de-calificaciones-recibidas` | `DSD_CU-066_cu-066-consultar-historial-de-calificaciones-recibidas` |
| CU-067 | Dar de Alta un Envase Físico | SS-13 | Implementado | `DSS_CU-067_cu-067-dar-de-alta-un-envase-físico` | `DSD_CU-067_cu-067-dar-de-alta-un-envase-físico` |
| CU-068 | Asignar Envases a un Pedido | SS-13 | Implementado | `DSS_CU-068_cu-068-asignar-envases-a-un-pedido` | `DSD_CU-068_070_cu-068-cu-070-ciclo-de-vida-del-envase-físico` |
| CU-069 | Consultar el Parque de Envases | SS-13 | Implementado | `DSS_CU-069_cu-069-consultar-el-parque-de-envases` | `DSD_CU-069_cu-069-consultar-el-parque-de-envases` |
| CU-070 | Registrar Movimiento de Envase (cambio de estado) | SS-13 | Implementado | `DSS_CU-070_cu-070-registrar-movimiento-de-envase` | `DSD_CU-068_070_cu-068-cu-070-ciclo-de-vida-del-envase-físico` |
| CU-071 | Consultar Historial de Movimientos de un Envase | SS-13 | Implementado | `DSS_CU-071_cu-071-consultar-historial-de-movimientos-de-un-envase` | `DSD_CU-071_cu-071-consultar-historial-de-movimientos-de-un-envase` |
| CU-072 | Crear Reserva Programada con Seña | SS-15 | Implementado | `DSS_CU-072_cu-072-crear-reserva-programada-con-seña` | `DSD_CU-072_cu-072-crear-reserva-programada-con-seña` |
| CU-073 | Listar Reservas y Estado de la Seña | SS-15 | Implementado | `DSS_CU-073_cu-073-listar-reservas-y-estado-de-la-seña` | `DSD_CU-073_cu-073-listar-reservas-y-estado-de-la-seña` |
| CU-074 | Confirmar Seña Cobrada en Efectivo | SS-15 | Implementado | `DSS_CU-074_cu-074-confirmar-seña-cobrada-en-efectivo` | `DSD_CU-074_cu-074-confirmar-seña-cobrada-en-efectivo` |
| CU-075 | Activar Reservas Vencidas Automaticamente (Cron) | SS-15 | Implementado | `DSS_CU-075_cu-075-activar-reservas-vencidas-automáticamente` | `DSD_CU-075_076_077_cu-075-cu-076-cu-077-los-tres-crons-de-reservas-y-pagos-pend` |
| CU-076 | Expirar Reservas sin Seña Pagada (Cron) | SS-15 | Implementado | `DSS_CU-076_cu-076-expirar-reservas-sin-seña-pagada` | `DSD_CU-075_076_077_cu-075-cu-076-cu-077-los-tres-crons-de-reservas-y-pagos-pend` |
| CU-077 | Expirar Pedidos de MercadoPago sin Pagar (Cron) | SS-15 | Implementado | `DSS_CU-077_cu-077-expirar-pedidos-de-mercadopago-sin-pagar` | `DSD_CU-075_076_077_cu-075-cu-076-cu-077-los-tres-crons-de-reservas-y-pagos-pend` |
| CU-078 | Consultar el Código de Entrega (QR del chofer) | SS-04 | Implementado | `DSS_CU-078_cu-078-obtener-el-código-de-entrega-qr-del-chofer` | `DSD_CU-078_079_cu-078-cu-079-entrega-verificada-por-qr-prueba-anti-fraude` |
| CU-079 | Confirmar Entrega Escaneando el QR (cliente) | SS-04 | Implementado | `DSS_CU-079_cu-079-confirmar-entrega-escaneando-el-qr-cliente` | `DSD_CU-078_079_cu-078-cu-079-entrega-verificada-por-qr-prueba-anti-fraude` |
| CU-080 | Consultar el Pool de Pedidos Disponibles | SS-02 | Implementado | `DSS_CU-080_cu-080-consultar-el-pool-de-pedidos-disponibles` | `DSD_CU-080_cu-080-consultar-el-pool-de-pedidos-disponibles` |
| CU-081 | Consultar los Pedidos Asignados al Chofer | SS-02 | Implementado | `DSS_CU-081_cu-081-consultar-los-pedidos-asignados-al-chofer` | `DSD_CU-081_cu-081-consultar-los-pedidos-asignados-al-chofer` |
| CU-082 | Crear Usuario Base | SS-01 | Implementado | `DSS_CU-082_cu-082-crear-usuario-base` | `DSD_CU-082_cu-082-crear-usuario-base` |
| CU-083 | Buscar / Listar Usuarios | SS-01 | Implementado | `DSS_CU-083_cu-083-buscar-listar-usuarios` | `DSD_CU-083_cu-083-buscar-listar-usuarios` |
| CU-084 | Verificar Existencia de Usuario (pre-registro) | SS-01 | Implementado | `DSS_CU-084_cu-084-verificar-existencia-de-usuario-pre-registro` | `DSD_CU-084_cu-084-verificar-existencia-de-usuario-pre-registro` |
| CU-085 | Eliminar Usuario (baja lógica) | SS-01 | Implementado | `DSS_CU-085_cu-085-eliminar-usuario-baja-lógica` | `DSD_CU-085_cu-085-eliminar-usuario-baja-lógica` |
| CU-086 | Registrar Administrador | SS-16 | Implementado | `DSS_CU-086_cu-086-registrar-administrador` | `DSD_CU-086_cu-086-registrar-administrador` |
| CU-087 | Crear el Primer Super Administrador (bootstrap) | SS-16 | Implementado | `DSS_CU-087_cu-087-crear-el-primer-super-administrador` | `DSD_CU-087_cu-087-crear-el-primer-super-administrador-bootstrap` |
| CU-088 | Consultar Administradores | SS-16 | Implementado | `DSS_CU-088_cu-088-consultar-administradores` | `DSD_CU-088_cu-088-consultar-administradores` |
| CU-089 | Gestionar Roles del Sistema | SS-16 | Implementado | `DSS_CU-089_cu-089-gestionar-roles-del-sistema` | `DSD_CU-089_cu-089-gestionar-roles-del-sistema` |
| CU-090 | Sembrar los Roles Iniciales | SS-16 | Implementado | `DSS_CU-090_cu-090-sembrar-los-roles-iniciales` | `DSD_CU-090_cu-090-sembrar-los-roles-iniciales` |
| CU-091 | Validar Vigencia del Token de Sesión | SS-01 | Implementado | `DSS_CU-091_cu-091-validar-vigencia-del-token-de-sesión` | `DSD_CU-091_cu-091-validar-vigencia-del-token-de-sesión` |
| CU-092 | Consultar Listado de Clientes | SS-16 | Implementado | `DSS_CU-092_cu-092-consultar-listado-de-clientes` | `DSD_CU-092_cu-092-consultar-listado-de-clientes` |
| CU-094 | Actualizar Ubicación del Cliente | SS-16 | Implementado | `DSS_CU-094_cu-094-actualizar-ubicación-del-cliente` | `DSD_CU-094_cu-094-actualizar-ubicación-del-cliente` |
| CU-095 | Eliminar Cliente (baja lógica) | SS-16 | Implementado | `DSS_CU-095_cu-095-eliminar-cliente-baja-lógica` | `DSD_CU-095_cu-095-eliminar-cliente-baja-lógica` |
| CU-096 | Actualizar Perfil del Chofer | SS-07 | Implementado | `DSS_CU-096_cu-096-actualizar-perfil-del-chofer` | `DSD_CU-096_cu-096-actualizar-perfil-del-chofer` |
| CU-097 | Eliminar Chofer (baja lógica) | SS-07 | Implementado | `DSS_CU-097_cu-097-eliminar-chofer-baja-lógica` | `DSD_CU-097_cu-097-eliminar-chofer-baja-lógica` |
| CU-098 | Registrar el Token de Notificaciones del Dispositivo | SS-17 | Implementado | `DSS_CU-098_cu-098-registrar-el-token-de-notificaciones-del-dispositivo` | `DSD_CU-098_cu-098-registrar-el-token-de-notificaciones-del-dispositivo` |
| CU-099 | Consultar los Tokens de un Usuario | SS-17 | Implementado | `DSS_CU-099_cu-099-consultar-los-tokens-de-un-usuario` | `DSD_CU-099_cu-099-consultar-los-tokens-de-un-usuario` |
| CU-100 | Enviar Notificación de Prueba | SS-17 | Implementado | `DSS_CU-100_cu-100-enviar-notificación-de-prueba` | `DSD_CU-100_cu-100-enviar-notificación-de-prueba` |
| CU-101 | Reenviar Notificación de Confirmación de Pedido | SS-17 | Implementado | `DSS_CU-101_cu-101-reenviar-notificación-de-confirmación-de-pedido` | `DSD_CU-101_cu-101-reenviar-notificación-de-confirmación-de-pedido` |
| CU-102 | Probar el Servicio de Correo | SS-17 | Implementado | `DSS_CU-102_cu-102-probar-el-servicio-de-correo` | `DSD_CU-102_cu-102-probar-el-servicio-de-correo` |
| CU-103 | Eliminar Franja Horaria | SS-09 | Implementado | `DSS_CU-103_cu-103-eliminar-franja-horaria` | `DSD_CU-103_cu-103-eliminar-franja-horaria` |
| CU-104 | Verificar la Salud del Sistema (liveness / readiness) | SS-18 | Implementado | `DSS_CU-104_cu-104-verificar-la-salud-del-sistema` | `DSD_CU-104_cu-104-verificar-la-salud-del-sistema-liveness-readiness` |
| CU-105 | Planificar el mantenimiento y las habilitaciones de la flota | SS-07 | Especificado | `DSS_CU-105_cu-105-planificar-el-mantenimiento-y-las-habilitaciones-de-l` | `DSD_CU-105_cu-105-planificar-el-mantenimiento-y-las-habilitaciones-de-l` |
| CU-106 | Anticipar la recompra por consumo estimado | SS-02 | Especificado | `DSS_CU-106_cu-106-anticipar-la-recompra-por-consumo-estimado` | `DSD_CU-106_cu-106-anticipar-la-recompra-por-consumo-estimado` |
| CU-107 | Agrupar pedidos por recorrido | SS-03 | Especificado | `DSS_CU-107_cu-107-agrupar-pedidos-por-recorrido` | `DSD_CU-107_cu-107-agrupar-pedidos-por-recorrido` |
| CU-108 | Recuperar envases no devueltos | SS-13 | Especificado | `DSS_CU-108_cu-108-recuperar-envases-no-devueltos` | `DSD_CU-108_cu-108-recuperar-envases-no-devueltos` |
