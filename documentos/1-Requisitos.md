# Documento de Requisitos del Sistema
**Proyecto:** SPLG – Sistema de Pedidos y Logística de Garrafas de Gas
**Versión:** 2.0
**Fecha:** 31/10/2026
**Realizado por:** Nahuel Wagner
**Realizado para:** Distribuidor de Gas Envasado (Cliente Real)
**Institución:** FCEQyN – UNaM
**Metodología:** Proceso Unificado (PU)

---

## Índice de Figuras

- Figura 1 — Diagrama de casos de uso del sistema por subsistemas
- Figura 2 — Diagrama de contexto del sistema
- Figura 3 — Diagrama de Subsistemas
- Figura 4 — SS-01 Autenticación y Usuarios: casos de uso
- Figura 5 — SS-02 Gestión de Pedidos, parte 1 de 2: casos de uso
- Figura 6 — SS-02 Gestión de Pedidos, parte 2 de 2: casos de uso
- Figura 7 — SS-03 Despacho y Asignación: casos de uso
- Figura 8 — SS-04 Seguimiento en Tiempo Real: casos de uso
- Figura 9 — SS-05 Reclamos: casos de uso
- Figura 10 — SS-06 Reportes y Tablero: casos de uso
- Figura 11 — SS-07 Gestión de Choferes y Vehículos: casos de uso, choferes (lámina 1 de 3)
- Figura 12 — SS-07 Gestión de Choferes y Vehículos: casos de uso, vehículos y vencimientos (lámina 2 de 3)
- Figura 13 — SS-07 Gestión de Choferes y Vehículos: casos de uso, costos, siniestros y adjuntos de flota (lámina 3 de 3)
- Figura 14 — SS-08 Gestión de Productos e Inventario, parte 1 de 2: casos de uso
- Figura 15 — SS-08 Gestión de Productos e Inventario, parte 2 de 2: casos de uso
- Figura 16 — SS-09 Franjas Horarias: casos de uso
- Figura 17 — SS-10 Multi-Distribuidora: casos de uso
- Figura 18 — SS-11 Cobertura Geográfica: casos de uso
- Figura 19 — SS-12 Incidencias y Calidad de Servicio: casos de uso
- Figura 20 — SS-13 Trazabilidad de Envases: casos de uso
- Figura 21 — SS-14 Pagos y Conciliación: casos de uso
- Figura 22 — SS-15 Reservas Programadas: casos de uso
- Figura 23 — SS-16 Administración de Cuentas y Roles: casos de uso
- Figura 24 — SS-17 Notificaciones y Mensajería: casos de uso
- Figura 25 — SS-18 Observabilidad y Operación: casos de uso
- Figura 26 — SS-19 Personal y Legajos: casos de uso
- Figura 27 — SS-20 Compras: casos de uso
- Figura 28 — SS-21 Caja, Rendiciones y Cuentas Corrientes, parte 1 de 2: casos de uso
- Figura 29 — SS-21 Caja, Rendiciones y Cuentas Corrientes, parte 2 de 2: casos de uso
- Figura 30 — Actores del sistema y el canal por el que operan

---

## Leyenda de Prioridad

| Indicador | Prioridad | Significado |
|:---------:|-----------|-------------|
| C | **Crítico** | El sistema no puede funcionar sin este elemento. Debe implementarse en las primeras iteraciones. |
| I | **Importante** | Agrega valor significativo al sistema. Forma parte del MVP pero no bloquea la operación base. |
| S | **Secundario** | Deseable pero prescindible en Fase 1. Puede diferirse a iteraciones posteriores. |
| M | **Menor** | Mejora de bajo impacto, que puede quedar para el final sin afectar la operación. |

El indicador **A** (*automático*) no es una prioridad sino una marca: señala el proceso que el sistema ejecuta sin intervención humana y se combina con cualquiera de las prioridades anteriores (por ejemplo, «C, A»).

---

---

## Lista de Cambios

| Nro | Fecha | Descripción | Autor |
|-----|-------|-------------|-------|
| 0 | 17/04/2026 | Versión inicial. | Nahuel Wagner |
| 1 | 03/05/2026 | Nombre del sistema corregido a SPLG. Requisito de información sobre pagos. Primeros casos de uso expandidos, requisitos no funcionales de mantenibilidad y confiabilidad, matriz de rastreabilidad y glosario. | Nahuel Wagner |
| 2 | 30/08/2026 | Verificación de la especificación contra el sistema construido: campos completos en los casos de uso expandidos, objetivos OBJ-09 a OBJ-15 y requisitos de información IRQ-09 a IRQ-15 (varias distribuidoras, cobertura, incidencias, calificaciones, envases, reservas y estado operativo). | Nahuel Wagner |
| 3 | 01/10/2026 | Requisito no funcional de aislamiento entre distribuidoras, consulta del registro de auditoría, vehículo en uso por chofer y nuevas operaciones sobre los reclamos. Diagrama de contexto en las fronteras del sistema y objetivos de la iteración reformulados. | Nahuel Wagner |
| 4 | 07/10/2026 | Ampliación del alcance a la gestión de la empresa: personal y legajos, flota ampliada, stock físico, compras y carga del camión, y caja y rendición, con los requisitos de información IRQ-17 a IRQ-19. Cada operación de alta, baja y modificación pasa a ser su propio caso de uso. | Nahuel Wagner |
| 5 | 18/10/2026 | Casos de uso expandidos actualizados según lo construido: stock físico, compras, carga y rendición del camión, cobros, historial de estados del pedido y parámetros del despacho. Estado de cada caso alineado con el plan de iteraciones. | Nahuel Wagner |
| 6 | 24/10/2026 | Revisión de contenido: cantidades por calificación, definición del Sistema Automático como el Tiempo, cuentas de los clientes, reservas con seña y reglas de validación en la aplicación, en el sistema y en la base de datos. | Nahuel Wagner |
| 7 | 31/10/2026 | Se reduce el alcance documentado a los 21 casos de uso esenciales: el circuito completo del pedido, los cinco módulos inteligentes y la consulta de la auditoría conservan su caso de uso expandido, y los demás casos quedan en la lista de casos de uso con su importancia y en el diagrama de su subsistema. El documento sigue el orden de la plantilla de la cátedra. Los módulos inteligentes M2 a M5 pasan a implementados y la auditoría registra todo cambio de datos desde la base de datos (IRQ-16, NFR-10 y CU-152). Se retiran del alcance las ganancias del chofer y las comisiones por entrega con su liquidación (CU-049, CU-240 a CU-244, CU-333 a CU-335 y CU-347), porque el chofer cobra un sueldo mensual. Los requisitos no funcionales expresan la meta sin el mecanismo técnico y el glosario queda con los términos del negocio. | Nahuel Wagner |

---

## 1. Presentación General

*Descripción breve de las principales características del sistema de software que se va a desarrollar, la situación actual que generar la necesidad de un nuevo desarrollo, la problemática que se acomete, y cualquier otra consideración que sitúe al posible lector en el contexto oportuno para comprender el resto del documento*

El proyecto SPLG surge de la necesidad de digitalizar la operación de un distribuidor de gas envasado que actualmente gestiona todos sus procesos de forma analógica: los clientes realizan pedidos por teléfono, los choferes reciben instrucciones verbales y el stock se registra manualmente en planillas. Esta situación genera demoras en la atención, errores en los pedidos, imposibilidad de rastrear entregas y reclamos sin evidencia objetiva.

El sistema propuesto integra cuatro componentes: una **App Cliente** (Flutter) para realizar pedidos y hacer seguimiento en tiempo real, una **App Chofer** (Flutter) para gestionar las entregas con GPS, un **Panel Administrativo** (React/Vite) para la gestión operativa completa, y un **Backend API** (NestJS) que centraliza toda la lógica de negocio, la base de datos PostgreSQL, el caché Redis y las notificaciones Firebase.

### Participantes del Proyecto

*Debe contener una lista con todos los participantes en el proyecto:*

| Rol | Nombre |
|-----|--------|
| Desarrollador / Analista | Nahuel Wagner |
| Cliente / Usuario Final | Distribuidor de Gas Envasado |
| Docente Supervisor | Lic. Sergio Daniel Caballero |
| Institución | FCEQyN – UNaM |

---
## 2. Objetivos del Sistema

*Se debe hacer una lista con los objetivos que se esperan alcanzar con el software a desarrollar.*

| Código | Prioridad | Objetivo | Descripción | Estabilidad | Comentarios |
|--------|:---------:|----------|-------------|:-----------:|-------------|
| OBJ-01 | C | Digitalizar la gestión de pedidos | Reemplazar el flujo telefónico por una plataforma digital donde el cliente realice pedidos de forma autónoma desde la app móvil, sin intervención del operador para registrar el pedido. | Alta | Cubierto por el circuito de pedidos (SS-02): el cliente hace el pedido solo desde su aplicación. |
| OBJ-02 | C, A | Automatizar la asignación de pedidos | Asignar los pedidos sin intervención del operador, ofreciéndolos de a un chofer por vez —el más cercano al domicilio de entrega que aún no haya sido contactado— con una ventana de aceptación acotada y ampliación progresiva del radio de búsqueda. | Alta | Cubierto por el despacho por proximidad (SS-03); la asignación manual queda como excepción del administrador. |
| OBJ-03 | C | Proveer seguimiento en tiempo real | Permitir al cliente ver la ubicación del chofer en un mapa mientras su pedido está en camino, mediante una conexión en tiempo real. | Alta | Cubierto por el seguimiento (SS-04); depende de que el dispositivo del chofer informe su posición. |
| OBJ-04 | I | Garantizar trazabilidad de entregas | Registrar evidencia objetiva (foto opcional, marcas de tiempo de cada cambio de estado, GPS) de cada entrega para resolver reclamos de forma objetiva y sin disputa. | Alta | Cubierto en parte: la foto de la entrega es opcional. Lo completa el registro de auditoría (NFR-10). |
| OBJ-05 | I | Centralizar el control operativo | Brindar al administrador una herramienta única (Panel Web) para gestionar choferes, vehículos, productos, stock, precios, franjas horarias, reclamos y visualizar reportes en tiempo real. | Alta | Cubierto por el panel web, ampliado con compras, personal, caja y cuentas corrientes (SS-19 a SS-21). |
| OBJ-06 | C, A | Sincronizar el inventario en tiempo real | Reservar automáticamente el stock al confirmar un pedido en una única operación indivisible y restituirlo automáticamente si el pedido se cancela, evitando ventas sin producto disponible. | Alta | Cubierto por la reserva de stock al confirmar el pedido y ampliado con el stock físico por depósito (SS-08). |
| OBJ-07 | I | Habilitar múltiples métodos de pago | Permitir al cliente pagar con efectivo, MercadoPago o transferencia bancaria, con aplicación automática, en el servidor, del recargo del 10 % cuando el pago es en línea (MercadoPago o transferencia). | Alta | Cubierto: efectivo, MercadoPago y transferencia (SS-14); el recargo lo aplica el sistema. |
| OBJ-08 | I | Gestionar franjas horarias de entrega | Permitir al administrador configurar rangos horarios de entrega con capacidad máxima diaria para distribuir la carga de trabajo de los choferes de forma ordenada. | Media | Cubierto por las franjas horarias y su disponibilidad (SS-09). |
| OBJ-09 | C | Operar varias distribuidoras sobre una misma instancia | Atender desde un único sistema a varias empresas comercializadoras manteniendo los datos de cada una aislados de los del resto, de modo que toda operación de gestión quede acotada a la distribuidora del usuario que la invoca. | Alta | Cubierto; el aislamiento entre distribuidoras es el requisito NFR-09. |
| OBJ-10 | I | Delimitar el área de reparto | Permitir que cada distribuidora defina las zonas dentro de las cuales acepta pedidos, con el recargo que corresponde a cada una, y verificar que el domicilio de entrega caiga dentro de alguna de ellas antes de tomar el pedido. | Alta | Cubierto por las zonas de cobertura (SS-11). |
| OBJ-11 | I | Registrar los contratiempos del reparto | Dejar asentado el inconveniente ocurrido durante la entrega —cliente ausente, faltante de stock, producto dañado u otro— con su descripción y su evidencia fotográfica, y llevarlo hasta la resolución del administrador. | Alta | Cubierto por las incidencias de la entrega (SS-12). |
| OBJ-12 | I | Medir la calidad del servicio | Permitir que el cliente y el chofer se califiquen mutuamente una vez entregado el pedido, con una sola calificación por pedido y por lado, y sostener con esas valoraciones el promedio que exhibe el perfil del chofer. | Alta | Cubierto por las calificaciones entre cliente y chofer (SS-12). |
| OBJ-13 | I | Rastrear el envase físico | Seguir cada botellón por su número de serie a lo largo de todo su ciclo —depósito, carga, despacho, poder del cliente y devolución vacío—, dejando asentado cada cambio de estado con el pedido y el responsable que lo produjo. | Alta | Cubierto por la trazabilidad de envases (SS-13). |
| OBJ-14 | I | Habilitar reservas programadas con seña | Permitir al cliente apartar garrafas para una fecha futura dejando una seña en garantía, con el stock descontado desde el momento de la reserva y con la activación del pedido y la expiración de la reserva impaga resueltas por procesos automáticos. | Alta | Cubierto por las reservas programadas con seña (SS-15). |
| OBJ-15 | I | Verificar el estado operativo del sistema | Informar el estado del backend y de las dependencias de las que depende —base de datos, cache, memoria y disco— y permitir probar los canales de aviso, para que el orquestador decida a qué instancia enviar tráfico y el administrador confirme que la mensajería funciona. | Media | Cubierto por la observabilidad (SS-18); lo consulta la plataforma de despliegue. |

---
## 3. Diagrama de Casos de Uso del Sistema

El diagrama de casos de uso del sistema se presenta por subsistemas, en notación UML: los 21
subsistemas dibujados como paquetes dentro del límite del sistema y los actores fuera de él, cada uno
unido a los subsistemas en los que participa; el Administrador General especializa al Administrador.
La sección 3.1 delimita el sistema con el diagrama de contexto, la sección 4 enumera todos los casos
de uso con su importancia y el diagrama de casos de uso de cada subsistema está en la sección 8.1.

**Figura 1 — Diagrama de casos de uso del sistema por subsistemas**

![Diagrama de casos de uso del sistema por subsistemas](../diagramas/uml/CU_Sistema_Diagrama-De-Subsistemas.png)

### 3.1 Fronteras del Sistema

El rectángulo del diagrama es el **límite del sistema**: lo que queda adentro es
responsabilidad de SPLG y lo que queda afuera no. Los actores se dibujan fuera de ese
límite porque interactúan con el sistema sin formar parte de él.

![Diagrama de contexto del sistema](../diagramas/uml/CU_Sistema_Diagrama-De-Contexto.png)

**Figura 2 — Diagrama de contexto del sistema**

**Queda dentro del límite**

| Pieza | Qué resuelve |
|---|---|
| App Cliente | El pedido, el seguimiento y el reclamo, desde el teléfono del cliente |
| App Chofer | La aceptación del pedido, la posición en el mapa y la confirmación de entrega |
| Panel de administración | La gestión de la distribuidora: catálogo, flota, franjas, reportes |
| Backend | Las reglas del negocio, la base de datos y los procesos programados |
| Procesos automáticos | El despacho por proximidad, las reservas y los avisos, sin intervención humana |

Los 21 subsistemas de la sección 5 son la división interna de ese límite.

**Queda fuera del límite**

| Fuera | Por qué |
|---|---|
| Firebase | Servicio de terceros: valida la identidad y entrega los avisos al dispositivo |
| MercadoPago | Servicio de terceros: procesa el cobro y avisa el resultado por webhook |
| Servicio de correo | Servicio de terceros: envía los correos del sistema (bienvenida al cliente, recuperación de contraseña, prueba del servicio y avisos de vencimientos, de stock bajo, de rendiciones sin cerrar y de multas por vencer) |
| Plataforma de despliegue (ACT-09) | Sistema externo que sondea el estado del backend para decidir si le envía tráfico o si reinicia la instancia; inicia CU-104 |
| Operador Técnico (ACT-10) | Persona con acceso al servidor: pone en marcha el sistema y crea la cuenta inicial (CU-087); no usa el panel ni las aplicaciones |
| El traslado físico de la garrafa | Lo hace el chofer; el sistema lo registra, no lo ejecuta |
| La facturación fiscal | No está en el alcance de esta fase |
| La contabilidad de la distribuidora | Sistema aparte, sin integración prevista |

El sistema **no decide** por el chofer ni por el cliente: propone, registra y avisa. Toda
acción sobre el mundo físico queda del lado de las personas.

## 4. Casos de Uso: lista e importancia

*Lista de casos de usos y su importancia dentro del sistema para determinar cuáles son los casos de usos de incluir en cada una de las iteraciones*

La tabla enumera todos los casos de uso identificados, con su subsistema, su actor principal, su
importancia y su estado en el sistema construido. La importancia sigue la leyenda de prioridad de este
documento: **Crítico** (el sistema no puede operar sin el caso), **Importante** (aporta valor
significativo), **Secundario** (deseable) y **Menor** (comodidad puntual); el criterio es el efecto de
cada caso sobre la operación diaria de la distribuidora. La importancia es la que decide qué casos se
abordan en cada iteración: la columna «Expandido» marca los 21 casos de uso esenciales que esta
iteración especifica con su caso de uso expandido (sección 8.3). Los demás quedan con su descripción de
alto nivel (Documento 0) y su lugar en el diagrama de su subsistema (sección 8.1).

| Importancia | Casos de uso vigentes |
|:---:|:---:|
| Crítico | 63 |
| Importante | 209 |
| Secundario | 54 |
| Menor | 2 |
| **Total** | **328** |

Diez casos fueron retirados del catálogo por no ser procesos de negocio elementales; la tabla de
retirados, con el motivo y el reemplazo de cada uno, está en el Documento 0. Además, diez casos quedan
retirados del alcance porque el chofer cobra un sueldo mensual y no gana comisiones por entrega: las
ganancias del chofer (CU-049) y las comisiones con su liquidación (CU-240 a CU-244, CU-333 a CU-335 y
CU-347). Figuran en la lista con ese motivo y no se cuentan entre los vigentes.

| Caso de Uso | Subsistema | Actor principal | Importancia | Estado | Expandido |
|-------------|:----------:|-----------------|:-----------:|--------|:---------:|
| CU-001 Iniciar Sesión | SS-01 | Cliente, Chofer, Administrador | Crítico | Implementado | Sí |
| CU-002 Registrarse como Cliente | SS-01 | Cliente | Crítico | Implementado | Sí |
| CU-004 Consultar el Perfil de Usuario | SS-01 | Cliente, Chofer | Importante | Implementado |  |
| CU-005 Crear un Pedido | SS-02 | Cliente, Administrador | Crítico | Implementado | Sí |
| CU-006 Consultar el Detalle de un Pedido | SS-02 | Cliente, Chofer, Administrador | Crítico | Implementado |  |
| CU-007 Consultar el Historial de Pedidos | SS-02 | Cliente | Importante | Implementado |  |
| CU-008 Cancelar un Pedido (Cliente) | SS-02 | Cliente | Importante | Implementado | Sí |
| CU-009 Liberar un Pedido (Chofer) | SS-02 | Chofer | Importante | Implementado |  |
| CU-010 Cancelar un Pedido (Administrador) | SS-02 | Administrador | Importante | Implementado |  |
| CU-011 Consultar Todos los Pedidos | SS-02 | Administrador | Importante | Implementado |  |
| CU-012 Asignar un Chofer Manualmente | SS-03 | Administrador | Secundario | Implementado |  |
| CU-013 Asignar un Pedido Automáticamente por Proximidad | SS-03 | Sistema Automático | Crítico | Implementado, con funcionalidad planificada | Sí |
| CU-014 Vencer la Oferta y Ofrecer al Siguiente Chofer | SS-03 | Sistema Automático | Crítico | Implementado | Sí |
| CU-015 Aceptar un Pedido | SS-03 | Chofer | Crítico | Implementado | Sí |
| CU-016 Rechazar un Pedido Ofrecido | SS-03 | Chofer | Importante | Implementado |  |
| CU-017 Modificar la Ubicación GPS del Chofer | SS-04 | Chofer | Crítico | Implementado, con funcionalidad planificada (C-10) | Sí |
| CU-018 Marcar un Pedido "En Camino" | SS-04 | Chofer | Crítico | Implementado |  |
| CU-019 Avisar la Llegada al Cliente | SS-04 | Chofer | Importante | Implementado |  |
| CU-020 Confirmar una Entrega Manualmente | SS-04 | Administrador, Administrador General | Crítico | Implementado |  |
| CU-022 Activar la Disponibilidad | SS-04 | Chofer | Crítico | Implementado | Sí |
| CU-023 Registrar un Reclamo | SS-05 | Cliente | Importante | Implementado | Sí |
| CU-024 Consultar los Reclamos | SS-05 | Administrador | Importante | Implementado |  |
| CU-025 Resolver un Reclamo | SS-05 | Administrador | Importante | Implementado | Sí |
| CU-026 Consultar el Tablero General | SS-06 | Administrador | Importante | Implementado |  |
| CU-027 Consultar el Reporte de Ventas por Chofer | SS-06 | Administrador | Importante | Implementado |  |
| CU-028 Consultar el Reporte de Ventas por Producto | SS-06 | Administrador | Importante | Implementado |  |
| CU-029 Consultar el Reporte por Método de Pago | SS-06 | Administrador | Secundario | Implementado |  |
| CU-030 Consultar el Gráfico de Ventas (últimos 7 días) | SS-06 | Administrador | Secundario | Implementado |  |
| CU-031 Registrar un Chofer (Gestión de la Flota) | SS-07 | Administrador | Crítico | Implementado |  |
| CU-032 Validar un Chofer | SS-07 | Administrador | Crítico | Implementado |  |
| CU-033 Activar un Chofer | SS-07 | Administrador | Importante | Implementado |  |
| CU-034 Registrar un Vehículo del Chofer | SS-07 | Administrador | Importante | Implementado |  |
| CU-035 Consultar el Listado de Choferes | SS-07 | Administrador | Importante | Implementado |  |
| CU-036 Crear un Producto (Garrafa) | SS-08 | Administrador | Crítico | Implementado |  |
| CU-037 Modificar el Precio de un Producto | SS-08 | Administrador | Crítico | Implementado |  |
| CU-038 Modificar el Stock de un Producto | SS-08 | Administrador | Crítico | Implementado |  |
| CU-039 Configurar las Promociones por Cantidad | SS-08 | Administrador | Importante | Implementado |  |
| CU-040 Desactivar un Producto | SS-08 | Administrador | Importante | Implementado |  |
| CU-041 Consultar el Catálogo de Productos (Cliente) | SS-08 | Cliente | Crítico | Implementado |  |
| CU-042 Crear una Franja Horaria | SS-09 | Administrador | Importante | Implementado |  |
| CU-043 Modificar una Franja Horaria | SS-09 | Administrador | Importante | Implementado |  |
| CU-044 Seleccionar una Franja Horaria al Crear un Pedido | SS-09 | Cliente | Importante | Implementado |  |
| CU-045 Consultar las Franjas Horarias Disponibles | SS-09 | Cliente | Importante | Implementado |  |
| CU-046 Consultar las Direcciones de Entrega del Cliente | SS-02 | Cliente | Importante | Implementado |  |
| CU-047 Recuperar la Contraseña | SS-01 | Cliente, Chofer, Administrador | Importante | Implementado |  |
| CU-048 Procesar el Pago con MercadoPago | SS-14 | MercadoPago | Crítico | Implementado | Sí |
| CU-049 Consultar las Ganancias del Chofer | SS-07 | Chofer, Administrador | Importante | Retirado del alcance: el chofer cobra un sueldo mensual |  |
| CU-050 Bloquear un Usuario | SS-01 | Administrador, Administrador General | Secundario | Implementado |  |
| CU-051 Consultar el Listado de Vehículos | SS-07 | Administrador | Importante | Implementado |  |
| CU-052 Registrar una Distribuidora | SS-10 | Administrador General | Crítico | Implementado |  |
| CU-053 Consultar las Distribuidoras | SS-10 | Administrador General | Crítico | Implementado |  |
| CU-054 Modificar los Datos de una Distribuidora | SS-10 | Administrador General | Crítico | Implementado |  |
| CU-055 Dar de Baja una Distribuidora | SS-10 | Administrador General | Importante | Implementado |  |
| CU-056 Crear un Polígono de Cobertura | SS-11 | Administrador, Administrador General | Importante | Implementado |  |
| CU-057 Consultar los Polígonos de Cobertura | SS-11 | Administrador, Administrador General | Secundario | Implementado |  |
| CU-058 Validar la Cobertura de una Dirección | SS-11 | Cliente, Administrador, Administrador General | Crítico | Implementado |  |
| CU-059 Dar de Baja un Polígono de Cobertura | SS-11 | Administrador, Administrador General | Secundario | Implementado |  |
| CU-060 Registrar una Incidencia de Entrega | SS-12 | Chofer, Administrador, Administrador General | Crítico | Implementado |  |
| CU-061 Consultar las Incidencias | SS-12 | Administrador, Administrador General | Importante | Implementado |  |
| CU-062 Consultar las Incidencias de un Pedido | SS-12 | Chofer, Administrador, Administrador General | Secundario | Implementado |  |
| CU-063 Resolver una Incidencia | SS-12 | Administrador, Administrador General | Importante | Implementado |  |
| CU-064 Calificar un Pedido (cliente↔chofer) | SS-12 | Cliente, Chofer | Crítico | Implementado |  |
| CU-065 Consultar el Promedio de Calificaciones de un Usuario | SS-12 | Cliente, Chofer, Administrador, Administrador General | Secundario | Implementado |  |
| CU-066 Consultar el Historial de Calificaciones Recibidas | SS-12 | Administrador, Administrador General | Secundario | Implementado |  |
| CU-067 Dar de Alta un Envase Físico | SS-13 | Administrador, Administrador General | Importante | Implementado |  |
| CU-068 Asignar los Envases a un Pedido | SS-13 | Chofer, Administrador, Administrador General | Crítico | Implementado |  |
| CU-069 Consultar el Parque de Envases | SS-13 | Administrador, Administrador General | Importante | Implementado |  |
| CU-070 Registrar un Movimiento de Envase (cambio de estado) | SS-13 | Chofer, Administrador, Administrador General | Crítico | Implementado |  |
| CU-071 Consultar el Historial de Movimientos de un Envase | SS-13 | Administrador, Administrador General | Importante | Implementado |  |
| CU-072 Crear una Reserva Programada con Seña | SS-15 | Cliente, Chofer, Administrador | Crítico | Implementado |  |
| CU-073 Consultar las Reservas y el Estado de la Seña | SS-15 | Administrador, Administrador General | Importante | Implementado |  |
| CU-074 Confirmar la Seña Cobrada en Efectivo | SS-15 | Administrador, Administrador General | Crítico | Implementado |  |
| CU-075 Activar las Reservas Vencidas Automáticamente | SS-15 | Sistema Automático | Crítico | Implementado |  |
| CU-076 Expirar las Reservas sin Seña Pagada | SS-15 | Sistema Automático | Importante | Implementado |  |
| CU-077 Expirar los Pedidos de MercadoPago sin Pagar | SS-15 | Sistema Automático | Importante | Implementado |  |
| CU-078 Consultar el Código de Entrega (QR del chofer) | SS-04 | Chofer, Administrador, Administrador General | Crítico | Implementado | Sí |
| CU-079 Confirmar una Entrega Escaneando el QR (cliente) | SS-04 | Cliente, Administrador, Administrador General | Crítico | Implementado | Sí |
| CU-080 Consultar el Pool de Pedidos Disponibles | SS-02 | Chofer, Administrador, Administrador General | Crítico | Implementado |  |
| CU-081 Consultar los Pedidos Asignados al Chofer | SS-02 | Chofer, Administrador, Administrador General | Crítico | Implementado |  |
| CU-082 Crear un Usuario Base | SS-01 | — | Importante | Implementado |  |
| CU-083 Consultar los Usuarios | SS-01 | Administrador | Importante | Implementado |  |
| CU-085 Dar de Baja un Usuario | SS-01 | Administrador, Administrador General | Importante | Implementado |  |
| CU-086 Registrar un Administrador | SS-16 | Administrador, Administrador General | Importante | Implementado |  |
| CU-087 Crear el Primer Administrador General | SS-16 | Operador Técnico | Importante | Implementado |  |
| CU-088 Consultar los Administradores | SS-16 | Administrador | Secundario | Implementado |  |
| CU-089 Consultar los Roles | SS-16 | Administrador General | Importante | Implementado |  |
| CU-092 Consultar el Listado de Clientes | SS-16 | Administrador | Importante | Implementado |  |
| CU-094 Modificar la Ubicación del Cliente | SS-16 | Cliente, Administrador | Secundario | Implementado |  |
| CU-095 Dar de Baja un Cliente | SS-16 | Administrador General | Importante | Implementado |  |
| CU-096 Modificar el Perfil del Chofer | SS-07 | Administrador | Importante | Implementado |  |
| CU-097 Dar de Baja un Chofer | SS-07 | Administrador | Importante | Implementado |  |
| CU-100 Enviar una Notificación de Prueba | SS-17 | Administrador General | Secundario | Implementado |  |
| CU-101 Reenviar la Notificación de Confirmación de Pedido | SS-17 | Administrador General | Secundario | Implementado |  |
| CU-102 Probar el Servicio de Correo | SS-17 | Administrador General | Secundario | Implementado |  |
| CU-104 Verificar la Salud del Sistema (vida y disponibilidad) | SS-18 | Plataforma de despliegue | Importante | Implementado |  |
| CU-105 Planificar el Mantenimiento y las Habilitaciones de la Flota | SS-07 | Chofer, Administrador, Sistema Automático | Importante | Implementado | Sí |
| CU-106 Anticipar la Recompra por Consumo Estimado | SS-02 | Cliente, Sistema Automático | Importante | Implementado en el sistema y el panel; en curso en la aplicación del cliente | Sí |
| CU-107 Agrupar Pedidos por Recorrido | SS-03 | Chofer, Sistema Automático | Importante | Implementado en el sistema y el panel; en curso en la aplicación del chofer | Sí |
| CU-108 Recuperar Envases No Devueltos | SS-13 | Cliente, Administrador, Sistema Automático | Importante | Implementado en el sistema y el panel; en curso en las aplicaciones | Sí |
| CU-109 Consultar el Detalle del Chofer | SS-07 | Administrador | Importante | Implementado |  |
| CU-110 Buscar un Chofer por Usuario | SS-07 | Administrador | Importante | Implementado |  |
| CU-111 Modificar un Vehículo | SS-07 | Administrador | Importante | Implementado |  |
| CU-112 Dar de Baja un Vehículo | SS-07 | Administrador | Importante | Implementado |  |
| CU-113 Consultar el Detalle del Vehículo | SS-07 | Administrador | Importante | Implementado |  |
| CU-114 Buscar un Vehículo por Patente | SS-07 | Administrador | Importante | Implementado |  |
| CU-115 Consultar los Vehículos de un Chofer | SS-07 | Administrador, Chofer | Importante | Implementado |  |
| CU-116 Registrar una Dirección de Entrega | SS-02 | Cliente | Importante | Implementado, con funcionalidad planificada (C-10) |  |
| CU-117 Consultar Detalle de una Dirección de Entrega | SS-02 | Cliente | Importante | Implementado |  |
| CU-118 Modificar una Dirección de Entrega | SS-02 | Cliente | Importante | Implementado, con funcionalidad planificada (C-10) |  |
| CU-119 Dar de Baja una Dirección de Entrega | SS-02 | Cliente | Importante | Implementado |  |
| CU-120 Marcar una Dirección como Predeterminada | SS-02 | Cliente | Importante | Implementado |  |
| CU-121 Consultar la Dirección Predeterminada | SS-02 | Cliente | Importante | Implementado |  |
| CU-122 Agregar un Ítem al Carrito | SS-02 | Cliente | Importante | Implementado |  |
| CU-123 Modificar la Cantidad de un Ítem del Carrito | SS-02 | Cliente | Importante | Implementado |  |
| CU-124 Quitar un Ítem del Carrito | SS-02 | Cliente | Importante | Implementado |  |
| CU-125 Consultar el Carrito | SS-02 | Cliente | Importante | Implementado |  |
| CU-126 Vaciar el Carrito | SS-02 | Cliente | Menor | Implementado |  |
| CU-127 Cambiar la Dirección de Entrega del Pedido | SS-02 | Cliente | Importante | Implementado |  |
| CU-128 Indicar Quién Recibe el Pedido | SS-02 | Cliente | Importante | Implementado |  |
| CU-129 Consultar el Detalle del Cliente | SS-16 | Administrador | Importante | Implementado |  |
| CU-130 Buscar un Cliente por Usuario | SS-16 | Administrador | Importante | Implementado |  |
| CU-131 Modificar los Datos del Cliente | SS-16 | Administrador General | Importante | Implementado |  |
| CU-132 Registrar la Revisión Periódica de un Envase | SS-13 | Administrador | Crítico | Implementado |  |
| CU-133 Consultar la Vigencia de un Envase | SS-13 | Administrador | Importante | Implementado |  |
| CU-134 Consultar los Envases Próximos a Vencer | SS-13 | Administrador | Importante | Implementado |  |
| CU-135 Bloquear el Despacho de un Envase Vencido | SS-13 | Sistema Automático | Crítico | Implementado |  |
| CU-136 Registrar el Seguro del Vehículo | SS-07 | Administrador | Crítico | Implementado |  |
| CU-137 Registrar la Verificación Técnica Vehicular | SS-07 | Administrador | Crítico | Implementado |  |
| CU-138 Registrar la Licencia de Conducir del Chofer | SS-07 | Administrador | Crítico | Implementado |  |
| CU-139 Consultar los Vencimientos de la Flota | SS-07 | Administrador | Importante | Implementado |  |
| CU-140 Programar un Mantenimiento de Vehículo | SS-07 | Administrador | Importante | Implementado |  |
| CU-141 Registrar un Mantenimiento Realizado | SS-07 | Administrador | Importante | Implementado |  |
| CU-142 Avisar los Vencimientos Próximos de la Flota | SS-07 | Sistema Automático | Importante | Implementado |  |
| CU-143 Declarar el Consumo Promedio al Registrarse | SS-02 | Cliente | Importante | Implementado |  |
| CU-144 Modificar el Consumo Promedio Declarado | SS-02 | Cliente | Importante | Implementado |  |
| CU-145 Configurar los Días de Aviso Previo a la Recompra | SS-02 | Cliente | Menor | Implementado en el sistema; en curso en la aplicación del cliente |  |
| CU-146 Consultar la Fecha Estimada de Recompra | SS-02 | Administrador | Importante | Implementado |  |
| CU-147 Realizar una Compra Express | SS-02 | Cliente | Crítico | Implementado |  |
| CU-148 Elegir la Modalidad de Entrega del Pedido | SS-02 | Cliente | Importante | Implementado |  |
| CU-149 Despachar un Pedido Express a un Chofer en Moto | SS-03 | Sistema Automático | Crítico | Implementado |  |
| CU-150 Programar la Vigencia de un Polígono de Cobertura | SS-11 | Administrador, Administrador General | Importante | Implementado |  |
| CU-151 Desactivar los Polígonos de Cobertura Vencidos | SS-11 | Sistema Automático | Importante | Implementado |  |
| CU-152 Consultar el Registro de Auditoría | SS-18 | Administrador, Administrador General | Importante | Implementado | Sí |
| CU-154 Consultar el Listado de Franjas Horarias | SS-09 | Administrador, Administrador General | Importante | Implementado |  |
| CU-155 Adjuntar un Archivo a una Tarea de Flota | SS-07 | Administrador | Importante | Implementado |  |
| CU-156 Consultar los Adjuntos de una Tarea de Flota | SS-07 | Administrador | Secundario | Implementado |  |
| CU-157 Descargar un Adjunto de Flota | SS-07 | Administrador | Secundario | Implementado |  |
| CU-158 Eliminar un Adjunto de Flota | SS-07 | Administrador | Secundario | Implementado |  |
| CU-159 Almacenar un Archivo | SS-07 | — | Importante | Implementado |  |
| CU-160 Recuperar un Archivo | SS-07 | — | Secundario | Implementado |  |
| CU-161 Poner un Vehículo en Uso para un Chofer | SS-07 | Administrador, Administrador General | Importante | Implementado |  |
| CU-162 Liberar el Vehículo en Uso de un Chofer | SS-07 | Administrador, Administrador General | Secundario | Implementado |  |
| CU-163 Consultar el Vehículo en Uso de un Chofer | SS-07 | Administrador, Administrador General, Chofer | Secundario | Implementado |  |
| CU-164 Consultar el Historial de Vehículos de un Chofer | SS-07 | Administrador, Administrador General | Secundario | Implementado |  |
| CU-165 Consultar el Historial de Choferes de un Vehículo | SS-07 | Administrador, Administrador General | Secundario | Implementado |  |
| CU-166 Tomar un Reclamo Pendiente | SS-05 | Administrador, Administrador General | Importante | Implementado |  |
| CU-167 Reabrir un Reclamo | SS-05 | Administrador, Administrador General | Importante | Implementado |  |
| CU-168 Reintegrar el Pago de un Pedido | SS-14 | Sistema Automático, Administrador | Importante | Implementado |  |
| CU-169 Registrar el Cambio de Estado de un Pedido | SS-02 | — | Importante | Implementado |  |
| CU-170 Consultar el Historial de Estados de un Pedido | SS-02 | Cliente, Chofer, Administrador, Administrador General | Secundario | Implementado |  |
| CU-171 Configurar los Parámetros de Despacho de la Distribuidora | SS-03 | Administrador, Administrador General | Crítico | Implementado |  |
| CU-172 Configurar los Parámetros de un Proceso Automático | SS-18 | Administrador, Administrador General | Importante | Implementado |  |
| CU-173 Configurar la Frecuencia de las Tareas Programadas | SS-18 | Administrador, Administrador General | Importante | Implementado |  |
| CU-174 Adjuntar la Fotografía de un Reclamo | SS-05 | Cliente, Administrador, Administrador General | Importante | Implementado |  |
| CU-175 Consultar la Fotografía de un Reclamo | SS-05 | Cliente, Administrador, Administrador General | Secundario | Implementado |  |
| CU-176 Consultar los Puestos de Trabajo | SS-19 | Administrador | Importante | Implementado |  |
| CU-177 Registrar el Legajo de un Empleado | SS-19 | Administrador | Crítico | Implementado |  |
| CU-178 Modificar el Legajo de un Empleado | SS-19 | Administrador | Importante | Implementado |  |
| CU-179 Consultar el Legajo de un Empleado | SS-19 | Administrador, Administrador General | Importante | Implementado |  |
| CU-180 Consultar el Listado de Empleados | SS-19 | Administrador, Administrador General | Importante | Implementado, con funcionalidad planificada |  |
| CU-181 Registrar el Egreso de un Empleado | SS-19 | Administrador | Crítico | Implementado |  |
| CU-182 Otorgar una Cuenta de Acceso a un Empleado | SS-19 | Administrador | Importante | Implementado |  |
| CU-183 Registrar el Curso de Transporte de Mercancías Peligrosas del Empleado | SS-19 | Administrador | Crítico | Implementado |  |
| CU-184 Registrar el Examen Psicofísico del Empleado | SS-19 | Administrador | Crítico | Implementado |  |
| CU-185 Registrar el Alta en la ART del Empleado | SS-19 | Administrador | Importante | Implementado |  |
| CU-186 Adjuntar un Archivo al Legajo | SS-19 | Administrador | Secundario | Implementado |  |
| CU-187 Consultar los Vencimientos del Personal | SS-19 | Administrador | Importante | Implementado |  |
| CU-188 Avisar los Vencimientos Próximos del Personal | SS-19 | Sistema Automático | Importante | Implementado |  |
| CU-189 Registrar la Asistencia de un Empleado | SS-19 | Administrador | Importante | Implementado |  |
| CU-190 Registrar el Inicio de la Jornada | SS-19 | Chofer | Secundario | Implementado |  |
| CU-191 Registrar una Licencia o Ausencia | SS-19 | Administrador | Importante | Implementado |  |
| CU-192 Aprobar una Solicitud de Licencia | SS-19 | Administrador | Importante | Implementado |  |
| CU-193 Consultar el Saldo de Vacaciones de un Empleado | SS-19 | Administrador | Secundario | Implementado |  |
| CU-194 Consultar el Tablero de Personal | SS-19 | Administrador | Secundario | Implementado |  |
| CU-195 Registrar una Carga de Combustible | SS-07 | Administrador, Chofer | Importante | Implementado |  |
| CU-196 Consultar el Consumo de Combustible de un Vehículo | SS-07 | Administrador | Importante | Implementado |  |
| CU-197 Registrar la Habilitación para Transportar Mercancías Peligrosas | SS-07 | Administrador | Crítico | Implementado |  |
| CU-198 Registrar una Multa de Tránsito | SS-07 | Administrador | Importante | Implementado |  |
| CU-199 Registrar el Pago de una Multa | SS-07 | Administrador | Secundario | Implementado |  |
| CU-200 Imputar una Multa al Chofer | SS-07 | Administrador | Secundario | Implementado |  |
| CU-201 Registrar un Siniestro | SS-07 | Administrador, Chofer | Importante | Implementado |  |
| CU-202 Cerrar un Siniestro | SS-07 | Administrador | Secundario | Implementado |  |
| CU-203 Consultar el Costo Total de un Vehículo | SS-07 | Administrador | Importante | Implementado |  |
| CU-204 Consultar el Tablero de Costos de la Flota | SS-07 | Administrador | Importante | Implementado |  |
| CU-205 Registrar un Neumático | SS-07 | Administrador | Secundario | Implementado |  |
| CU-206 Registrar un Movimiento de Neumático | SS-07 | Administrador | Secundario | Implementado |  |
| CU-207 Consultar los Depósitos | SS-08 | Administrador | Importante | Implementado |  |
| CU-208 Consultar el Stock por Ubicación | SS-08 | Administrador | Crítico | Implementado |  |
| CU-209 Consultar los Movimientos de Stock | SS-08 | Administrador | Importante | Implementado |  |
| CU-210 Configurar el Stock Mínimo | SS-08 | Administrador | Secundario | Implementado |  |
| CU-211 Avisar el Stock Bajo | SS-08 | Sistema Automático | Importante | Implementado |  |
| CU-212 Transferir Stock entre Depósitos | SS-08 | Administrador | Secundario | Implementado |  |
| CU-213 Registrar un Ajuste o una Merma de Stock | SS-08 | Administrador | Importante | Implementado |  |
| CU-214 Consultar los Proveedores | SS-20 | Administrador | Importante | Implementado |  |
| CU-215 Emitir una Orden de Compra | SS-20 | Administrador | Importante | Implementado |  |
| CU-216 Cancelar una Orden de Compra | SS-20 | Administrador | Secundario | Implementado |  |
| CU-217 Registrar la Recepción de una Compra | SS-20 | Administrador | Crítico | Implementado |  |
| CU-218 Registrar la Carga del Camión | SS-08 | Administrador | Crítico | Implementado |  |
| CU-219 Registrar la Salida del Camión | SS-08 | Chofer, Administrador | Importante | Implementado |  |
| CU-220 Descontar del Stock Físico lo Entregado | SS-08 | — | Crítico | Implementado |  |
| CU-221 Registrar el Regreso del Camión | SS-08 | Chofer, Administrador | Importante | Implementado |  |
| CU-222 Cerrar la Rendición de Stock del Camión | SS-08 | Administrador | Crítico | Implementado |  |
| CU-223 Consultar la Carga Actual del Camión | SS-08 | Chofer | Secundario | Implementado |  |
| CU-224 Conciliar el Stock Vendible con el Físico | SS-08 | Administrador, Sistema Automático | Importante | Implementado |  |
| CU-225 Crear una Caja | SS-21 | Administrador | Importante | Implementado |  |
| CU-226 Abrir la Caja | SS-21 | Administrador | Importante | Implementado |  |
| CU-227 Cerrar la Caja con Arqueo | SS-21 | Administrador | Crítico | Implementado |  |
| CU-228 Registrar una Entrada de Dinero en la Caja | SS-21 | Administrador | Crítico | Implementado |  |
| CU-229 Anular un Movimiento de Caja | SS-21 | Administrador | Importante | Implementado |  |
| CU-230 Crear una Categoría de Ingresos y Gastos | SS-21 | Administrador | Secundario | Implementado |  |
| CU-231 Generar la Rendición Diaria del Chofer | SS-21 | Sistema Automático | Importante | Implementado |  |
| CU-232 Declarar el Efectivo Rendido | SS-21 | Chofer, Administrador | Crítico | Implementado |  |
| CU-233 Aprobar la Rendición del Chofer | SS-21 | Administrador | Crítico | Implementado |  |
| CU-234 Avisar las Rendiciones sin Cerrar | SS-21 | Sistema Automático | Importante | Implementado |  |
| CU-235 Habilitar la Cuenta Corriente de un Cliente | SS-21 | Administrador | Importante | Implementado |  |
| CU-236 Vender a Cuenta Corriente | SS-21 | Administrador | Crítico | Implementado |  |
| CU-237 Registrar un Pago de Cuenta Corriente | SS-21 | Administrador, Chofer | Crítico | Implementado |  |
| CU-238 Consultar el Estado de Cuenta de un Cliente | SS-21 | Administrador | Importante | Implementado |  |
| CU-239 Consultar la Antigüedad de la Deuda | SS-21 | Administrador | Secundario | Implementado |  |
| CU-240 Crear una Regla de Comisión por Entrega | SS-21 | Administrador | Importante | Retirado del alcance: el chofer cobra un sueldo mensual |  |
| CU-241 Registrar la Comisión de una Entrega | SS-21 | Sistema Automático | Importante | Retirado del alcance: el chofer cobra un sueldo mensual |  |
| CU-242 Liquidar las Comisiones de un Chofer | SS-21 | Administrador | Importante | Retirado del alcance: el chofer cobra un sueldo mensual |  |
| CU-243 Registrar el Pago de una Liquidación | SS-21 | Administrador | Importante | Retirado del alcance: el chofer cobra un sueldo mensual |  |
| CU-244 Consultar Mis Comisiones | SS-21 | Chofer | Secundario | Retirado del alcance: el chofer cobra un sueldo mensual |  |
| CU-245 Consultar el Tablero Financiero | SS-21 | Administrador | Importante | Implementado |  |
| CU-246 Verificar la Habilitación Laboral del Chofer | SS-19 | — | Importante | Implementado |  |
| CU-247 Reactivar un Vehículo | SS-07 | Administrador | Importante | Implementado |  |
| CU-248 Verificar la Carga de Camión Abierta del Chofer | SS-08 | — | Importante | Implementado |  |
| CU-249 Configurar el Control de Carga de Camión Abierta | SS-08 | Administrador | Secundario | Implementado |  |
| CU-250 Aplicar un Movimiento de Stock | SS-08 | — | Crítico | Implementado |  |
| CU-251 Modificar el Perfil de Usuario | SS-01 | Cliente, Chofer | Importante | Implementado |  |
| CU-252 Crear un Rol | SS-16 | Administrador General | Importante | Implementado |  |
| CU-253 Modificar un Rol | SS-16 | Administrador General | Importante | Implementado |  |
| CU-254 Dar de Baja un Rol | SS-16 | Administrador General | Importante | Implementado |  |
| CU-255 Crear un Puesto de Trabajo | SS-19 | Administrador | Importante | Implementado |  |
| CU-256 Modificar un Puesto de Trabajo | SS-19 | Administrador | Importante | Implementado |  |
| CU-257 Dar de Baja un Puesto de Trabajo | SS-19 | Administrador | Importante | Implementado |  |
| CU-258 Registrar un Depósito | SS-08 | Administrador | Importante | Implementado |  |
| CU-259 Modificar un Depósito | SS-08 | Administrador | Importante | Implementado |  |
| CU-260 Dar de Baja un Depósito | SS-08 | Administrador | Importante | Implementado |  |
| CU-261 Registrar un Proveedor | SS-20 | Administrador | Importante | Implementado |  |
| CU-262 Modificar un Proveedor | SS-20 | Administrador | Importante | Implementado |  |
| CU-263 Dar de Baja un Proveedor | SS-20 | Administrador | Importante | Implementado |  |
| CU-264 Modificar una Caja | SS-21 | Administrador | Importante | Implementado |  |
| CU-265 Modificar una Categoría de Ingresos y Gastos | SS-21 | Administrador | Secundario | Implementado |  |
| CU-266 Desactivar la Disponibilidad | SS-04 | Chofer | Crítico | Implementado |  |
| CU-267 Desactivar un Chofer | SS-07 | Administrador | Importante | Implementado |  |
| CU-268 Reactivar un Producto | SS-08 | Administrador | Importante | Implementado |  |
| CU-269 Consultar los Productos Inactivos | SS-08 | Administrador | Importante | Implementado |  |
| CU-270 Desbloquear un Usuario | SS-01 | Administrador, Administrador General | Secundario | Implementado |  |
| CU-271 Invalidar un Chofer | SS-07 | Administrador | Crítico | Implementado |  |
| CU-272 Buscar un Usuario | SS-01 | Administrador | Importante | Implementado |  |
| CU-273 Marcar el Depósito Predeterminado | SS-08 | Administrador | Importante | Implementado |  |
| CU-274 Registrar el Conteo Inicial de un Depósito | SS-08 | Administrador | Importante | Implementado |  |
| CU-275 Consultar los Ajustes de Stock | SS-08 | Administrador | Importante | Implementado |  |
| CU-276 Anular una Transferencia de Stock | SS-08 | Administrador | Secundario | Implementado |  |
| CU-277 Registrar un Ajuste de Conciliación del Vendible | SS-08 | Administrador | Importante | Implementado |  |
| CU-278 Reaplicar las Entregas sin Movimiento de Stock | SS-08 | Administrador | Importante | Implementado |  |
| CU-279 Consultar el Resumen de Stock | SS-08 | Administrador | Importante | Implementado |  |
| CU-280 Anular una Recepción de Compra | SS-20 | Administrador | Importante | Implementado |  |
| CU-281 Marcar el Pago de una Recepción | SS-20 | Administrador | Secundario | Implementado |  |
| CU-282 Cerrar una Orden de Compra con Faltante | SS-20 | Administrador | Importante | Implementado |  |
| CU-283 Consultar las Órdenes de Compra | SS-20 | Administrador | Importante | Implementado |  |
| CU-284 Consultar las Recepciones de Compra | SS-20 | Administrador | Importante | Implementado |  |
| CU-285 Consultar el Costo Promedio de las Garrafas | SS-20 | Administrador | Importante | Implementado |  |
| CU-286 Consultar el Historial de Compras de un Proveedor | SS-20 | Administrador | Importante | Implementado |  |
| CU-287 Modificar una Orden de Compra | SS-20 | Administrador | Secundario | Implementado |  |
| CU-288 Enviar una Orden de Compra | SS-20 | Administrador | Importante | Implementado |  |
| CU-289 Cancelar una Carga del Camión | SS-08 | Administrador | Importante | Implementado |  |
| CU-290 Consultar las Cargas del Camión | SS-08 | Administrador | Importante | Implementado |  |
| CU-291 Consultar una Carga del Camión | SS-08 | Chofer, Administrador | Importante | Implementado |  |
| CU-292 Confirmar el Cobro en Efectivo | SS-14 | Chofer | Crítico | Implementado | Sí |
| CU-293 Informar el Cobro Impago | SS-14 | Chofer | Importante | Implementado |  |
| CU-294 Resolver un Cobro Impago | SS-14 | Administrador, Administrador General | Importante | Implementado |  |
| CU-295 Corregir los Renglones de una Carga del Camión | SS-08 | Administrador | Importante | Implementado |  |
| CU-296 Reponer una Carga del Camión | SS-08 | Administrador | Importante | Implementado |  |
| CU-297 Consultar el Stock Mínimo | SS-08 | Administrador | Secundario | Implementado |  |
| CU-298 Consultar el Control de Carga de Camión Abierta | SS-08 | Administrador | Secundario | Implementado |  |
| CU-299 Registrar el Cobro en Efectivo como Administrador | SS-14 | Administrador, Administrador General | Importante | Implementado |  |
| CU-300 Registrar el Cobro Impago como Administrador | SS-14 | Administrador, Administrador General | Importante | Implementado |  |
| CU-301 Confirmar una Transferencia | SS-14 | Administrador, Administrador General | Importante | Implementado | Sí |
| CU-302 Cotizar un Pedido | SS-02 | Cliente, Administrador, Administrador General | Importante | Implementado |  |
| CU-303 Consultar la Ruta de un Pedido | SS-04 | Cliente, Chofer | Importante | Implementado |  |
| CU-304 Consultar los Cobros Pendientes | SS-06 | Administrador, Administrador General | Secundario | Implementado |  |
| CU-305 Modificar un Polígono de Cobertura | SS-11 | Administrador, Administrador General | Importante | Implementado |  |
| CU-306 Consultar un Polígono de Cobertura | SS-11 | Administrador, Administrador General | Secundario | Implementado |  |
| CU-307 Activar un Polígono de Cobertura | SS-11 | Administrador, Administrador General | Importante | Implementado |  |
| CU-308 Desactivar un Polígono de Cobertura | SS-11 | Administrador, Administrador General | Importante | Implementado |  |
| CU-309 Registrar una Salida de Dinero de la Caja | SS-21 | Administrador | Crítico | Implementado |  |
| CU-310 Transferir Fondos entre Cajas | SS-21 | Administrador | Importante | Implementado |  |
| CU-311 Dar de Baja el Legajo de un Empleado | SS-19 | Administrador | Importante | Implementado |  |
| CU-312 Reingresar a un Empleado | SS-19 | Administrador | Importante | Implementado |  |
| CU-313 Corregir la Asistencia de un Empleado | SS-19 | Administrador | Importante | Implementado |  |
| CU-314 Consultar la Asistencia de los Empleados | SS-19 | Administrador | Importante | Implementado |  |
| CU-315 Registrar el Fin de la Jornada | SS-19 | Chofer | Secundario | Implementado |  |
| CU-316 Modificar una Licencia o Ausencia | SS-19 | Administrador | Importante | Implementado |  |
| CU-317 Cancelar una Licencia o Ausencia | SS-19 | Administrador | Importante | Implementado |  |
| CU-318 Rechazar una Solicitud de Licencia | SS-19 | Administrador | Importante | Implementado |  |
| CU-319 Consultar las Licencias | SS-19 | Administrador | Importante | Implementado |  |
| CU-320 Modificar una Carga de Combustible | SS-07 | Administrador | Importante | Implementado |  |
| CU-321 Anular una Carga de Combustible | SS-07 | Administrador | Importante | Implementado |  |
| CU-322 Consultar las Cargas de Combustible | SS-07 | Administrador | Secundario | Implementado |  |
| CU-323 Modificar una Multa de Tránsito | SS-07 | Administrador | Importante | Implementado |  |
| CU-324 Anular una Multa de Tránsito | SS-07 | Administrador | Importante | Implementado |  |
| CU-325 Consultar las Multas de Tránsito | SS-07 | Administrador | Secundario | Implementado |  |
| CU-326 Avisar las Multas por Vencer | SS-07 | Sistema Automático | Importante | Implementado |  |
| CU-327 Modificar un Siniestro | SS-07 | Administrador | Importante | Implementado |  |
| CU-328 Consultar los Siniestros | SS-07 | Administrador | Secundario | Implementado |  |
| CU-329 Registrar un Ajuste de Cuenta Corriente | SS-21 | Administrador | Importante | Implementado |  |
| CU-330 Reabrir la Rendición del Chofer | SS-21 | Administrador | Importante | Implementado |  |
| CU-331 Modificar la Cuenta Corriente de un Cliente | SS-21 | Administrador | Importante | Implementado |  |
| CU-332 Asentar el Cargo de una Venta a Cuenta Corriente | SS-21 | Sistema Automático | Crítico | Implementado |  |
| CU-333 Modificar una Regla de Comisión por Entrega | SS-21 | Administrador | Importante | Retirado del alcance: el chofer cobra un sueldo mensual |  |
| CU-334 Aprobar una Liquidación de Comisiones | SS-21 | Administrador | Importante | Retirado del alcance: el chofer cobra un sueldo mensual |  |
| CU-335 Anular una Liquidación de Comisiones | SS-21 | Administrador | Importante | Retirado del alcance: el chofer cobra un sueldo mensual |  |
| CU-336 Cambiar el Correo del Usuario | SS-01 | Cliente, Chofer, Administrador | Importante | Implementado |  |
| CU-337 Ajustar el Saldo del Chofer | SS-07 | Administrador | Importante | Implementado |  |
| CU-338 Retomar el Pedido en Curso | SS-02 | Chofer | Importante | Implementado |  |
| CU-339 Modificar un Pedido Pendiente (Administrador) | SS-02 | Administrador, Administrador General | Importante | Implementado |  |
| CU-340 Consultar los Movimientos de Caja | SS-21 | Administrador, Administrador General | Importante | Implementado |  |
| CU-341 Modificar un Pedido Pendiente (Cliente) | SS-02 | Cliente | Importante | Implementado |  |
| CU-342 Activar una Franja Horaria | SS-09 | Administrador | Importante | Implementado |  |
| CU-343 Desactivar una Franja Horaria | SS-09 | Administrador | Importante | Implementado |  |
| CU-344 Consultar el Catálogo de Productos (Administrador) | SS-08 | Administrador | Importante | Implementado |  |
| CU-345 Modificar un Administrador | SS-16 | Administrador, Administrador General | Importante | Implementado |  |
| CU-346 Dar de Baja un Administrador | SS-16 | Administrador, Administrador General | Importante | Implementado |  |
| CU-347 Anular el Pago de una Liquidación | SS-21 | Administrador | Importante | Retirado del alcance: el chofer cobra un sueldo mensual |  |
| CU-348 Consultar el Reintegro de un Pedido | SS-14 | Cliente | Secundario | Implementado |  |

---

## 5. Subsistemas del Proyecto

El sistema opera bajo un modelo **multi-distribuidora**: una única instancia atiende a
varias empresas comercializadoras manteniendo sus datos aislados entre sí. Ese
aislamiento no es un subsistema más sino una **restricción arquitectónica transversal**:
todo caso de uso de gestión queda acotado a la distribuidora del usuario que lo invoca.

### 5.1 Subsistemas de negocio

| Código | Subsistema | Descripción |
|--------|------------|-------------|
| SS-01 | Autenticación y Usuarios | Registro, ingreso y control de acceso diferenciado por rol, delegado en el proveedor de identidad: el sistema verifica en cada solicitud la identidad que certifica el proveedor y resuelve el rol contra la base de datos. |
| SS-02 | Gestión de Pedidos | Alta transaccional del pedido, ciclo de vida de sus estados y cancelación, con reserva y restitución de stock. |
| SS-03 | Despacho y Asignación | Negociación secuencial del pedido con los choferes disponibles: oferta con vigencia acotada, paso al siguiente candidato y ampliación progresiva del radio de búsqueda. |
| SS-04 | Seguimiento en Tiempo Real | Actualización de la posición del chofer y aviso de cada cambio de estado al cliente, por conexión persistente y por notificación al dispositivo. |
| SS-05 | Reclamos | Registro del reclamo posterior a la entrega por parte del cliente, y su gestión y resolución por el administrador. |
| SS-06 | Reportes y Tablero | Estadísticas operativas y análisis de ventas para el administrador. |
| SS-07 | Gestión de Choferes y Vehículos | Alta, validación y administración de los repartidores y de las unidades de la flota. Con la ampliación de flota (C-18), también las cargas de combustible, las multas, los siniestros, los neumáticos y el costo de cada unidad. |
| SS-08 | Gestión de Productos e Inventario | Tipos de garrafa comercializados, con su precio, su stock y sus promociones por volumen; y el stock físico por depósito y por camión, sus movimientos, ajustes y umbrales, y la carga y rendición del camión. |
| SS-09 | Franjas Horarias | Configuración de los rangos horarios de entrega y de su capacidad máxima diaria. |
| **SS-11** | **Cobertura Geográfica** | Definición de las áreas dentro de las cuales la distribuidora acepta pedidos, con el recargo que corresponde a cada una, y validación de cobertura de un domicilio. |
| **SS-12** | **Incidencias y Calidad de Servicio** | Registro por el chofer de los contratiempos ocurridos durante el reparto, y calificación recíproca entre cliente y chofer al cerrar el pedido. |
| **SS-13** | **Trazabilidad de Envases** | Seguimiento del botellón físico individual por su número de serie a lo largo de todo su ciclo: depósito, carga, despacho, poder del cliente y devolución. |
| **SS-14** | **Pagos y Conciliación** | Cobro a través de pasarela, registro de cada transacción y procesamiento de los avisos que la pasarela devuelve; cobro del efectivo de lo entregado por el chofer y por el administrador, impagos y confirmación de transferencias. |
| **SS-15** | **Reservas Programadas** | Pedidos concertados para una fecha futura con una seña en garantía, con su activación y su expiración automáticas. |
| SS-19 | Personal y Legajos | Legajo de cada persona que trabaja en la distribuidora, con o sin cuenta de acceso; puestos; documentación con vencimiento; asistencia y licencias. Puestos, legajos, egreso, cuenta de acceso, documentación con vencimiento, asistencia y licencias construidos (C-08). |
| **SS-20** | **Compras** | Proveedores, órdenes de compra a las plantas de llenado y recepción de lo comprado, que es lo que hace entrar garrafas llenas al stock. |
| **SS-21** | **Caja, Rendiciones y Cuentas Corrientes** | Cajas con sesión y arqueo, libro de movimientos, rendición diaria del chofer y cuentas corrientes de clientes. Construido (C-20). |

### 5.2 Subsistemas de soporte

| Código | Subsistema | Descripción |
|--------|------------|-------------|
| **SS-10** | **Multi-Distribuidora** | Alta y administración de las empresas comercializadoras, y aislamiento de los datos de cada una. Es la dimensión transversal a la que quedan acotados los subsistemas de negocio. |
| **SS-16** | **Administración de Cuentas y Roles** | Designación de administradores, definición de los roles del sistema y gestión del padrón de clientes por parte del administrador. |
| **SS-17** | **Notificaciones y Mensajería** | Registro de los dispositivos de cada usuario y envío de los avisos, tanto al dispositivo como por correo. |
| **SS-18** | **Observabilidad y Operación** | Verificación del estado de los componentes de los que depende el sistema, registro de auditoría de todo cambio de datos y configuración de los procesos automáticos y de las tareas programadas de cada distribuidora. Es el subsistema que realiza los requisitos no funcionales de disponibilidad y escalabilidad. |

> **Sobre SS-08 y SS-13.** El sistema distingue dos conceptos que el lenguaje corriente
> confunde. SS-08 administra el **producto**: el tipo de garrafa que se vende, con su
> precio y su stock agregado. SS-13 administra el **envase**: el botellón físico
> individual, identificado por su número de serie, que se entrega y se espera recuperar.
> El cliente compra un producto pero recibe un envase, y es ese envase concreto el que
> hay que rastrear.

**Figura 3 — Diagrama de Subsistemas**

![Subsistemas del proyecto](../diagramas/uml/CU_Sistema_Subsistemas.png)

> Todo subsistema de negocio opera acotado a la distribuidora del usuario que lo invoca:
> SS-10 no es un subsistema más sino la restricción que los envuelve a todos.

---

> **Documento de Requisitos del Sistema — Requisitos de la Iteración**
>
> Proyecto: SPLG – Sistema de Pedidos y Logística de Garrafas de Gas · Versión 2.0 · Fecha: 31/10/2026
>
> Realizado por: Nahuel Wagner · Realizado para: Distribuidor de Gas Envasado (Cliente Real)

---

## 6. Objetivos de la Iteración

*Se debe hacer una lista con los objetivos que se esperan alcanzar con el software a desarrollar.*

La iteración en curso, de la Fase de Construcción, persigue los objetivos que siguen. Se derivan de los
objetivos del sistema de la sección 2 y acotan qué parte de cada uno se especifica y se construye en
esta vuelta.

| Código | Objetivo | Descripción | Estabilidad | Comentarios |
|--------|----------|-------------|:-----------:|-------------|
| OBJ-I-01 | Especificar el circuito esencial del pedido | Describir con su caso de uso expandido el recorrido completo de un pedido: registro e ingreso del cliente, alta del pedido, disponibilidad del chofer, asignación automática y re-oferta, aceptación, seguimiento, entrega con código, cobro en efectivo, por transferencia o por MercadoPago, cancelación y reclamo con su resolución. | Alta | Realiza OBJ-01 a OBJ-04 y OBJ-07. Son dieciséis de los 21 casos de uso esenciales. |
| OBJ-I-02 | Incorporar los cinco módulos inteligentes | Construir los procesos automatizados que deciden por su cuenta, se parametrizan por distribuidora y nunca ejecutan sin una persona lo que compromete dinero: asignación secuencial de pedidos (M1), mantenimiento predictivo de la flota (M2), anticipación de la recompra (M3), agrupación de pedidos por recorrido (M4) y recuperación de envases no devueltos (M5). | Alta | M1 y M2 están construidos de punta a punta. M3, M4 y M5 están construidos en el sistema y en el panel de administración, apagados hasta que cada distribuidora los habilita; su etapa en las aplicaciones móviles está en curso. |
| OBJ-I-03 | Garantizar la trazabilidad total de los datos | Dejar constancia de todo cambio de datos —quién, cuándo, desde dónde, el valor anterior y el nuevo—, de cada ingreso al sistema y de cada operación rechazada, sin que ninguna persona pueda modificar ni borrar ese registro, y ofrecer al administrador su consulta. | Alta | Realiza OBJ-04 y OBJ-05 por medio de IRQ-16, NFR-10 y CU-152. |
| OBJ-I-04 | Sostener la operación de varias distribuidoras | Mantener aislados los datos de cada distribuidora en todos los casos de uso de la iteración. | Alta | Realiza OBJ-09 por medio de NFR-09. |
| OBJ-I-05 | Ordenar el alcance por importancia | Mantener la lista completa de los casos de uso con su importancia (sección 4), de modo que cada iteración tome los que corresponden. | Media | Las ganancias del chofer y las comisiones por entrega quedan fuera del alcance, porque el chofer cobra un sueldo mensual. |

---

## 7. Requisitos de Información

*Debe tener una lista de requisitos de almacenamientos y de restricciones de información que se haya identificado.*

### IRQ-01 — Información sobre Usuarios

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-01, OBJ-05 |
| **Requisitos asociados** | CU-001, CU-002, CU-004, CU-031, CU-046, CU-047, CU-050, CU-082, CU-083, CU-085, CU-086, CU-087, CU-088, CU-089, CU-092, CU-094, CU-095, CU-100, CU-102, CU-106, CU-108, CU-116, CU-117, CU-118, CU-119, CU-120, CU-121, CU-143, CU-144, CU-145, CU-147, CU-148, CU-235, CU-251, CU-252, CU-253, CU-254, CU-270, CU-272, CU-331, CU-336, CU-345, CU-346 |
| **Descripción** | El sistema debe almacenar y gestionar la información de los tres tipos de usuario del sistema. |
| **Datos específicos** | Nombre completo, email (único), número de teléfono, rol (cliente, chofer o administrador), fecha de registro, estado activo/inactivo, identificación del dispositivo al que se le envían los avisos, estado de validación (para choferes). |
| **Estabilidad** | Alta |

### IRQ-02 — Información sobre Pedidos

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-01, OBJ-02, OBJ-06 |
| **Requisitos asociados** | CU-005, CU-006, CU-007, CU-008, CU-009, CU-010, CU-011, CU-012, CU-013, CU-014, CU-015, CU-016, CU-018, CU-019, CU-020, CU-048, CU-060, CU-061, CU-062, CU-064, CU-068, CU-070, CU-072, CU-073, CU-075, CU-076, CU-077, CU-078, CU-079, CU-080, CU-081, CU-101, CU-105, CU-106, CU-107, CU-108, CU-122, CU-123, CU-124, CU-125, CU-126, CU-127, CU-128, CU-149, CU-169, CU-170, CU-231, CU-236, CU-292, CU-293, CU-294, CU-299, CU-300, CU-301, CU-302, CU-303, CU-304, CU-332, CU-338, CU-339, CU-341 |
| **Descripción** | El sistema debe almacenar el historial completo de cada pedido desde su creación hasta la entrega o cancelación, incluyendo todos los cambios de estado y sus marcas de tiempo. |
| **Datos específicos** | Identificador del pedido, cliente, chofer asignado (vacío mientras no lo tiene), coordenadas de entrega, ítems y cantidades, precio unitario al momento de compra, subtotal por ítem, descuento aplicado (%), total del pedido, medio de pago (efectivo, MercadoPago o transferencia), estado del pago (pendiente, pagado, fallido, impago o dado por incobrable), estado del pedido (reservado, pendiente, aceptado, en camino, entregado o cancelado), franja horaria seleccionada, fecha solicitada de entrega, ventana de entrega (inicio y fin), cantidad de intentos de despacho, motivo de cancelación (si aplica) y el momento de la creación, de la aceptación, de la salida y de la entrega. De cada cambio de estado: estado anterior (vacío en la creación), estado nuevo, usuario que lo originó (vacío si fue un proceso programado), motivo y fecha. Del carrito del cliente, que precede al pedido: cliente, distribuidora, y por cada ítem el tipo de garrafa, la cantidad y el precio unitario vigente al agregarlo, como referencia. |
| **Estabilidad** | Alta |

### IRQ-03 — Información sobre Choferes y Vehículos

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-02, OBJ-05 |
| **Requisitos asociados** | CU-006, CU-012, CU-013, CU-014, CU-015, CU-017, CU-022, CU-031, CU-032, CU-033, CU-034, CU-035, CU-051, CU-064, CU-065, CU-081, CU-096, CU-097, CU-105, CU-107, CU-109, CU-110, CU-111, CU-112, CU-113, CU-114, CU-115, CU-129, CU-130, CU-131, CU-136, CU-137, CU-138, CU-139, CU-140, CU-141, CU-142, CU-155, CU-156, CU-157, CU-158, CU-159, CU-160, CU-161, CU-162, CU-163, CU-164, CU-165, CU-195, CU-196, CU-197, CU-198, CU-199, CU-200, CU-201, CU-202, CU-203, CU-204, CU-205, CU-206, CU-231, CU-232, CU-233, CU-247, CU-266, CU-267, CU-271, CU-320, CU-321, CU-322, CU-323, CU-324, CU-325, CU-326, CU-327, CU-328, CU-330, CU-337, CU-338 |
| **Descripción** | El sistema debe registrar los datos del repartidor, su estado operativo, el vehículo asociado y el vehículo que usa en cada momento, con el historial de quién usó cada vehículo. |
| **Datos específicos** | Datos del usuario (ver IRQ-01). Del perfil del chofer: calificación promedio, estado de validación, estado activo y ubicación GPS actual. Del vehículo: tipo (auto / moto / camioneta), patente, marca, modelo, año, color, capacidad de carga. De cada asignación de vehículo: chofer, vehículo, fecha de asignación, fecha de liberación (vacía mientras está en uso), administrador que la hizo, administrador que la cerró y nota. Del vehículo, además: tipo de combustible y capacidad del tanque. De cada carga de combustible: fecha y hora, tipo de combustible, litros, precio por litro, importe, kilometraje, si se llenó el tanque, estación, medio de pago, comprobante y si es anómala. De cada multa de tránsito: fecha de la infracción, jurisdicción, número de acta, infracción, importe, importe con pago voluntario, vencimiento, estado, fecha e importe de pago y si se imputó al chofer. De cada siniestro: fecha, lugar, descripción, heridos, terceros, derrame de gas, denuncia policial, reclamo al seguro, estado, costos y cierre. De cada neumático: serie, marca, medida, costo, estado, posición y movimientos. |
| **Estabilidad** | Alta |

### IRQ-04 — Información sobre Productos (Garrafas)

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-06, OBJ-07 |
| **Requisitos asociados** | CU-005, CU-008, CU-010, CU-016, CU-036, CU-037, CU-038, CU-039, CU-040, CU-041, CU-067, CU-076, CU-077, CU-106, CU-268, CU-269, CU-339, CU-341, CU-344 |
| **Descripción** | El sistema debe almacenar el catálogo de garrafas disponibles con su precio vigente y stock actual. |
| **Datos específicos** | Tipo de garrafa (ej: "10kg", "15kg", "45kg"), peso, precio de venta vigente, stock disponible, descripción opcional, estado activo/inactivo, promociones por volumen (cantidad mínima y porcentaje de descuento de cada una). |
| **Estabilidad** | Alta |

### IRQ-05 — Información sobre Franjas Horarias

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-01, OBJ-08 |
| **Requisitos asociados** | CU-005, CU-042, CU-043, CU-044, CU-045, CU-107, CU-132, CU-133, CU-134, CU-135, CU-154, CU-339, CU-341, CU-342, CU-343 |
| **Descripción** | El sistema debe almacenar las franjas horarias de entrega configuradas por el administrador y controlar su capacidad. |
| **Datos específicos** | Nombre de la franja (ej: "Mañana", "Tarde"), hora de inicio (HH:MM), hora de fin (HH:MM), capacidad máxima diaria de pedidos, estado activo/inactivo. |
| **Estabilidad** | Alta |

### IRQ-06 — Información sobre Reclamos

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-04, OBJ-05 |
| **Requisitos asociados** | CU-023, CU-024, CU-025, CU-146, CU-166, CU-167, CU-174, CU-175 |
| **Descripción** | El sistema debe registrar los reclamos realizados por clientes sobre pedidos entregados, incluyendo la evidencia adjunta y la resolución del administrador. |
| **Datos específicos** | Identificador del reclamo, referencia al pedido asociado, referencia al cliente reclamante, motivo del reclamo (texto libre), descripción detallada, referencia de la foto de evidencia —clave del almacenamiento o dirección externa— (opcional), estado (pendiente, en proceso, resuelto o rechazado), nota de resolución del administrador (obligatoria al resolver/rechazar), fecha de creación. |
| **Estabilidad** | Alta |

### IRQ-07 — Información sobre Direcciones de Entrega

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-01, OBJ-02 |
| **Requisitos asociados** | CU-005, CU-026, CU-027, CU-028, CU-029, CU-030, CU-046, CU-058, CU-094, CU-339, CU-341 |
| **Descripción** | El sistema debe almacenar las direcciones de entrega del cliente para agilizar la creación de futuros pedidos. |
| **Datos específicos** | Referencia al cliente propietario, calle y número, referencia adicional (ej: "departamento 3B, timbre roto"), latitud, longitud, alias de la dirección (ej: "Casa", "Trabajo"). |
| **Estabilidad** | Alta |

### IRQ-08 — Información sobre Pagos y Transacciones

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-07 |
| **Requisitos asociados** | CU-005, CU-020, CU-029, CU-048, CU-072, CU-074, CU-077, CU-079, CU-168, CU-225, CU-228, CU-237, CU-264, CU-292, CU-293, CU-294, CU-299, CU-300, CU-301, CU-309, CU-310, CU-329, CU-340, CU-348 |
| **Descripción** | El sistema debe registrar la información del pago asociado a cada pedido, incluyendo el método, el estado y la referencia externa de MercadoPago cuando corresponda. |
| **Datos específicos** | Medio de pago (efectivo, MercadoPago o transferencia), estado del pago (pendiente, pagado o fallido), recargo aplicado (porcentaje y monto), identificador del cobro en MercadoPago (para los pagos en línea), marca de tiempo de confirmación de pago, estado reintegrado del pago cuando el importe se devolvió por la pasarela. |
| **Estabilidad** | Alta |

### IRQ-09 — Información sobre Distribuidoras

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-09 |
| **Requisitos asociados** | CU-052, CU-053, CU-054, CU-055, CU-056, CU-057, CU-059, CU-150, CU-151, CU-171, CU-172, CU-305, CU-306, CU-307, CU-308 |
| **Descripción** | El sistema debe almacenar los datos de cada empresa comercializadora que opera en la plataforma, junto con el identificador al que queda acotada toda la información de gestión del resto de los subsistemas. |
| **Datos específicos** | Identificador de la distribuidora — clave a la que se ata todo dato de gestión del sistema; Nombre comercial — denominación con la que se muestra la empresa; Nombre corto (slug) — identificador legible y único con el que se resuelve la distribuidora en el encabezado de la petición; Razón social — nombre legal de la empresa; Identificación fiscal (CUIT) — clave tributaria de la empresa; Email y teléfono de contacto — datos de contacto de la distribuidora; URL del logotipo — imagen que identifica a la empresa en las aplicaciones; Estado — activa o suspendida; Plan contratado — plan de servicio asignado a la empresa; Fecha de alta, fecha de última modificación y marca de baja lógica — la baja no borra el registro para no romper las referencias de sus pedidos; Configuración de procesos automáticos — por proceso, los parámetros de la distribuidora (pasos de radio y ventana de aceptación del despacho, parámetros de cada módulo inteligente, frecuencia de las tareas programadas), con el usuario que los modificó y la fecha. |
| **Estabilidad** | Alta |
| **Comentarios** | Es la dimensión transversal del sistema (SS-10): el identificador de la distribuidora se repite en las entidades de negocio y acota toda consulta de gestión. La búsqueda por nombre corto existe internamente y la usan los puntos de acceso públicos de catálogo (CU-041) y de franjas horarias (CU-045), pero no está expuesta como operación del Administrador General (CU-053). |

### IRQ-10 — Información sobre Zonas de Cobertura

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-10, OBJ-09 |
| **Requisitos asociados** | CU-005, CU-056, CU-057, CU-058, CU-059, CU-072, CU-150, CU-151, CU-305, CU-306, CU-307, CU-308 |
| **Descripción** | El sistema debe almacenar las áreas geográficas dentro de las cuales cada distribuidora acepta pedidos, con el recargo asociado a cada área, para poder resolver si un domicilio queda cubierto y con qué costo adicional. |
| **Datos específicos** | Identificador de la zona — clave de la zona de cobertura; Distribuidora propietaria — empresa a la que pertenece la zona; las consultas se acotan siempre por este dato; Nombre de la zona — denominación con la que el administrador la identifica (ej.: "Centro", "Villa Cabello"); Polígono del área — vértices que delimitan la zona, en coordenadas geográficas, sobre los que se resuelve si un punto cae dentro; Recargo — tipo (monto fijo o porcentaje sobre el subtotal de ítems) y valor, que se suman al total del pedido entregado dentro de la zona; Estado activo/inactivo — indica si la zona se considera en la validación de cobertura; Fecha de alta y fecha de última modificación — momento en que se definió la zona y en que se la modificó por última vez. |
| **Estabilidad** | Alta |
| **Comentarios** | Si la distribuidora no definió ninguna zona, el sistema asume cobertura total con recargo cero: la ausencia de zonas no bloquea la operación. El resultado de la validación devuelve si el punto está cubierto, el nombre de la zona alcanzada y el recargo que le corresponde. |

### IRQ-11 — Información sobre Incidencias de Entrega

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-11, OBJ-04 |
| **Requisitos asociados** | CU-060, CU-061, CU-062, CU-063 |
| **Descripción** | El sistema debe registrar los contratiempos ocurridos durante el reparto de un pedido, con su evidencia y el usuario que los reportó, y conservar la resolución que el administrador les da. |
| **Datos específicos** | Identificador de la incidencia — clave de la incidencia; Pedido afectado — pedido sobre el que se reporta el contratiempo; Distribuidora — se toma del pedido referenciado y no del usuario que reporta; Usuario que reporta — identificador del chofer o del administrador que deja asentada la incidencia; Tipo — producto dañado, faltante de stock, cliente ausente u otro; Descripción — relato de lo sucedido durante la entrega; URL de la foto — evidencia fotográfica opcional; Estado — abierta o resuelta; Nota de resolución — texto con el que el administrador cierra la incidencia; Fecha de creación y fecha de resolución — momento en que se reportó y en que se cerró. |
| **Estabilidad** | Alta |
| **Comentarios** | La incidencia no reemplaza al reclamo (IRQ-06): el reclamo lo levanta el cliente después de la entrega, la incidencia la deja el chofer durante el reparto. El alta toma la distribuidora del pedido y no la del contexto de la petición, limitación conocida del aislamiento entre distribuidoras. |

### IRQ-12 — Información sobre Calificaciones

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-12, OBJ-04 |
| **Requisitos asociados** | CU-064, CU-065, CU-066 |
| **Descripción** | El sistema debe registrar la valoración que el cliente y el chofer se dan mutuamente al cerrarse el pedido, y sostener con ella el promedio de calificación de cada usuario. |
| **Datos específicos** | Identificador de la calificación; Pedido calificado — pedido entregado sobre el que se emite la valoración; Distribuidora — se toma del pedido, de modo que los promedios del panel quedan por empresa; Usuario emisor — quien califica; se toma del usuario identificado, nunca de lo que se envía; Usuario calificado — el otro lado del pedido; se deriva del propio pedido; Lado emisor — cliente o chofer; junto con el pedido forma la restricción de unicidad que admite una sola calificación por lado; Puntaje — valoración de 1 a 5 estrellas; Comentario — observación escrita opcional de quien califica; Fecha de emisión — momento en que se registró la calificación. |
| **Estabilidad** | Alta |
| **Comentarios** | Cuando la calificación la emite el cliente, el sistema recalcula además el promedio del chofer y lo guarda en su perfil (IRQ-03). El promedio del cliente se calcula al consultarlo y no se persiste en su perfil. |

### IRQ-13 — Información sobre Envases Físicos y sus Movimientos

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-13, OBJ-04 |
| **Requisitos asociados** | CU-067, CU-068, CU-069, CU-070, CU-071 |
| **Descripción** | El sistema debe registrar cada botellón físico identificado por su número de serie, su situación actual y quién lo tiene, junto con la traza completa de los cambios de estado por los que pasó. |
| **Datos específicos** | Identificador del envase — clave del botellón físico; Distribuidora propietaria — empresa dueña del envase; Número de serie — identificación grabada en el botellón; es única por distribuidora, no a nivel de toda la plataforma; Tipo de producto — formato de garrafa al que corresponde el envase (IRQ-04); Estado — en depósito, lleno, despachado, en poder del cliente o vacío devuelto; Cliente actual — usuario que tiene el envase en su poder; solo se completa mientras el envase está con el cliente; Pedido actual — pedido en el que el envase salió despachado; permite avanzarlo al confirmarse la entrega; Importe de garantía — monto en depósito que representa el envase; Fecha de alta y fecha de última modificación — momento en que se incorporó al parque y en que cambió por última vez; Movimiento: estado de origen y estado de destino — situación anterior y posterior; el estado de origen queda vacío en el movimiento que inaugura la trazabilidad; Movimiento: pedido asociado — pedido en cuyo contexto ocurrió la transición, si corresponde; Movimiento: usuario que lo ejecutó — chofer o administrador responsable del cambio de estado; Movimiento: nota y fecha — motivo del movimiento y momento en que se produjo. |
| **Estabilidad** | Alta |
| **Comentarios** | No confundir con IRQ-04: aquel describe el producto que se vende, con su precio y su stock agregado; este describe el envase concreto que se entrega y se espera recuperar. El historial de movimientos es de solo agregado: no se edita ni se borra, únicamente se lee para reconstruir el recorrido del envase. |

### IRQ-14 — Información sobre Reservas Programadas y su Seña

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-14, OBJ-06, OBJ-07 |
| **Requisitos asociados** | CU-072, CU-073, CU-074, CU-075, CU-076 |
| **Descripción** | El sistema debe registrar los pedidos apartados para una fecha futura y el estado de la seña que los garantiza, para poder activarlos el día agendado o expirarlos cuando la seña no se cobra. |
| **Datos específicos** | Indicador de reserva — dato del cuerpo del pedido que hace que este nazca en estado reservado; la fecha agendada por sí sola no lo convierte en reserva; Estado reservado — situación en la que el pedido no se ofrece a ningún chofer y el stock ya quedó descontado; Fecha de entrega agendada — día para el que el cliente apartó la mercadería; es obligatoria en toda reserva; Monto de la seña — importe que el cliente deja en garantía al reservar; Seña cobrada — indica si la seña se acreditó; arranca siempre en falso y la marca el aviso de la pasarela o la confirmación manual del administrador; Enlace de pago de la seña — preferencia generada solo por el importe de la seña cuando el medio elegido es MercadoPago (IRQ-08); Saldo restante — diferencia entre el total del pedido y la seña, calculada al momento de listar las reservas y no almacenada; Motivo de cancelación — texto con el que queda cancelada la reserva que expiró sin seña cobrada; Plazo de gracia de la seña — cantidad de horas configurable tras las cuales la reserva impaga se cancela y el stock se restituye. |
| **Estabilidad** | Alta |
| **Comentarios** | La reserva se apoya sobre los mismos datos del pedido (IRQ-02) y sobre el stock del producto (IRQ-04): el descuento se hace al reservar y la restitución, al expirar. Los procesos automáticos que activan y expiran reservas no se acotan por distribuidora, por ser procesos de plataforma. |

### IRQ-15 — Información sobre el Estado Operativo del Sistema

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-15, OBJ-05 |
| **Requisitos asociados** | CU-100, CU-102, CU-104, CU-173 |
| **Descripción** | El sistema debe reunir e informar el estado de sus componentes y el resultado de las pruebas de sus canales de aviso, de modo que el orquestador sepa si la instancia puede recibir tráfico y el administrador pueda diagnosticar la mensajería. |
| **Datos específicos** | Estado de la sonda de vida — indicación de que el proceso responde, acompañada de su marca temporal; Estado de la base de datos — resultado de la verificación de conexión con la base de datos; Estado del caché — resultado de la verificación de conexión con el caché, del que dependen el despacho por proximidad y el seguimiento en vivo; Memoria residente del proceso — consumo medido contra el umbral de 300 MB; Ocupación de disco — margen libre medido contra el umbral del 90 %; Diagnóstico de notificaciones: dispositivo de destino, título y cuerpo — datos con los que se arma el mensaje de prueba; Diagnóstico de notificaciones: identificador del mensaje o error devuelto — resultado que entrega el proveedor de mensajería; Diagnóstico de correo: dirección de destino y resultado del envío — dirección probada y estado devuelto por el proveedor; Diagnóstico de correo: comportamiento de la caché de enlaces — indica si los dos enlaces de recuperación generados seguidos resultaron iguales. |
| **Estabilidad** | Media |
| **Comentarios** | Estos datos no se persisten: se calculan en el momento de la consulta y solo quedan en el registro de eventos. Es el requisito de información que sostiene a NFR-03 (Disponibilidad) y NFR-04 (Escalabilidad). La prueba del servicio de correo es una operación de diagnóstico exclusiva del Administrador General (CU-102). |

### IRQ-16 — Información sobre el Registro de Auditoría

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-04, OBJ-05 |
| **Requisitos asociados** | CU-152 |
| **Descripción** | El sistema debe dejar constancia de todo cambio de datos y de toda operación de escritura, de modo que se pueda reconstruir después quién hizo qué, sobre qué y cuándo. Es lo que permite resolver una disputa con evidencia en lugar de con la palabra de cada parte. |
| **Datos específicos** | Auditoría de datos, una por cada registro afectado: tipo de acción (alta, modificación, baja lógica, reactivación, baja física, ingreso, ingreso fallido o salida); entidad afectada y registro; usuario que hizo el cambio, vacío si lo hizo un proceso automático; distribuidora a la que corresponde; dirección de red; fecha y hora; origen (un usuario, un proceso automático del sistema o un cambio hecho directamente sobre la base de datos) y, por cada campo que cambió, el valor anterior y el nuevo. Para un ingreso, el correo, el canal y, si falló, el motivo. Registro de operaciones, uno por cada operación de escritura: autor y su rol al momento de hacerla, distribuidora, operación y recurso afectado, fecha y hora, aplicación de origen (panel, aplicación del cliente o del chofer), dirección de red, resultado —exitosa o rechazada, con el motivo— y lo que se pidió, **con las credenciales depuradas**. |
| **Estabilidad** | Alta |
| **Comentarios** | La auditoría de datos la escribe la propia base de datos, con un disparador en cada tabla y dentro de la misma operación que hace el cambio: alcanza a lo que hace un usuario, a lo que hacen los procesos automáticos y a un cambio hecho directamente sobre la base, que queda con su origen. Un dato que no cambió no genera asiento, y las contraseñas y los códigos secretos se guardan ocultos. Los dos registros son de **solo escritura**: el sistema no ofrece ninguna operación de modificación ni de baja sobre ellos, para ningún rol, y la base de datos rechaza toda modificación, todo borrado y todo vaciado. Este requisito sostiene a OBJ-04 (trazabilidad) más allá de la entrega: OBJ-04 pedía evidencia objetiva de una entrega y esto la extiende a todo dato del sistema. |

### IRQ-17 — Información sobre el Personal y sus Legajos

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-05, OBJ-09 |
| **Requisitos asociados** | CU-176, CU-177, CU-178, CU-179, CU-180, CU-181, CU-182, CU-183, CU-184, CU-185, CU-186, CU-187, CU-188, CU-189, CU-190, CU-191, CU-192, CU-193, CU-194, CU-246, CU-255, CU-256, CU-257, CU-311, CU-312, CU-313, CU-314, CU-315, CU-316, CU-317, CU-318, CU-319 |
| **Descripción** | El sistema debe llevar el legajo de cada persona que trabaja en la distribuidora, tenga o no cuenta de acceso, y su asistencia, sus licencias y la documentación con vencimiento que se le exige según su puesto, para que la distribuidora sepa quién trabaja, quién está presente y quién no está en regla. |
| **Datos específicos** | Puesto (nombre y categoría); legajo (número, nombre, apellido, tipo y número de documento, CUIL, fecha de nacimiento, domicilio, teléfono, correo personal, contacto de emergencia, fecha de ingreso, modalidad de contratación, estado, fecha y motivo de egreso); cuenta de acceso, si la tiene; jornada (día, ingreso, egreso, origen, nota); licencia (tipo, período, días, estado, motivo, quién y cuándo la resolvió); documentación con vencimiento, como tarea de un plan con dueño empleado; archivos adjuntos con su etiqueta. |
| **Estabilidad** | Media |
| **Comentarios** | Puestos, legajos, documentación con vencimiento, asistencia y licencias construidos (C-08). El documento, el CUIL, el domicilio y el contacto de emergencia son datos personales (Ley 25.326): solo salen en la ficha y no en los listados. La baja del empleado es el egreso, que conserva el legajo. Una persona que no es chofer ni administrador no tiene cuenta: el sistema no define roles para ella. |

### IRQ-18 — Información sobre Stock, Compras y Carga del Camión

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-05, OBJ-06 |
| **Requisitos asociados** | CU-020, CU-038, CU-207, CU-208, CU-209, CU-210, CU-211, CU-212, CU-213, CU-214, CU-215, CU-216, CU-217, CU-218, CU-219, CU-220, CU-221, CU-222, CU-223, CU-224, CU-248, CU-249, CU-250, CU-258, CU-259, CU-260, CU-261, CU-262, CU-263, CU-273, CU-274, CU-275, CU-276, CU-277, CU-278, CU-279, CU-280, CU-281, CU-282, CU-283, CU-284, CU-285, CU-286, CU-287, CU-288, CU-289, CU-290, CU-291, CU-295, CU-296, CU-297, CU-298 |
| **Descripción** | El sistema debe llevar el stock físico de garrafas por ubicación (depósitos y camiones) y por condición, con el libro de cada movimiento, y reconciliarlo con el stock vendible del catálogo; registrar a los proveedores, las órdenes de compra y las recepciones de lo comprado; y registrar la hoja de carga de cada camión, desde que se carga hasta que se rinde. |
| **Datos específicos** | De cada depósito: nombre, código (único entre los vigentes de la distribuidora), tipo (depósito o sucursal), dirección, si es el predeterminado y su estado. De cada ubicación de stock: si es un depósito o un vehículo. De cada saldo: tipo de garrafa, condición (llena, vacía o defectuosa) y cantidad, nunca negativa. De cada movimiento, de solo agregado: tipo de garrafa, cantidad, ubicación y condición de origen y de destino, motivo, documento que lo originó, autor y momento. De cada umbral: depósito, tipo de garrafa, mínimo de llenas y momento del último aviso. De cada ajuste: número correlativo, ubicación, motivo, nota obligatoria y renglones con la diferencia por tipo de garrafa y condición. De cada proveedor: razón social, CUIT (único entre los vigentes), tipo, contacto y plazo de pago. De cada orden de compra: número, proveedor, depósito destino, estado (borrador, enviada, parcialmente recibida, recibida, cerrada con faltante o cancelada), fecha de emisión y fecha esperada, total, motivos de cancelación y de cierre, y renglones con cantidad, costo unitario, vacíos a canjear y cantidad recibida. De cada recepción: número interno, tipo y número del comprobante del proveedor (único por proveedor y tipo), depósito, fecha de recepción, renglones con las llenas recibidas, los vacíos entregados, el costo y el promedio y la existencia previos, estado de pago y estado, y motivo y fecha de anulación. De cada carga de camión: número, vehículo, chofer, ayudante, depósito de salida, día, estado, instantes de apertura, salida, regreso y cierre, renglones con lo cargado, repuesto, declarado, entregado, esperado y la diferencia, y la nota de la diferencia. Del tipo de garrafa: el costo promedio ponderado. |
| **Estabilidad** | Media |
| **Comentarios** | Es un modelo cuantitativo, por cantidad y tipo, y no reemplaza al envase con número de serie (IRQ-13), que sigue siendo la trazabilidad individual. El stock vendible de IRQ-04 es lo que ya se reserva al crear un pedido; el físico se mantiene aparte y una invariante, que verifica un proceso nocturno, los relaciona: vendible igual a lo lleno en depósitos y camiones menos lo reservado por pedidos abiertos. El saldo de un camión es cero al cerrar su rendición. Construidos: el stock físico, las compras y la carga y rendición del camión. |

### IRQ-19 — Información sobre Caja, Rendiciones y Cuentas Corrientes

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-05, OBJ-07 |
| **Requisitos asociados** | CU-225, CU-226, CU-227, CU-228, CU-229, CU-230, CU-231, CU-232, CU-233, CU-234, CU-235, CU-236, CU-237, CU-238, CU-239, CU-245, CU-264, CU-265, CU-309, CU-310, CU-329, CU-330, CU-331, CU-332, CU-340 |
| **Descripción** | El sistema debe llevar el dinero de la distribuidora: las cajas con su saldo y su libro de movimientos, la rendición diaria de lo que cobra cada chofer y las cuentas corrientes de los clientes con crédito. |
| **Datos específicos** | Caja — nombre, tipo (efectivo, banco o billetera), saldo y si exige sesión; sesión de caja — apertura, cierre, monto inicial, esperado, contado y diferencia; movimiento de caja — sentido, importe, categoría, medio y origen, de solo agregar; categoría de caja — ingreso o egreso, de sistema o propia; rendición del chofer — día, pedidos en efectivo, cobros en la calle, gastos, efectivo esperado y declarado, diferencia y su resolución; cuenta corriente — razón social, CUIT, condición fiscal, límite de crédito, plazo de pago, estado y saldo; asiento de cuenta corriente — cargo, pago, nota de crédito o de débito, con su vencimiento; imputación — qué pago cubre qué cargo. |
| **Estabilidad** | Alta |
| **Comentarios** | Los importes se guardan con precisión decimal fija y se calculan con aritmética decimal. Los dos libros (caja y cuenta corriente) son de solo agregar: se corrigen con un asiento de sentido contrario y la base rechaza toda modificación o borrado. El saldo de una caja y el de una cuenta son copias del libro que se concilian todas las noches. El chofer cobra un sueldo mensual: las comisiones por entrega y su liquidación quedan fuera del alcance. |

---

## 8. Requisitos Funcionales — Casos de Uso

*Debe tener una lista de los requisitos funcionales, expresado en forma tradicional o mediante casos de usos*

Los requisitos funcionales se expresan con casos de uso. La lista de todos los casos, con su
importancia, está en la sección 4 y su descripción de alto nivel, en el Documento 0. Esta sección
reúne el diagrama de casos de uso de cada subsistema (8.1), la definición de los actores (8.2) y el
caso de uso expandido de los 21 casos de uso esenciales de la iteración (8.3). El diagrama de secuencia
del sistema de cada uno de esos casos está en el Documento 2 y su diagrama de interacción, en el
Documento 3.

### 8.1 Diagramas de Casos de Uso por Subsistema

Cada subsistema tiene su diagrama de casos de uso, en notación UML: los actores fuera del límite, los casos de uso dentro, las relaciones `«include»` y `«extend»` con sus puntos de extensión, y el Administrador General dibujado como especialización del Administrador. Por eso el Administrador General se asocia solo a los casos que son exclusivos suyos: los demás los hereda. Los casos de otro subsistema que uno de éste incluye o extiende se dibujan fuera del límite, con el código de su subsistema. Cada diagrama muestra todos los casos de uso de su subsistema, también los que en esta iteración no tienen su caso de uso expandido.

![SS-01 Autenticación y Usuarios](../diagramas/uml/CU_SS-01_Autenticacion-Y-Usuarios.png)

**Figura 4 — SS-01 Autenticación y Usuarios: casos de uso**

![SS-02 Gestión de Pedidos, parte 1 de 2](../diagramas/uml/CU_SS-02_Gestion-De-Pedidos_Parte-1.png)

**Figura 5 — SS-02 Gestión de Pedidos, parte 1 de 2: casos de uso**

![SS-02 Gestión de Pedidos, parte 2 de 2](../diagramas/uml/CU_SS-02_Gestion-De-Pedidos_Parte-2.png)

**Figura 6 — SS-02 Gestión de Pedidos, parte 2 de 2: casos de uso**

![SS-03 Despacho y Asignación](../diagramas/uml/CU_SS-03_Despacho-Y-Asignacion.png)

**Figura 7 — SS-03 Despacho y Asignación: casos de uso**

![SS-04 Seguimiento en Tiempo Real](../diagramas/uml/CU_SS-04_Seguimiento-En-Tiempo-Real.png)

**Figura 8 — SS-04 Seguimiento en Tiempo Real: casos de uso**

![SS-05 Reclamos](../diagramas/uml/CU_SS-05_Reclamos.png)

**Figura 9 — SS-05 Reclamos: casos de uso**

![SS-06 Reportes y Tablero](../diagramas/uml/CU_SS-06_Reportes-Y-Dashboard.png)

**Figura 10 — SS-06 Reportes y Tablero: casos de uso**

![SS-07 Choferes](../diagramas/uml/CU_SS-07_Choferes.png)

**Figura 11 — SS-07 Gestión de Choferes y Vehículos: casos de uso, choferes (lámina 1 de 3)**

![SS-07 Vehículos y vencimientos](../diagramas/uml/CU_SS-07_Vehiculos.png)

**Figura 12 — SS-07 Gestión de Choferes y Vehículos: casos de uso, vehículos y vencimientos (lámina 2 de 3)**

![SS-07 Costos, siniestros y adjuntos de flota](../diagramas/uml/CU_SS-07_Costos-Siniestros-Y-Adjuntos.png)

**Figura 13 — SS-07 Gestión de Choferes y Vehículos: casos de uso, costos, siniestros y adjuntos de flota (lámina 3 de 3)**

![SS-08 Gestión de Productos e Inventario, parte 1 de 2](../diagramas/uml/CU_SS-08_Gestion-De-Productos_Parte-1.png)

**Figura 14 — SS-08 Gestión de Productos e Inventario, parte 1 de 2: casos de uso**

![SS-08 Gestión de Productos e Inventario, parte 2 de 2](../diagramas/uml/CU_SS-08_Gestion-De-Productos_Parte-2.png)

**Figura 15 — SS-08 Gestión de Productos e Inventario, parte 2 de 2: casos de uso**

![SS-09 Franjas Horarias](../diagramas/uml/CU_SS-09_Franjas-Horarias.png)

**Figura 16 — SS-09 Franjas Horarias: casos de uso**

![SS-10 Multi-Distribuidora](../diagramas/uml/CU_SS-10_Multi-Distribuidora.png)

**Figura 17 — SS-10 Multi-Distribuidora: casos de uso**

![SS-11 Cobertura Geográfica](../diagramas/uml/CU_SS-11_Cobertura-Geografica.png)

**Figura 18 — SS-11 Cobertura Geográfica: casos de uso**

![SS-12 Incidencias y Calidad de Servicio](../diagramas/uml/CU_SS-12_Incidencias-Y-Calidad-De-Servicio.png)

**Figura 19 — SS-12 Incidencias y Calidad de Servicio: casos de uso**

![SS-13 Trazabilidad de Envases](../diagramas/uml/CU_SS-13_Trazabilidad-De-Envases.png)

**Figura 20 — SS-13 Trazabilidad de Envases: casos de uso**

![SS-14 Pagos y Conciliación](../diagramas/uml/CU_SS-14_Pagos-Y-Conciliacion.png)

**Figura 21 — SS-14 Pagos y Conciliación: casos de uso**

![SS-15 Reservas Programadas](../diagramas/uml/CU_SS-15_Reservas-Programadas.png)

**Figura 22 — SS-15 Reservas Programadas: casos de uso**

![SS-16 Administración de Cuentas y Roles](../diagramas/uml/CU_SS-16_Administracion-De-Cuentas-Y-Roles.png)

**Figura 23 — SS-16 Administración de Cuentas y Roles: casos de uso**

![SS-17 Notificaciones y Mensajería](../diagramas/uml/CU_SS-17_Notificaciones-Y-Mensajeria.png)

**Figura 24 — SS-17 Notificaciones y Mensajería: casos de uso**

![SS-18 Observabilidad y Operación](../diagramas/uml/CU_SS-18_Observabilidad-Y-Operacion.png)

**Figura 25 — SS-18 Observabilidad y Operación: casos de uso**

![SS-19 Personal y Legajos](../diagramas/uml/CU_SS-19_Personal-Y-Legajos.png)

**Figura 26 — SS-19 Personal y Legajos: casos de uso**
![SS-20 Compras](../diagramas/uml/CU_SS-20_Compras.png)

**Figura 27 — SS-20 Compras: casos de uso**
![SS-21 Caja, Rendiciones y Cuentas Corrientes, parte 1 de 2](../diagramas/uml/CU_SS-21_Caja-Rendiciones-Y-Cuentas-Corrientes_Parte-1.png)

**Figura 28 — SS-21 Caja, Rendiciones y Cuentas Corrientes, parte 1 de 2: casos de uso**

![SS-21 Caja, Rendiciones y Cuentas Corrientes, parte 2 de 2](../diagramas/uml/CU_SS-21_Caja-Rendiciones-Y-Cuentas-Corrientes_Parte-2.png)

**Figura 29 — SS-21 Caja, Rendiciones y Cuentas Corrientes, parte 2 de 2: casos de uso**

### 8.2 Definición de Actores

| Código | Actor | Tipo | Descripción |
|--------|-------|:----:|-------------|
| ACT-01 | **Cliente** | Humano | Usuario final que compra garrafas de gas. Usa la aplicación del cliente en su teléfono: hace pedidos, elige la franja de entrega y el medio de pago, sigue el pedido en el mapa, administra sus direcciones y puede reclamar si algo sale mal. Inicia 48 casos de uso. |
| ACT-02 | **Chofer** | Humano | Repartidor de la distribuidora. Usa la aplicación del chofer en su teléfono: se pone en línea, recibe las ofertas de pedidos cercanos, las acepta o las rechaza, informa su posición, entrega y rinde lo cobrado. Inicia 45 casos de uso. |
| ACT-03 | **Administrador** | Humano | Operador de una distribuidora, con alcance acotado a su propia empresa. Usa el panel web para gestionar choferes, vehículos, productos, stock, compras, personal, caja, cuentas corrientes, franjas horarias, reclamos y reportes. Tiene acceso total dentro de su distribuidora, salvo la cuenta de un cliente, que administra el Administrador General. Inicia 249 casos de uso. |
| ACT-04 | **Sistema Automático** | Automático | Actor externo que representa el Tiempo, según la convención de Larman: el reloj o temporizador que dispara los casos de uso programados —el vencimiento de las ofertas de despacho, la activación y el vencimiento de las reservas, los avisos y las conciliaciones, y las revisiones periódicas de los cinco procesos automatizados: asignación secuencial de pedidos, planificación predictiva del mantenimiento, anticipación de la recompra, agrupación de pedidos por recorrido y recuperación de envases no devueltos— sin que los inicie una persona ni un sistema externo. Lo que el backend hace al ser disparado es comportamiento del sistema, no del actor. Única excepción documentada: la primera oferta de CU-013 sale por dentro de CU-005, al confirmarse el alta del pedido; se mantiene bajo este actor porque sus reintentos los dispara el reloj (CU-014). Es el actor principal de 22 casos de uso. |
| ACT-05 | **Administrador General** | Humano | Operador de la plataforma, con alcance sobre todas las distribuidoras. Especializa al Administrador: hace todo lo que éste hace y además lo que es exclusivo de la plataforma —dar de alta las distribuidoras, designar a sus administradores y administrar los roles—. Es el único actor cuyo alcance no está acotado a una distribuidora; cuando escribe sobre pedidos, cobros, incidencias, reclamos, adjuntos o las cuentas del personal de una empresa, debe indicar con qué distribuidora trabaja: sin esa indicación el sistema no escribe nada. Participa en 71 casos de uso. |
| ACT-06 | **MercadoPago** | Secundario (sistema externo) | Pasarela de cobro, externa al sistema. El sistema le pide el cobro de cada pedido o seña que se paga por ese medio y recibe de ella el aviso de pago aprobado. Inicia CU-048 con ese aviso y participa como actor secundario en CU-005, CU-072 y CU-147. |
| ACT-07 | **Firebase** | Secundario (sistema externo) | Servicio externo de identidad y mensajería. Verifica quién es el usuario que ingresa, crea y deshabilita cuentas, genera el enlace de recuperación de contraseña y entrega las notificaciones a los dispositivos. No inicia ningún caso de uso; participa como actor secundario en CU-001, CU-004, CU-005, CU-013, CU-014, CU-015, CU-016, CU-018, CU-019, CU-020, CU-047, CU-072, CU-079, CU-082, CU-085, CU-100, CU-101 y CU-147. |
| ACT-08 | **Servicio de correo** | Secundario (sistema externo) | Servicio externo que envía los correos del sistema: bienvenida al cliente, recuperación de contraseña, prueba del servicio y avisos de vencimientos, de stock bajo, de rendiciones sin cerrar y de multas por vencer. No inicia ningún caso de uso; participa como actor secundario en CU-002, CU-047, CU-102, CU-142, CU-188, CU-211, CU-224, CU-234 y CU-326. |
| ACT-09 | **Plataforma de despliegue** | Primario (sistema externo) | Orquestador de contenedores, balanceador de carga o servicio de monitoreo, externo al sistema, que sondea el estado del backend para decidir si le envía tráfico o si reinicia la instancia. Es quien inicia CU-104. |
| ACT-10 | **Operador Técnico** | Humano | Persona con acceso al servidor donde corre el sistema, que lo pone en marcha. No usa el panel ni las aplicaciones: ejecuta una orden en el servidor para crear la cuenta inicial. Es quien inicia CU-087. |

![Actores del sistema y el canal por el que operan](../diagramas/uml/CU_Sistema_Actores.png)

**Figura 30 — Actores del sistema y el canal por el que operan**

> Los cinco actores humanos operan siempre a través de una aplicación o del panel web, salvo el Operador Técnico,
> que lo hace desde una consola del servidor; ninguno accede directamente a la base de datos. El Sistema
> Automático no tiene interfaz: son los procesos que el backend dispara por sí mismo, y es el
> actor principal de los casos de uso que la documentación marca como automáticos.
> MercadoPago, Firebase y el servicio de correo son sistemas externos que el backend invoca:
> participan como actores secundarios y no inician ningún caso de uso. La plataforma de
> despliegue es un sistema externo que, al revés, es quien consulta el estado del backend.

> **Generalización.** El Administrador General (ACT-05) es una especialización del Administrador (ACT-03): hace todo lo que hace éste y además lo que es exclusivo de la plataforma. La especialización no reemplaza a las asociaciones: en los diagramas, cada actor se une a todos sus casos de uso, también ACT-05 a los que comparte con ACT-03, y la generalización se mantiene entre los dos. ACT-06, ACT-07 y ACT-08 son actores secundarios: el sistema los invoca para completar un caso que inició otro actor.

---

### 8.3 Casos de Uso del Sistema

Los 21 casos de uso esenciales recorren el circuito completo del pedido con los tres actores humanos,
los cinco módulos inteligentes y la consulta de la auditoría. Se presentan en el orden del circuito:
ingreso y registro, alta y cancelación del pedido, disponibilidad del chofer, asignación automática
(M1), aceptación, seguimiento, entrega con código, cobro, reclamo, módulos M2 a M5 y auditoría. Cada
caso sigue la ficha de la plantilla; el encabezado indica su importancia y el campo Estado, lo que está
construido. Un caso que este documento no expande se nombra por su código, que figura en la lista de la
sección 4.

---

#### Crítico CU-001 — Iniciar Sesión

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-01, OBJ-02, OBJ-05 |
| **Requisitos asociados** | IRQ-01 |
| **Descripción** | El usuario informa su correo y su contraseña desde la aplicación que le corresponde: la del cliente, la del chofer o el panel de administración. El sistema verifica su identidad con el proveedor de identidad y lo deja operando con las funciones de su rol. El sistema no guarda ninguna contraseña ni emite credenciales propias: cada solicitud posterior se vuelve a verificar y el rol del usuario se resuelve en el momento. |
| **Precondición** | El usuario está registrado en el sistema. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El usuario informa su correo y su contraseña en la aplicación que le corresponde. |
| 2 | La aplicación pide al proveedor de identidad que verifique las credenciales. |
| 3 | El proveedor de identidad confirma la identidad del usuario y entrega a la aplicación la constancia de identidad. |
| 4 | La aplicación presenta la constancia al sistema y le pide el usuario de ese correo. |
| 5 | El sistema verifica la constancia, comprueba que la cuenta no esté bloqueada y que el rol del usuario corresponda a la aplicación desde la que opera, y le entrega el usuario con su rol. |
| 6 | La aplicación comprueba que el rol sirva para ella —el panel de administración admite a los administradores y al Administrador General— y deja al usuario operando con las funciones de su rol; el panel mantiene la sesión abierta durante una hora. |

**Postcondición:** El usuario está identificado y opera con las funciones de su rol. El sistema no conserva una sesión propia: cada solicitud se verifica de nuevo.

**Excepciones**

| Paso | Acción |
|------|--------|
| 2 | Si el correo o la contraseña son incorrectos, o el usuario no existe, el proveedor de identidad rechaza el ingreso y la aplicación informa el error. |
| 2 | Si hay un error de red, la aplicación informa «Sin conexión a internet. Verificá tu conexión e intentá de nuevo.» |
| 5 | Si la cuenta está bloqueada, el sistema deniega la solicitud e informa «La cuenta está bloqueada. Comuníquese con la distribuidora.» |
| 5 | Si el usuario no existe en el sistema, o si su rol no corresponde a la aplicación desde la que opera —por ejemplo, un cliente que entra por la aplicación de choferes—, el sistema deniega la solicitud. |
| 5 | Si la constancia de identidad venció o fue revocada, el sistema deniega la solicitud y la aplicación vuelve a pedir el ingreso. |
| 6 | Si el rol del usuario no sirve para la aplicación, esta no abre la sesión; el panel informa «No tenés permisos de administrador». |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 3 | 3 segundos |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Múltiples veces por día por usuario. Varía según la duración de la sesión. |
| **Estabilidad** | Alta |
| **Comentarios** | El sistema depende del proveedor de identidad: si éste no responde, nadie puede ingresar. El ingreso no impide entrar a un chofer no habilitado: la validación que otorga el administrador (CU-032) y la habilitación (CU-033) se exigen cuando el chofer quiere ponerse en línea (CU-022) y al elegirlo como candidato para un pedido. |

---

#### Crítico CU-002 — Registrarse como Cliente

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-01 |
| **Requisitos asociados** | IRQ-01 |
| **Descripción** | Una persona nueva se registra como cliente informando sus datos personales. El sistema crea su cuenta y su perfil de cliente, le envía un correo de bienvenida y le avisa que ya puede iniciar sesión. El registro no abre la sesión y nunca crea un rol distinto del de cliente. |
| **Precondición** | La persona tiene conexión a internet y no tiene una cuenta con el mismo correo ni con el mismo teléfono. |
| **Puntos de extensión** | PE-01: El cliente declara cuánto gas consume por mes, lo extiende CU-143 Declarar el Consumo Promedio al Registrarse. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | La persona elige registrarse como cliente. |
| 2 | Informa su nombre completo, su correo, su teléfono y una contraseña. |
| 3 | El sistema controla que no se estén haciendo demasiados registros desde el mismo origen. |
| 4 | El sistema valida los datos: correo con formato de correo, contraseña de al menos seis caracteres, nombre de al menos dos y teléfono en formato internacional. Rechaza cualquier dato que no forme parte del registro de un cliente, como un rol o una distribuidora. |
| 5 | El sistema controla que el correo y el teléfono estén libres, crea la cuenta de acceso y guarda el usuario con su perfil de cliente, sin validar, en una sola operación. |
| 6 | El sistema informa los datos del usuario creado, con su rol y su perfil. No abre la sesión. |
| 7 | El sistema envía el correo de bienvenida. |

**Postcondición:** Existe un usuario nuevo con rol de cliente, su cuenta de acceso y su perfil de cliente. Todavía no tiene sesión: para realizar pedidos debe iniciar sesión (CU-001).

**Excepciones**

| Paso | Acción |
|------|--------|
| 3 | Si el origen superó el máximo de registros por minuto, el sistema rechaza la solicitud y pide reintentar más tarde. |
| 4 | Si falta algún dato, no tiene el formato esperado o sobra alguno, el sistema rechaza el registro e indica el campo. |
| 5 | Si el correo o el teléfono ya están en uso, el sistema informa «Email o teléfono ya en uso» e invita a iniciar sesión. La cuenta existente no se modifica. |
| 5 | Si el proveedor de identidad rechaza la cuenta, el sistema informa el motivo y no crea nada. |
| 5 | Si no se puede guardar el usuario, el sistema deshace el registro y no deja ninguna cuenta a medias. |
| 7 | Si el envío del correo de bienvenida falla, el registro queda hecho igual. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 6 | 5 segundos |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Una vez por cliente, en el alta. A nivel del sistema, varias veces por día según el ritmo de registros nuevos. |
| **Estabilidad** | Alta |
| **Comentarios** | El sistema no inicia la sesión del usuario recién registrado: la aplicación encadena el inicio de sesión por su cuenta. El cliente puede declarar cuánto gas consume por mes al registrarse (CU-143); si no lo hace, el registro sigue igual. |

---

#### Crítico CU-005 — Crear un Pedido

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-01, OBJ-02, OBJ-06, OBJ-07 |
| **Requisitos asociados** | IRQ-02, IRQ-04, IRQ-05, IRQ-07, IRQ-08, IRQ-10 |
| **Descripción** | El cliente —o el administrador, por teléfono y a nombre de un cliente— elige productos, cantidades, dirección de entrega y medio de pago, y confirma el pedido. El sistema verifica la cobertura de la dirección, reserva el stock y el cupo de la franja de forma conjunta —o no reserva nada—, calcula el total con las promociones y los recargos, registra el pedido y, salvo que el pago sea por MercadoPago, lo ofrece a un chofer. Opcionalmente, el cliente agenda la entrega en una franja horaria (CU-044) o elige la modalidad express (CU-148). La reserva con fecha agendada y seña no es parte de este caso: es CU-072. |
| **Precondición** | El solicitante —el cliente o un administrador— está identificado. Existe al menos un producto activo con stock en la distribuidora elegida y el cliente tiene una dirección de entrega registrada. |
| **Puntos de extensión** | PE-02: El cliente quiere agendar la entrega en una franja horaria, lo extiende CU-044 Seleccionar una Franja Horaria al Crear un Pedido. PE-03: El cliente puede elegir la modalidad express, lo extiende CU-148 Elegir la Modalidad de Entrega del Pedido. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El cliente consulta el catálogo de la distribuidora (CU-041). Si el pedido lo carga el administrador por teléfono, el administrador indica además a qué cliente pertenece. |
| 2 | Elige uno o más productos e indica la cantidad de cada uno: en la aplicación del cliente los suma al carrito (CU-122 a CU-126) y el pedido sale de ese carrito; el administrador los arma directamente en el pedido. Para ver el precio, el sistema le cotiza el pedido (CU-302) cada vez que cambia algo que lo afecta: el total que se muestra lo calcula el sistema, no la aplicación. |
| 3 | Elige la dirección de entrega entre las que tiene guardadas. |
| 4 | Si quiere agendar la entrega, elige una fecha y una franja horaria disponible (CU-044, punto de extensión PE-02). |
| 5 | Elige el medio de pago: efectivo, MercadoPago o transferencia; el administrador puede cargarlo además a cuenta corriente (CU-236). Con MercadoPago o con transferencia el sistema agrega un recargo del 10 %; el pago en efectivo no lleva recargo. |
| 6 | Revisa el resumen —ítems, descuentos, subtotal, recargos y total— y confirma. Si la aplicación acompaña el envío con una clave que identifica el intento y la conexión se corta y reintenta, el sistema no crea un segundo pedido. |
| 7 | El sistema comprueba que el pedido se cree a nombre del propio cliente; un administrador sí puede cargarlo a nombre de un cliente. |
| 8 | El sistema verifica que la dirección sea del cliente y esté dentro de una zona de cobertura de la distribuidora, y toma el recargo de esa zona. Si la distribuidora no definió zonas, o la dirección no tiene ubicación, no controla la cobertura. |
| 9 | Si el pedido trae fecha y franja, el sistema reserva el cupo de la franja elegida; si trae franja sin fecha, solo comprueba que la franja exista y esté activa. Por cada ítem, comprueba que el producto sea de la distribuidora y que alcance el stock, lo descuenta y le aplica las promociones por volumen, tomando siempre el precio del sistema y nunca el que informa el cliente. |
| 10 | El sistema suma al total el recargo de la zona y, si el pago es en línea, el recargo del 10 %. |
| 11 | El sistema registra el pedido y sus ítems como pendiente y deja asentada la creación en el historial de estados del pedido. Si el pedido salió del carrito, lo vacía en la misma operación. |
| 12 | Si el pago es en efectivo, por transferencia o a cuenta corriente, el sistema ofrece el pedido a un chofer (CU-013). Si es por MercadoPago, genera el enlace de cobro y no ofrece el pedido a nadie hasta que se confirme el cobro. |
| 13 | El sistema avisa al cliente que el pedido fue creado y avisa del alta al panel de administración. |
| 14 | El cliente ve el seguimiento del pedido. |

**Postcondición:** Existe un pedido pendiente. El stock de cada ítem y el cupo de la franja se descontaron juntos con el alta. Si el pedido salió del carrito, el carrito quedó vacío. Salvo en pago con MercadoPago, el pedido quedó ofrecido a un chofer.

**Excepciones**

| Paso | Acción |
|------|--------|
| 4 | Si el pedido trae una fecha agendada anterior a hoy, con franja o sin ella, el sistema lo rechaza e informa que la fecha agendada no puede ser pasada. |
| 4 | Si la franja elegida no existe o está inactiva, el sistema rechaza el pedido e informa «Franja horaria inválida o inactiva». |
| 6 | Si se reintenta el mismo pedido con datos distintos, el sistema lo rechaza y no ejecuta la operación. |
| 6 | Si el pedido no trae ningún ítem, el sistema lo rechaza e informa «El pedido necesita al menos un renglón»; si repite la misma garrafa en dos renglones, lo rechaza y pide sumar las cantidades en uno solo. El panel lo avisa antes de enviar («Esta garrafa ya está en otro renglón: sumá las cantidades en uno solo»). |
| 6 | Si el pedido sale del carrito y además trae ítems, el sistema lo rechaza: con el carrito, los ítems son los del carrito. |
| 6 | Si el pedido express trae también franja horaria o fecha agendada, el sistema lo rechaza: el express no se agenda. |
| 7 | Si un cliente intenta crear un pedido a nombre de otro cliente, el sistema deniega la operación. |
| 7 | Si el pedido sale del carrito y quien lo crea no es el cliente, el sistema deniega la operación. |
| 8 | Si el cliente no existe, el sistema cancela la operación e informa «Cliente no encontrado». |
| 8 | Si la dirección no existe o no es del cliente, el sistema cancela la operación e informa «Dirección no encontrada». |
| 8 | Si la dirección está fuera de todas las zonas de cobertura de la distribuidora, el sistema rechaza el pedido antes de tocar el stock. |
| 8 | Si el pedido es express y la modalidad dejó de estar disponible para esa dirección, el sistema rechaza el pedido, informa el motivo y deja que el cliente lo haga con franja horaria. |
| 9 | Si la franja elegida no tiene cupo para esa fecha, el sistema cancela la operación y rechaza el pedido. |
| 9 | Si la franja elegida es de hoy y ya terminó, el sistema rechaza el pedido e informa «La franja ya terminó, elegí otra». |
| 9 | Si algún producto del pedido no existe, el sistema cancela la operación e informa «Garrafa no encontrada», con el producto. |
| 9 | Si el stock de algún ítem es menor que la cantidad pedida, el sistema cancela la operación e informa «Stock insuficiente para <producto>». El pedido no se crea y el inventario no cambia. |
| 9 | Si algún producto no pertenece a la distribuidora del pedido, el sistema cancela la operación e informa «La garrafa <producto> no pertenece a la distribuidora seleccionada». |
| 9 | Si dos pedidos simultáneos compiten por el mismo stock, el sistema deshace y reintenta la operación completa; si agotados los reintentos sigue el choque, informa un conflicto y el pedido no se crea. |
| 9 | Ante cualquier otro error, el sistema cancela la operación e informa «Error al crear el pedido». |
| 12 | Si no hay ningún chofer elegible, el pedido queda pendiente sin oferta y lo retoma la re-oferta automática (CU-014). |
| 13 | Si falla el envío del aviso, el pedido queda creado igual. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 11 | 5 segundos |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Variable según la demanda de la distribuidora (estimado: 10 a 50 pedidos por día en la Fase 1). |
| **Estabilidad** | Alta |
| **Comentarios** | Los totales se calculan con aritmética decimal exacta y las promociones se aplican según la cantidad mínima configurada en cada producto. Si ningún chofer resulta elegible, el pedido queda pendiente en silencio: el cliente no ve ninguna diferencia. El sistema no restringe la creación de pedidos a los clientes: cualquier usuario identificado puede crear uno, aunque un cliente solo puede hacerlo para sí mismo, y solo el administrador puede cargarlo a cuenta corriente. El proceso de compra con carrito persistente (CU-122 a CU-126), la elección explícita de modalidad (CU-148) y la compra express en un paso (CU-147) están construidos: la aplicación del cliente crea siempre el pedido desde el carrito, y el administrador lo arma con los ítems en el propio pedido; también puede recibir la modalidad de entrega y quién va a recibir el pedido (CU-128). Tampoco usa CU-121: el cliente elige la dirección de una lista completa que ya trae marcada la predeterminada. La reserva con fecha agendada y seña pasa por la misma operación de alta pero es otro caso de uso, con su propia secuencia (CU-072). La protección contra pedidos duplicados depende de la clave que identifica cada intento y que acompaña el envío: la aplicación del cliente la envía y el panel no. El total que guarda el sistema es la suma exacta de los renglones, el recargo de la zona, el recargo del medio de pago en línea —que se guarda aparte— y, si corresponde, el de la entrega express; la base de datos rechaza un pedido cuyo total no coincida con esa suma y no admite la misma garrafa en dos renglones del mismo pedido. |

---

#### Importante CU-008 — Cancelar un Pedido (Cliente)

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-01, OBJ-06 |
| **Requisitos asociados** | IRQ-02, IRQ-04 |
| **Descripción** | El cliente cancela un pedido propio que todavía no salió hacia su domicilio. El sistema marca el pedido como cancelado, restituye el stock de todos sus ítems al inventario y avisa a quienes corresponda. |
| **Precondición** | El cliente está identificado. El pedido es suyo. |
| **Puntos de extensión** | PE-04: El pedido cancelado tiene un pago aprobado por una pasarela, lo extiende CU-168 Reintegrar el Pago de un Pedido. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El cliente abre el detalle del pedido y elige cancelarlo. |
| 2 | Indica el motivo de la cancelación, que es obligatorio. Si la solicitud se repite por un corte de conexión, el sistema no vuelve a procesarla. |
| 3 | El sistema comprueba, en este orden, que el pedido pertenezca al cliente, que no esté ya entregado ni cancelado y que no esté en camino. |
| 4 | El sistema marca el pedido como cancelado con el motivo recibido y asienta el cambio en el historial de estados del pedido. |
| 5 | En la misma operación, el sistema devuelve al inventario la cantidad de cada ítem del pedido. |
| 6 | El sistema confirma juntos el cambio de estado y la restitución del stock. |
| 7 | El sistema avisa al cliente de la cancelación, con el motivo y quién canceló, avisa al panel de administración y, si había chofer asignado, le avisa que ya no hace falta ir. |
| 8 | Si el pedido tenía un pago aprobado por una pasarela, el sistema lo reintegra (CU-168, punto de extensión PE-04). |

**Postcondición:** El pedido está cancelado, con su motivo. El stock de todos los ítems fue restituido. Las dos cosas se confirmaron juntas: dos cancelaciones simultáneas no devuelven el stock dos veces. Si el pedido estaba pagado por una pasarela, el pago se devolvió (CU-168).

**Excepciones**

| Paso | Acción |
|------|--------|
| 3 | Si el pedido no existe, el sistema informa que no lo encontró. |
| 3 | Si el pedido no es del cliente, o es de una distribuidora distinta de la que el cliente tiene elegida, el sistema informa que no lo encontró, sin revelar que existe. Este control se hace antes de mirar el estado. |
| 3 | Si el pedido ya está entregado o cancelado, el sistema informa «No se puede cancelar un pedido finalizado». |
| 3 | Si el pedido ya está en camino, el sistema informa «El pedido ya está en camino. Contacte al soporte.» |
| 2 | Si se reintenta la misma solicitud con datos distintos, el sistema la rechaza y no la ejecuta. |
| 2 | Si el motivo falta, el sistema rechaza la cancelación e informa «Para cancelar el pedido hay que indicar el motivo»; si son sólo espacios, la rechaza e informa que el motivo no puede estar vacío; el motivo admite hasta 500 caracteres. El panel pide el motivo antes de enviar: «Escribí el motivo de la cancelación». |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 6 | 3 segundos |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Baja: solo cuando el cliente necesita cancelar un pedido de manera excepcional. |
| **Estabilidad** | Alta |
| **Comentarios** | La cancelación del cliente (CU-008) y la del administrador (CU-010) comparten el mismo comportamiento del sistema —cancelan el pedido y restituyen el stock—; lo que cambia es el actor. La liberación del chofer (CU-009) es otra cosa: el pedido vuelve a pendiente y no se restituye stock. El aviso a la aplicación del chofer viaja solo por la conexión en tiempo real: un chofer con la aplicación cerrada puede no enterarse. Los vencimientos automáticos (CU-076 y CU-077) no emiten el aviso en vivo: el cliente se entera al ver el pedido (CU-006). Un chofer que «cancela» no cancela: libera el pedido a pendiente (CU-009). El motivo es obligatorio en tres capas: el formulario de cancelación del panel, el sistema y la base de datos, que no admite un pedido cancelado sin motivo; las cancelaciones automáticas por vencimiento dejan el suyo. |

---

#### Crítico CU-022 — Activar la Disponibilidad

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-02 |
| **Requisitos asociados** | IRQ-03 |
| **Descripción** | El chofer indica que está disponible para recibir pedidos. El sistema comprueba que esté habilitado y validado y guarda su disponibilidad. Es la misma operación que desactivarla (CU-266), con el valor en verdadero. |
| **Precondición** | El usuario está identificado como chofer o administrador y el chofer indicado tiene perfil de repartidor. Un chofer solo cambia su propia disponibilidad; un administrador, la de los choferes de su distribuidora. Para ponerse disponible, el chofer está habilitado por el administrador (CU-033) y validado (CU-032). |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El chofer enciende su disponibilidad desde la pantalla principal de su aplicación. |
| 2 | La aplicación informa el valor deseado —disponible—: no pide alternar el valor actual sino el que debe quedar. |
| 3 | El sistema busca el perfil de repartidor de ese usuario. |
| 4 | El sistema comprueba que el chofer esté habilitado y validado y guarda su disponibilidad. |
| 5 | El sistema no hace nada sobre el seguimiento de posiciones: el chofer reaparece cuando su aplicación informa la siguiente posición (CU-017). |
| 6 | El sistema informa el nuevo estado de disponibilidad para que la aplicación lo muestre. |

**Postcondición:** El chofer quedó disponible. Empieza a recibir ofertas recién cuando su aplicación informa su primera posición.

**Excepciones**

| Paso | Acción |
|------|--------|
| 2 | Si quien pide es otro chofer, el sistema deniega la operación e informa «No podés cambiar la disponibilidad de otro chofer»; si es un cliente, también la deniega. |
| 2 | Si el usuario no tiene perfil de repartidor, o es de otra distribuidora que la del administrador, el sistema informa «Perfil de repartidor no encontrado para este usuario». |
| 4 | Si el chofer está deshabilitado o sin validar, el sistema deniega la operación y no cambia nada. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 4 | 1 segundo |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Alta por chofer: al empezar el turno o al volver de una pausa. |
| **Estabilidad** | Alta |
| **Comentarios** | La operación es del propio chofer, o del administrador sobre los choferes de su distribuidora: un chofer no puede cambiar la disponibilidad de otro. Ponerse en línea exige habilitación y validación. Estar disponible no reincorpora al chofer al despacho: reaparece con la siguiente posición que informe su aplicación (CU-017) y hasta entonces no recibe ofertas. |

---

#### Crítico · automático CU-013 — Asignar un Pedido Automáticamente por Proximidad

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-02 |
| **Requisitos asociados** | IRQ-02, IRQ-03 |
| **Descripción** | Al crearse un pedido, el sistema ofrece el pedido a un solo chofer por vez: el más cercano al domicilio de entrega que todavía no haya sido contactado, con un plazo acotado para aceptar. La oferta queda registrada de forma durable, de modo que sobrevive a un reinicio del servidor y queda auditable. |
| **Precondición** | Existe un pedido pendiente sin chofer asignado, con sus coordenadas de entrega. Al menos un chofer de la misma distribuidora está presente en el seguimiento de posiciones. |
| **Estado** | Implementado, con funcionalidad planificada: admitir como candidatos a los choferes que están por terminar su entrega (paso 3.a). La verificación de la carga de camión (CU-248) y la de la situación laboral del chofer (CU-246) están implementadas. |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El sistema recibe el aviso de que se creó un pedido, una vez confirmada su alta. |
| 2 | El sistema recupera los choferes a los que ya se les ofreció este pedido, para no contactarlos de nuevo. |
| 3 | El sistema lee los parámetros del despacho de la distribuidora (CU-171) y busca el siguiente candidato recorriendo los pasos de radio de menor a mayor —por omisión 5, 10, 15 y 20 km—: toma los choferes presentes, ordenados por cercanía, solo los de la distribuidora del pedido, y descarta a los ya contactados, a los que no tienen un vehículo en uso, a los que tienen vencida la licencia o la documentación del vehículo (CU-161, CU-136 a CU-138), a los que no pueden recibir pedidos según su carga de camión abierta y a los que no están habilitados laboralmente. Se queda con el primero que aparece. |
| 4 | Planificado, sin iteración asignada: entre los candidatos el sistema admite tanto a los choferes libres como a los que están por terminar su entrega en curso, pero descarta a los que están en pleno recorrido. Así un chofer que entrega la última garrafa puede recibir el pedido siguiente sin un hueco muerto entre uno y otro. |
| 5 | El sistema registra la oferta a nombre de ese chofer, con su vencimiento fijado en la ventana de aceptación de la distribuidora (30 segundos por omisión). |
| 6 | El sistema le avisa al chofer en tiempo real, con el detalle del pedido y la hora en que la oferta pierde vigencia. |
| 7 | El sistema le envía además una notificación al dispositivo, por si tiene la aplicación cerrada. El envío no frena el proceso. |

**Postcondición:** Existe una oferta vigente a nombre de un único chofer. El pedido sigue pendiente hasta que ese chofer la acepte, la rechace o la deje vencer.

**Excepciones**

| Paso | Acción |
|------|--------|
| 3 | Si ningún paso de radio arroja un candidato nuevo, el sistema no emite ninguna oferta y el pedido queda a la espera. Avisa a los administradores de la distribuidora, una sola vez por agotamiento, si no hay choferes elegibles en el radio o si los que había rechazaron o esperan una re-oferta. El proceso de CU-014 lo reintenta cuando aparezcan choferes disponibles. |
| 3 | Si el pedido no tiene punto de entrega, no hay contra qué medir la cercanía: no se emite oferta y se avisa a los administradores. |
| 3 | Si los únicos choferes cercanos son de otra distribuidora, quedan descartados: un chofer nunca recibe ofertas de una empresa que no es la suya. |
| 3 | Si el chofer no tiene un vehículo en uso, o su licencia o ese vehículo tienen documentación vencida, queda descartado y la oferta pasa al siguiente. |
| 3 | Si el chofer tiene una carga de camión que no está en ruta, o su vehículo en uso no es el de la carga, o no tiene carga y la distribuidora exige tenerla (CU-249), queda descartado y la oferta pasa al siguiente. |
| 7 | Si falla el envío de la notificación al dispositivo, el proceso sigue: la oferta ya fue registrada y el aviso en tiempo real ya se emitió. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 5 | 1 segundo |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Una vez por cada pedido creado, y de nuevo por cada rechazo o vencimiento. |
| **Estabilidad** | Alta |
| **Comentarios** | Para recibir ofertas, un chofer tiene que estar presente en el seguimiento de posiciones, pertenecer a la distribuidora del pedido, estar habilitado por el administrador y validado, y pasar la regla de flota: sin vehículo en uso, o con la licencia o la documentación del vehículo vencida, no recibe ninguna oferta. La habilitación que otorga el administrador (CU-032 y CU-033) y que retira (CU-271 y CU-267) tiene así efecto sobre el despacho. Un chofer entra al seguimiento al emitir su posición y sale al apagar su disponibilidad o al desconectarse; estar presente significa tener la aplicación abierta y reportando su posición. Ofrecer a un único chofer por vez, en lugar de difundir a todos, es el núcleo del módulo inteligente M1. |

---

#### Crítico · automático CU-014 — Vencer la Oferta y Ofrecer al Siguiente Chofer

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-02 |
| **Requisitos asociados** | IRQ-02, IRQ-03 |
| **Descripción** | Un proceso automático revisa cada pocos segundos las ofertas cuya ventana de aceptación ya pasó. Las da por vencidas y, si el pedido sigue sin chofer, lo ofrece al siguiente candidato. También reingresa al circuito los pedidos pendientes que quedaron sin ninguna oferta activa. |
| **Precondición** | Existe al menos una oferta vencida, o un pedido pendiente sin oferta vigente. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El proceso se ejecuta automáticamente en un ciclo corto y fijo. |
| 2 | El sistema se asegura de que solo una instancia lo ejecute a la vez y decide a qué distribuidoras les toca el ciclo según el intervalo de cada una (CU-173); las demás esperan el suyo. |
| 3 | El sistema obtiene las ofertas cuya vigencia expiró y marca cada una como vencida. |
| 4 | El sistema vuelve a leer el pedido, porque pudo haber sido aceptado o cancelado por otra vía mientras la oferta corría. |
| 5 | Si el pedido sigue pendiente y sin chofer, el sistema ejecuta CU-013 para ofrecerlo al siguiente candidato. |
| 6 | Además, por cada distribuidora, el sistema toma hasta cincuenta pedidos pendientes sin oferta vigente y con más de un minuto de antigüedad —los recién creados ya fueron ofrecidos al crearse— y les abre una oferta sin pisar las que estén en curso. |

**Postcondición:** Ninguna oferta vencida permanece abierta. Cada pedido pendiente tiene a lo sumo una oferta vigente.

**Excepciones**

| Paso | Acción |
|------|--------|
| 4 | Si el pedido ya fue aceptado o cancelado, no se vuelve a ofrecer y el ciclo continúa con la oferta siguiente. |
| 5 | Si no quedan candidatos nuevos en ningún paso de radio, el pedido queda a la espera hasta la próxima ejecución. |
| 3 | Si la ejecución falla, el error se registra y la ejecución siguiente puede retomar el trabajo. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 1 | Ciclo automático de 15 segundos |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Automático: ciclo fijo de 15 segundos; cada distribuidora lo recibe con su propio intervalo. |
| **Estabilidad** | Alta |
| **Comentarios** | Con varias instancias del sistema corriendo, solo una procesa cada ciclo. El barrido de pendientes está acotado a cincuenta pedidos por ciclo y por distribuidora: con una cola mayor se drena de a cincuenta, y ninguna distribuidora tapa a otra. El rechazo explícito del chofer no espera a este proceso: cierra la oferta y dispara la siguiente de inmediato. Cuando se agotan los candidatos, el sistema avisa a los administradores de la distribuidora, una sola vez por agotamiento (CU-013), y el pedido permanece pendiente. Los pasos de radio y la ventana de aceptación se leen de la configuración de la distribuidora (CU-171) y el intervalo del ciclo, de CU-173. |

---

#### Crítico CU-015 — Aceptar un Pedido

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-02, OBJ-03 |
| **Requisitos asociados** | IRQ-02, IRQ-03 |
| **Descripción** | El chofer acepta el pedido que se le ofreció. El sistema se lo asigna, genera el código de entrega, de seis dígitos, que se usará en la confirmación por código (CU-079), cierra la oferta y avisa al cliente. |
| **Precondición** | El chofer está identificado y conectado. El pedido está pendiente. El chofer está habilitado por el administrador y validado, tiene un vehículo en uso (CU-161) y ni su licencia ni ese vehículo tienen documentación vencida (CU-136 a CU-138). |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El chofer recibe la oferta del pedido y elige «Aceptar». |
| 2 | El sistema toma la identidad del chofer de su sesión e ignora cualquier otro identificador de repartidor que venga en el pedido; un administrador sí puede indicar a qué chofer asignarlo. |
| 3 | Si quien acepta es un chofer y el pedido ya tiene un chofer asignado, el sistema comprueba que sea él mismo. Luego comprueba que el pedido siga pendiente. |
| 4 | El sistema comprueba que quien acepta tenga perfil de repartidor, sea de la distribuidora del pedido, esté habilitado y validado y tenga un vehículo en uso habilitado (CU-161), y que esté habilitado laboralmente. |
| 5 | El sistema comprueba que la carga de camión del chofer que queda con el pedido lo habilite a recibir pedidos. Solo se saltea cuando el mismo chofer repite una aceptación que ya era suya. |
| 6 | El sistema le asigna el pedido, lo pasa a aceptado, asienta el cambio en el historial de estados, registra el momento, guarda en el pedido una copia de la patente, la marca y el modelo del vehículo del chofer y genera el código secreto de entrega. |
| 7 | El sistema cierra como aceptada la oferta que ese chofer tenía abierta sobre el pedido. |
| 8 | En la misma operación, el sistema retira las ofertas abiertas a los demás choferes, que no cuentan como intento, y después les avisa que la oferta ya no está vigente. |
| 9 | El sistema avisa al cliente en tiempo real de la aceptación, con el nombre y el teléfono del chofer, y avisa al panel de administración. |
| 10 | El sistema envía al cliente una notificación al dispositivo, con el texto genérico de confirmación de pedido, que no menciona la aceptación ni al chofer. |

**Postcondición:** El pedido está aceptado por el chofer, con su código de entrega generado. Las ofertas abiertas a otros choferes quedaron retiradas.

**Excepciones**

| Paso | Acción |
|------|--------|
| 3 | Si el pedido no existe, el sistema informa que no lo encontró. |
| 3 | Si el pedido es de otra distribuidora que la de quien acepta, el sistema informa que no lo encontró, sin revelar que existe. |
| 3 | Si el pedido está entregado o cancelado, el sistema rechaza la operación por transición no permitida. |
| 3 | Si el pedido ya tiene asignado a otro chofer, el sistema rechaza la aceptación e informa «Este pedido no está asignado a tu usuario», antes de mirar la transición: una aceptación tardía no desplaza al chofer que ya lo tomó. Este control no alcanza al administrador, que puede reasignar indicando otro chofer. |
| 3 | Si el mismo chofer que ya tiene el pedido vuelve a aceptarlo, la operación no falla y no cambia nada: conserva el código de entrega y el momento de aceptación. |
| 4 | Si quien acepta no tiene perfil de repartidor, o es de otra distribuidora que la del pedido, el sistema informa que no encontró al repartidor. |
| 4 | Si el chofer está deshabilitado, el sistema informa «El repartidor está deshabilitado»; si no está validado, «El repartidor no está validado». |
| 4 | Si el chofer no tiene un vehículo en uso, o su licencia o ese vehículo tienen documentación vencida, el sistema rechaza la aceptación e informa «No se puede asignar: …» con el motivo. Un chofer sin vehículo en uso tampoco recibe la oferta (CU-013). |
| 5 | Si el chofer no puede recibir pedidos por su carga de camión, el sistema rechaza la aceptación e informa el motivo —por ejemplo «Tu distribuidora exige una carga de camión abierta para trabajar: pedile al administrador que abra tu carga del día»—. |
| 1 | Si el solicitante es el Administrador General y no indica la distribuidora, el sistema rechaza la operación e informa que falta indicar la distribuidora. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 6 | 3 segundos |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Alta por chofer: se repite cada vez que le llega una oferta, varias veces por jornada. |
| **Estabilidad** | Alta |
| **Comentarios** | La copia del vehículo queda en el pedido aunque el vehículo se reasigne después, de modo que el historial no cambia; si el pedido vuelve a pendiente, la copia se borra junto con el chofer asignado. Un segundo chofer no puede quedarse con un pedido ajeno. Al cliente le llega siempre el mensaje de confirmación de pedido: el mensaje propio de cada estado está escrito pero no se usa. Cuando hay una carga de camión (C-09, implementado), antes de aceptar el sistema verifica que el chofer pueda recibir pedidos según esa carga. |

---

#### Crítico · automático CU-017 — Modificar la Ubicación GPS del Chofer

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-02, OBJ-03 |
| **Requisitos asociados** | IRQ-03 |
| **Descripción** | Mientras el chofer está en línea, su aplicación informa la posición del dispositivo. El sistema la registra para que el despacho pueda encontrarlo y, si el chofer está entregando un pedido, la reenvía al cliente de ese pedido y al panel, junto con cuánto falta para llegar. |
| **Precondición** | El chofer está identificado y conectado en tiempo real. El dispositivo tiene el GPS activo y los permisos de ubicación concedidos. |
| **Estado** | Implementado, con funcionalidad planificada (C-10): el cálculo del tiempo estimado de llegada (pasos 6 y 7). |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | La aplicación del chofer detecta un desplazamiento de al menos diez metros y emite una nueva posición, tanto desde el inicio como desde la pantalla del pedido que lleva: el sistema necesita esa posición para trazar la ruta del pedido (CU-303). |
| 2 | La aplicación informa la posición, con la latitud y la longitud. |
| 3 | El sistema recibe el mensaje y recuerda de qué chofer es la conexión, para poder retirarlo del seguimiento cuando se desconecte. |
| 4 | El sistema registra la posición en el seguimiento de choferes, que es la fuente que consulta el despacho (CU-013). |
| 5 | El sistema consulta si ese chofer tiene un pedido en curso. El vínculo entre chofer y pedido se crea al pasar el pedido a en camino y se borra al confirmarse la entrega. |
| 6 | Si lo tiene, el sistema calcula cuánto falta para llegar al domicilio —distancia restante y tiempo estimado— y reenvía la posición con ese dato al cliente del pedido, para que actualice el mapa de seguimiento, y al panel de administración. |
| 7 | El tiempo estimado no se recalcula en cada posición: se reutiliza el último mientras siga vigente y se rehace solo cuando pasó un intervalo o el chofer se movió lo suficiente. |

**Postcondición:** La posición del chofer está actualizada y el despacho puede encontrarlo. Si el chofer está entregando, el cliente y el panel ven la posición nueva y cuánto falta para que llegue.

**Excepciones**

| Paso | Acción |
|------|--------|
| 2 | Si falta el chofer o alguna de las dos coordenadas, el sistema registra el error y descarta el mensaje. Las coordenadas de valor cero son válidas. |
| 2 | Si se interrumpe la conexión en tiempo real, la aplicación reintenta la reconexión automáticamente. |
| 5 | Si el chofer no tiene ningún pedido en curso, la posición se guarda igual pero no se reenvía a nadie. |
| 6 | Si no se puede calcular el tiempo estimado, la posición se reenvía igual, sin ese dato: el cliente sigue viendo el mapa moverse. El seguimiento nunca se interrumpe por no poder estimar. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 4 | 100 milisegundos |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Cada vez que el GPS detecta un desplazamiento de diez metros o más mientras el chofer está en línea. |
| **Estabilidad** | Alta |
| **Comentarios** | La posición se guarda solo en memoria para que la búsqueda por cercanía sea rápida: como contrapartida, no queda historial de recorridos. De quién es la posición lo decide la sesión del chofer, no el mensaje: un chofer indicado dentro del mensaje se ignora. El sistema no valida que las coordenadas estén en rango: un par imposible no se guarda, pero el chofer no se entera. El tiempo estimado se agrega al aviso que ya existía y no es un caso de uso aparte: el cliente no lo pide, lo recibe con la posición. Se calcula en el sistema y se reutiliza a propósito, porque rehacerlo en cada posición significaría una consulta externa por cada movimiento de cada chofer, sin aportar precisión: entre dos posiciones separadas por diez metros el tiempo estimado es el mismo. |

---

#### Crítico CU-078 — Consultar el Código de Entrega (QR del chofer)

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-04 |
| **Requisitos asociados** | IRQ-02 |
| **Descripción** | El chofer obtiene el código de entrega del pedido que está llevando, de seis dígitos, para mostrarlo como QR al cliente al llegar; debajo del QR figura el mismo número, grande y agrupado («482 913»), para dictarlo. El código se genera al aceptarse el pedido y es la mitad emisora del mecanismo antifraude que se completa en CU-079. Con el pedido en camino, el chofer asignado —o un administrador— también puede generar un código nuevo si el actual se compartió o el cliente agotó sus intentos. |
| **Precondición** | El solicitante está identificado como chofer, o como administrador. El pedido existe y ya fue aceptado, por lo que tiene código de entrega. Si es un chofer, es el asignado al pedido. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El chofer abre el detalle del pedido que está por entregar y pide el QR de entrega. |
| 2 | El sistema verifica el identificador del pedido y lo recupera. |
| 3 | Si el solicitante es un chofer, el sistema comprueba que el pedido esté asignado a él. |
| 4 | El sistema verifica que el pedido tenga código de entrega. |
| 5 | El sistema muestra el código del pedido. |
| 6 | La aplicación del chofer muestra el código como QR y, debajo, en grande y agrupado de a tres dígitos, para dictarlo. |
| 7 | Si hace falta otro código, el chofer elige «Generar código nuevo» y confirma. |
| 8 | El sistema verifica que el pedido esté en camino y que sea del chofer que lo pide (o que lo pida un administrador). |
| 9 | El sistema reemplaza el código anterior por uno nuevo, pone en cero los intentos fallidos del cliente y deja el hecho asentado en la auditoría, sin guardar el valor del código. |
| 10 | La aplicación del chofer muestra el código nuevo al instante. |

**Postcondición:** El chofer dispone del código de seis dígitos del pedido y lo muestra como QR o lo dicta. Consultarlo no cambia el pedido. Si generó uno nuevo, el anterior dejó de valer, el cliente vuelve a tener todos sus intentos y el pedido deja de estar bloqueado, si lo estaba.

**Excepciones**

| Paso | Acción |
|------|--------|
| 2 | Si el identificador no es válido, el sistema rechaza la consulta. |
| 2 | Si el pedido no existe, el sistema informa «Order with ID: … not found». |
| 2 | Si el pedido es de otra distribuidora que la del solicitante, el sistema informa lo mismo, sin revelar que existe. |
| 3 | Si el chofer no tiene perfil de repartidor o el pedido no está asignado a él, el sistema deniega la consulta e informa «Este pedido no está asignado a tu usuario». |
| 4 | Si el pedido todavía no fue aceptado y por lo tanto no tiene código, el sistema informa «El pedido todavía no tiene código de entrega (debe estar aceptado)». |
| 1 | Si el solicitante es un cliente, el sistema deniega la consulta: el cliente nunca conoce el código por el sistema, solo escaneando el QR que muestra el chofer. |
| 8 | Si el pedido está asignado a otro chofer, el sistema deniega la operación e informa «Este pedido no está asignado a tu usuario». |
| 8 | Si el pedido no está en camino, el sistema rechaza la generación del código nuevo. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 5 | 1 segundo |
| 9 | 1 segundo |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Una vez por cada pedido que llega al domicilio; el chofer puede repetirla si la pantalla se cierra. Generar un código nuevo es excepcional. |
| **Estabilidad** | Alta |
| **Comentarios** | Consultar el código no lo cambia, por mucho que el chofer lo pida: es siempre el mismo hasta que el chofer o un administrador genere uno nuevo, para que el QR mostrado sea estable durante todo el trayecto. Los códigos de pedidos que ya estaban en curso, con otro formato, siguen valiendo hasta que se genere uno nuevo. |

---

#### Crítico CU-079 — Confirmar una Entrega Escaneando el QR (cliente)

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-03, OBJ-04, OBJ-07 |
| **Requisitos asociados** | IRQ-02, IRQ-08 |
| **Descripción** | El cliente escanea con su aplicación el QR que le muestra el chofer —o escribe a mano los seis dígitos que el chofer le dicta, con un teclado numérico—; si el código coincide con el guardado en el pedido, el sistema da la entrega por realizada. Es el camino normal de cierre de la entrega y la prueba antifraude: el chofer no puede cerrarla (CU-020 es del administrador) y, como el cliente solo puede conocer el código habiendo visto el QR en la mano del chofer, la confirmación prueba que el chofer estuvo presente. Cada código incorrecto del cliente cuenta como un intento: al quinto, el pedido queda bloqueado hasta que el chofer o un administrador genere un código nuevo (CU-078). Si el cliente no puede confirmar, un administrador puede confirmar con el mismo código, que consigue con CU-078, dejando el motivo por escrito. |
| **Precondición** | El solicitante está identificado como el cliente titular del pedido o como administrador (el Administrador General indica la distribuidora). El pedido está en camino y tiene código de entrega desde su aceptación (CU-015) o su asignación manual (CU-012). El chofer está en el domicilio mostrando el QR. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El chofer llega al domicilio y muestra en su aplicación el QR obtenido con CU-078. |
| 2 | El cliente lo escanea con su aplicación, que lee el código de seis dígitos; si no puede escanear, escribe los seis dígitos que el chofer le dicta, con el teclado numérico. |
| 3 | La aplicación envía el código. Si se repite el envío por un corte de conexión, el sistema no lo procesa dos veces. |
| 4 | El sistema recupera el pedido y comprueba la pertenencia: si el solicitante es un cliente, el pedido es suyo. |
| 5 | El sistema verifica que el pedido esté en camino. |
| 6 | El sistema comprueba que el pedido no esté bloqueado y compara el código recibido con el guardado, de una forma que no da pistas sobre cuán cerca estuvo el intento. Si el código es incorrecto y lo envió un cliente, suma un intento fallido; el administrador no suma intentos. |
| 7 | Con el código válido, el sistema pasa el pedido a entregado con el mismo comportamiento que CU-020, registra el momento y asienta el cambio en el historial de estados. Si confirma un administrador, el sistema exige el motivo (de 10 a 500 caracteres) y lo guarda en el historial de estados y en la auditoría; para el cliente no se pide. |
| 8 | Si el medio de pago es efectivo, el pago sigue pendiente: la entrega no lo marca como cobrado. |
| 9 | El sistema corta el seguimiento en vivo del chofer que entregó. |
| 10 | El sistema pasa los envases despachados en el pedido al estado «con el cliente», de mejor esfuerzo: si falla, la entrega igual se completa. |
| 11 | El sistema descuenta el stock físico de lo entregado y acredita los envases vacíos recolectados, dentro de la misma operación y sin que un fallo la revierta. |
| 12 | El sistema avisa al cliente en tiempo real del nuevo estado, avisa a los administradores y envía la notificación, todo de mejor esfuerzo. |

**Postcondición:** El pedido está entregado, con la evidencia de que el cliente validó la entrega o con el motivo del administrador en su historial de estados. Si el pago era en efectivo, sigue pendiente de cobro. El chofer salió del seguimiento en vivo y los envases del pedido figuran en poder del cliente. Las llenas entregadas salieron del camión del pedido o del depósito predeterminado y los vacíos recolectados entraron en el mismo lugar (CU-220).

**Excepciones**

| Paso | Acción |
|------|--------|
| 1 | Si el chofer que muestra el QR tuvo el pedido y ya no lo tiene a cargo, al ver el pedido (CU-006) el sistema informa «Este pedido ya no está asignado a tu usuario» y la aplicación sale de la pantalla. |
| 3 | Si el código falta o viene vacío, el sistema rechaza la operación. |
| 3 | Si se reintenta el mismo envío con datos distintos, el sistema lo rechaza y no lo ejecuta. |
| 4 | Si el pedido no existe, el sistema informa «Order with ID: … not found». |
| 4 | Si el pedido es de una distribuidora distinta de la que está en contexto —la del administrador que confirma una entrega asistida, o la que eligió el cliente—, el sistema informa lo mismo, sin revelar que existe. |
| 4 | Si el pedido es de otro cliente, el sistema deniega la operación e informa «No autorizado a confirmar la entrega de otro cliente». |
| 5 | Si el pedido ya está entregado, no es un error: el sistema muestra el pedido tal cual, sin reprocesar ni volver a exigir el código, para tolerar el doble escaneo y el reintento de red. |
| 5 | Si el pedido está en cualquier otro estado que no sea en camino, el sistema rechaza la operación e informa «El pedido no está en camino, no se puede confirmar la entrega». |
| 6 | Si el código no tiene el formato de un código de entrega, porque se leyó mal o se escribió mal, el sistema rechaza la operación e informa que el código no se leyó bien, para que el cliente lo escanee o lo escriba de nuevo; si lo envió un cliente, suma un intento fallido. |
| 6 | Si el solicitante es un cliente y el código es el de otro pedido suyo que también está en camino, el sistema rechaza la operación e informa que ese código corresponde a otro pedido, y suma un intento fallido. |
| 6 | Si el código no coincide, o el pedido no tiene código, el sistema rechaza la operación e informa «Código de entrega inválido»; si lo envió un cliente, suma un intento fallido. |
| 6 | Si el cliente ya sumó cinco códigos incorrectos, el pedido está bloqueado: el sistema rechaza la operación e informa «Demasiados intentos: pedile al chofer un código nuevo», incluso si el código es el correcto, hasta que el chofer o un administrador genere un código nuevo (CU-078). El administrador no se bloquea. |
| 7 | Si confirma un administrador y el motivo falta o no tiene entre 10 y 500 caracteres, el sistema rechaza la operación; esta comprobación es posterior a la del código. |
| 11 | Si ni el camión ni el depósito tienen llenas suficientes, la entrega igual se completa y lo pendiente queda para la conciliación (CU-224); se resuelve con CU-278. |
| 4 | Si el solicitante es el Administrador General y no indica la distribuidora, el sistema rechaza la operación e informa que falta indicar la distribuidora. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 7 | 3 segundos |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Una vez por pedido entregado, en el pico de la franja horaria de entrega. |
| **Estabilidad** | Alta |
| **Comentarios** | El código tiene un millón de combinaciones y solo vale mientras el pedido está en camino; como cada cliente puede equivocarse a lo sumo cinco veces antes del bloqueo, adivinarlo es inviable. Los administradores también pueden confirmar, para entregas asistidas desde soporte: no tienen la prueba del escaneo, así que dejan el motivo asentado igual que en CU-020. El descuento del stock (CU-220, incluido en este caso) se hace en la misma operación; si no puede, la entrega igual queda confirmada y lo pendiente se ve en la conciliación (CU-224). El cobro del efectivo es un circuito aparte, a cargo del chofer (CU-292 y CU-293). |

---

#### Crítico CU-292 — Confirmar el Cobro en Efectivo

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-04, OBJ-07 |
| **Requisitos asociados** | IRQ-02, IRQ-08 |
| **Descripción** | El chofer asignado a un pedido entregado y pagado en efectivo confirma que cobró. Entregar un pedido no lo marca como pagado: el pago queda pendiente hasta que el chofer confirma en este caso. Pasa a pagado y el sistema registra el momento y al chofer que lo confirmó. |
| **Precondición** | El solicitante está identificado como el chofer asignado al pedido. El pedido está entregado, se paga en efectivo y su pago está pendiente. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El chofer entrega el pedido (CU-079) y cobra el efectivo al cliente. |
| 2 | En su aplicación, el chofer elige «Pago recibido». Si repite el envío por un corte de conexión, el sistema no lo procesa dos veces. |
| 3 | El sistema comprueba que el pedido sea de la distribuidora y lo reserva mientras opera, para que nadie lo cambie a la vez. |
| 4 | El sistema comprueba que el pedido sea del chofer, que esté entregado y que se haya pagado en efectivo. |
| 5 | Si el pago está pendiente, el sistema lo pasa a pagado y registra el momento y el chofer que lo confirmó. |
| 6 | El sistema muestra el pedido con el pago pagado. |

**Postcondición:** El pago del pedido está pagado, con el momento de la confirmación y el chofer que la hizo.

**Excepciones**

| Paso | Acción |
|------|--------|
| 3 | Si el pedido no existe o es de otra distribuidora, el sistema informa que no lo encontró. |
| 4 | Si el pedido está asignado a otro chofer, el sistema rechaza la operación e informa «Este pedido no está asignado a tu usuario», antes de mirar el estado. |
| 4 | Si el pedido no está entregado, o no se pagó en efectivo, el sistema rechaza la operación. |
| 5 | Si el pago ya estaba pagado, no es un error: el sistema muestra el pedido tal cual. |
| 5 | Si el pago ya se informó como impago, el sistema rechaza la operación: lo resuelve un administrador (CU-294). |
| 2 | Si se reintenta el mismo envío con datos distintos, el sistema lo rechaza. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 5 | 1 segundo |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Una vez por pedido entregado en efectivo. |
| **Estabilidad** | Alta |
| **Comentarios** | Entregar no es cobrar: la entrega (CU-020 y CU-079) deja el pago en efectivo pendiente, y el cobro lo confirma el chofer apenas recibe el dinero. Es el dato que alimenta el efectivo cobrado de la jornada del chofer (CU-291). Si el cliente no pagó, el chofer informa el impago con CU-293. |

---

#### Importante CU-301 — Confirmar una Transferencia

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-04, OBJ-07 |
| **Requisitos asociados** | IRQ-02, IRQ-08 |
| **Descripción** | El administrador resuelve el cobro de un pedido pagado por transferencia: confirmarla pasa el pago a pagado, desde pendiente o desde fallido —la transferencia llegó después de marcarla no recibida—; marcarla no recibida lo deja fallido, solo desde pendiente y solo sobre un pedido entregado. Exige el motivo, que queda en la nota de resolución, en el historial de estados y en la auditoría. Una transferencia sin confirmar no suma a las ventas. |
| **Precondición** | El solicitante está identificado como administrador (el Administrador General debe indicar la distribuidora). El pedido se paga por transferencia y no está cancelado. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El administrador abre un pedido pagado por transferencia y elige confirmarla o marcarla como no recibida. |
| 2 | Escribe el motivo, de 10 a 500 caracteres. Si repite el envío por un corte de conexión, el sistema no lo procesa dos veces. |
| 3 | El sistema comprueba que el pedido sea de la distribuidora y lo reserva mientras opera, para que nadie lo cambie a la vez. |
| 4 | El sistema comprueba que el pedido se pague por transferencia y no esté cancelado. |
| 5 | Si la decisión ya estaba tomada, el sistema muestra el pedido tal cual. Si no, comprueba que el cambio sea válido: confirmar vale desde pendiente o desde fallido; marcar como no recibida vale solo desde pendiente y con el pedido entregado. |
| 6 | El sistema pasa el pago a pagado o a fallido y registra el momento y al administrador como quien lo resolvió, con el motivo; si fue pagado, registra también la confirmación del cobro. |
| 7 | El sistema deja en el historial de estados una nota con el mismo estado de origen y de destino y el texto «Transferencia confirmada (o marcada como no recibida) por un administrador: motivo»; la auditoría registra el cambio. |
| 8 | El sistema muestra el pedido. |

**Postcondición:** El pago del pedido está pagado o fallido según la decisión, con quién, cuándo y por qué; el historial tiene la nota del motivo.

**Excepciones**

| Paso | Acción |
|------|--------|
| 4 | Si el pedido no existe o es de otra distribuidora, el sistema informa que no lo encontró. |
| 4 | Si el Administrador General no indica la distribuidora, el sistema rechaza la operación e informa que falta indicar la distribuidora. |
| 2 | Si no se indica si llegó o no, o el motivo falta o no tiene entre 10 y 500 caracteres, el sistema rechaza la operación. |
| 2 | Si se reintenta el mismo envío con datos distintos, el sistema lo rechaza. |
| 4 | Si el pedido no es una transferencia, o está cancelado, el sistema rechaza la operación. |
| 5 | Si el pago ya estaba en lo que se pide, no es un error: el sistema muestra el pedido tal cual. |
| 5 | Si la transferencia ya estaba pagada y se la quiere marcar como no recibida, o el pago ya no está pendiente, el sistema rechaza la operación e informa «La transferencia ya se confirmó: no se cambia». |
| 5 | Si se quiere marcar como no recibida un pedido que todavía no se entregó, el sistema rechaza la operación: marcarla antes no frenaría nada. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 8 | 2 segundos |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Media: una vez por pedido pagado por transferencia. |
| **Estabilidad** | Alta |
| **Comentarios** | Una transferencia sin confirmar no suma a las ventas: el reporte de cobros pendientes (CU-304) la informa como pendiente de confirmar o como no recibida. Si la transferencia se confirma y el pedido se cancela después, la cancelación no se bloquea, pero el dinero ya está en la distribuidora: el reporte lo informa como reintegro pendiente y el sistema no gestiona el reintegro. La nota del historial no es una transición: tiene el mismo estado de origen y de destino. |

---

#### Crítico CU-048 — Procesar el Pago con MercadoPago

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-02, OBJ-07 |
| **Requisitos asociados** | IRQ-02, IRQ-08 |
| **Descripción** | Cuando un pedido se paga con MercadoPago, la pasarela avisa al sistema. El sistema valida la autenticidad del aviso, consulta el estado real del pago en MercadoPago —sin confiar nunca en el contenido recibido—, actualiza el registro de pagos, marca el pedido como pagado y recién entonces dispara el despacho. Si el mismo aviso llega más de una vez, no produce efectos nuevos. Complementa a CU-005, donde el cliente solo elige el medio de pago. |
| **Precondición** | Existe un pedido con medio de pago MercadoPago y un intento de cobro registrado como pendiente, referido al pedido. La clave que autentica los avisos y la dirección donde la pasarela notifica están configuradas. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El cliente completa el pago en la pantalla de cobro de MercadoPago. |
| 2 | MercadoPago avisa al sistema, con el tipo de evento y el identificador del pago. El aviso no cuenta contra el límite general de solicitudes, porque la pasarela puede notificar en ráfaga. |
| 3 | El sistema tolera los dos formatos que usa MercadoPago y normaliza el identificador del pago y el tipo de evento. |
| 4 | El sistema valida la autenticidad del aviso con la clave configurada. |
| 5 | El sistema descarta todo aviso cuyo tipo no sea de pago o que llegue sin identificador de pago. |
| 6 | El sistema consulta el pago real a MercadoPago, con un tiempo máximo de espera de cinco segundos para no retener conexiones. |
| 7 | El sistema actualiza su registro de pagos: busca el intento por el identificador de pago de la pasarela y, si es el primer aviso, toma el intento pendiente más reciente de ese pedido. Le asigna el identificador y traduce el estado de la pasarela a aprobado, rechazado, cancelado, reintegrado o pendiente. |
| 8 | El sistema recupera el pedido a partir de la referencia del pago. |
| 9 | Si el pago está aprobado, el sistema vuelve a leer el pedido, de modo que dos avisos simultáneos del mismo pago no pasen ambos el control de repetición. |
| 10 | Si el pedido está en un estado terminal, o ya tiene un identificador de pago, o ya está pagado, el sistema termina sin modificar nada. |
| 11 | Si el pedido es una reserva, el pago corresponde a la seña: el sistema marca la seña como pagada, guarda el identificador del pago y no despacha, porque la reserva la activa el proceso automático el día agendado. |
| 12 | En el caso general, el sistema marca el pedido como pagado y guarda el identificador del pago de la pasarela. |
| 13 | Después de confirmar lo anterior, el sistema avisa al cliente que su pago fue aprobado, en tiempo real y por notificación, de mejor esfuerzo. El aviso sale solo en la primera confirmación: los reintentos no lo repiten. |
| 14 | Si el pedido no es una reserva, el sistema dispara el despacho al siguiente chofer candidato (CU-013), de mejor esfuerzo. |
| 15 | El sistema acusa recibo a MercadoPago. |

**Postcondición:** El registro de pagos refleja el estado real informado por la pasarela. Si el pago fue aprobado, el pedido quedó pagado con el identificador del pago —o con la seña marcada como pagada, si era una reserva— y el despacho se disparó exactamente una vez. Repetir el mismo aviso no vuelve a marcar el pedido, ni a avisar al cliente, ni a despacharlo.

**Excepciones**

| Paso | Acción |
|------|--------|
| 4 | Si la autenticidad del aviso no se puede comprobar, o falta la clave configurada, el sistema registra la advertencia, no procesa el aviso y acusa recibo de todas formas, para no revelar si el pago o el pedido existen. |
| 6 | Si la consulta del pago a MercadoPago falla o supera el tiempo de espera, el sistema registra el error y aborta el procesamiento sin tocar el pedido. |
| 6 | Si el pago que informa la pasarela no trae referencia al pedido, el sistema registra la advertencia y lo ignora. |
| 7 | Si no se encuentra ningún intento de cobro asociado a ese pago, el sistema registra la advertencia y continúa igual con la confirmación del pedido: el registro de pagos queda incompleto, pero el pedido sí se actualiza. |
| 8 | Si la referencia no corresponde a ningún pedido, el sistema registra la advertencia y aborta. |
| 9 | Si el pedido desaparece entre la consulta inicial y el bloqueo, el sistema registra la advertencia y aborta. |
| 9 | Ante cualquier error al actualizar, el sistema deshace los cambios, lo registra y acusa recibo igualmente, para que MercadoPago no reintente en bucle contra una respuesta de error. |
| 13 | Si el aviso al cliente falla, el sistema registra el error y sigue: el pago no se revierte ni se detiene el despacho. |
| 14 | Si el despacho falla, el sistema registra el error y el pedido queda pagado a la espera del reintento del despacho: el pago no se revierte. |
| 9 | Si el pago llega rechazado o cancelado, el sistema únicamente lo registra, no realiza ninguna acción sobre el pedido y no avisa al cliente (ver Comentarios). |
| 9 | Si el pago llega en un estado no definitivo, el sistema lo registra como tal y no actúa. |
| 9 | Si el pago ya estaba aprobado y llega un aviso atrasado como pendiente, rechazado o cancelado, el sistema lo ignora: un pago aprobado sólo puede pasar a devuelto. La base de datos lo garantiza aunque el aviso llegue por otro camino. |
| 9 | Si la pasarela aprueba un importe distinto del esperado, el sistema marca el pago, deja una alerta registrada, y no da el pedido por pagado ni lo despacha. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 15 | 5 segundos |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Una o más notificaciones por cada pedido pagado con MercadoPago; la pasarela reintenta el mismo aviso si no recibe respuesta. |
| **Estabilidad** | Alta |
| **Comentarios** | La repetición segura no descansa en un solo mecanismo sino en tres, encadenados: un identificador de pago único en el registro de pagos, otro en el pedido, y el bloqueo del pedido mientras se actualiza, que serializa dos avisos concurrentes del mismo pago. Un pago rechazado o cancelado no tiene un circuito propio: el pedido queda pendiente con su stock reservado hasta que el proceso automático lo cancela por vencimiento (CU-077) y recién ahí libera el stock; el cliente no se entera del rechazo. |

---

#### Importante CU-023 — Registrar un Reclamo

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-04 |
| **Requisitos asociados** | IRQ-06 |
| **Descripción** | El cliente registra un reclamo sobre un pedido propio, con el motivo, una descripción y, opcionalmente, una foto. El reclamo nace pendiente y hereda la distribuidora del pedido reclamado. |
| **Precondición** | El cliente está identificado y el pedido existe y es suyo. Si el reclamo lo registra un administrador, el pedido es de su distribuidora. El pedido no tiene que estar entregado. |
| **Puntos de extensión** | PE-06: El cliente adjunta evidencia fotográfica, lo extiende CU-174 Adjuntar la Fotografía de un Reclamo. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El cliente abre su historial de pedidos y elige uno. |
| 2 | Elige registrar un reclamo. |
| 3 | Ingresa el motivo y una descripción detallada y, si quiere, adjunta una foto, que se sube con CU-174 Adjuntar la Fotografía de un Reclamo (punto de extensión PE-06). |
| 4 | Confirma el envío. |
| 5 | El sistema toma como reclamante al cliente identificado, ignorando cualquier otro cliente que venga en la solicitud; un administrador sí puede registrar el reclamo a nombre de un cliente, para soporte. |
| 6 | Si quien registra es un administrador, el sistema comprueba primero que el pedido sea de su distribuidora; después, que exista y que pertenezca al cliente indicado. |
| 7 | El sistema crea el reclamo pendiente y le asigna la distribuidora del pedido reclamado. |

**Postcondición:** Existe un reclamo pendiente asociado al pedido, al cliente y a la distribuidora del pedido. El administrador no fue avisado: lo descubre al consultar el listado (CU-024).

**Excepciones**

| Paso | Acción |
|------|--------|
| 6 | Si el pedido no existe, el sistema informa «Order with ID: … not found». |
| 6 | Si quien registra es un administrador y el pedido es de otra distribuidora, el sistema informa que no lo encontró, sin revelar que existe. |
| 6 | Si el pedido no pertenece al cliente indicado, el sistema informa «Esta orden no pertenece al cliente indicado» como solicitud incorrecta, no como acceso denegado. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 7 | 2 segundos |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Baja por cliente: esporádica, solo ante un problema con un pedido. |
| **Estabilidad** | Alta |
| **Comentarios** | El sistema no exige que el pedido esté entregado para admitir un reclamo: se puede reclamar un pedido pendiente, aceptado o incluso cancelado, de modo que la regla de negocio que daba sentido al caso no está implementada. El sistema no avisa al administrador de que entró un reclamo nuevo: el vínculo con CU-024 depende de que alguien mire el listado. La foto se sube y se consulta con CU-174 y CU-175. |

---

#### Importante CU-025 — Resolver un Reclamo

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-04, OBJ-05 |
| **Requisitos asociados** | IRQ-06 |
| **Descripción** | El administrador define la resolución de un reclamo pendiente o en proceso, dejándolo resuelto o rechazado, con una nota de resolución obligatoria. Un reclamo ya resuelto o rechazado no admite esta operación sin reabrirlo antes (CU-167). |
| **Precondición** | El solicitante está identificado como administrador (el Administrador General indica la distribuidora). El reclamo existe, es de su distribuidora y está pendiente o en proceso. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El administrador abre el detalle del reclamo. Si ya lo tomó antes (CU-166), está en proceso; también puede resolver uno todavía pendiente sin tomarlo primero. |
| 2 | Lee el motivo, la descripción y la foto adjunta, si la hay. |
| 3 | Elige el estado de cierre —resuelto o rechazado— e ingresa la nota de resolución. |
| 4 | Confirma la acción. |
| 5 | El sistema comprueba que el reclamo exista y sea de su distribuidora, que la nota no esté vacía y que el cambio de estado sea válido, sin admitir repetir el estado actual. |
| 6 | El sistema guarda el nuevo estado y la nota de resolución. |

**Postcondición:** El reclamo quedó con el estado elegido y su nota de resolución. No queda constancia de cuándo se resolvió ni de quién lo resolvió, y el cliente no fue avisado.

**Excepciones**

| Paso | Acción |
|------|--------|
| 5 | Si la nota falta, está vacía o tiene solo espacios, el sistema rechaza la operación por dato obligatorio. |
| 3 | Si el estado elegido no es resuelto ni rechazado —por ejemplo, en proceso o pendiente—, el sistema rechaza la operación e informa «status debe ser uno de: resolved, rejected». Pasar un reclamo a en proceso es CU-166 y ningún camino lo devuelve a pendiente. |
| 5 | Si el reclamo no existe, o es de otra distribuidora, el sistema informa «Reclamo no encontrado», sin distinguir ambos casos. |
| 5 | Si el reclamo ya está resuelto o rechazado, el sistema rechaza el cambio con el detalle —por ejemplo «Transición de reclamo inválida: resolved → rejected»— y no pisa la nota anterior; hay que reabrirlo primero (CU-167). Repetir el mismo estado también se rechaza. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 6 | 1 segundo |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Media: acompaña la frecuencia de ingreso de reclamos nuevos. |
| **Estabilidad** | Alta |
| **Comentarios** | Los cambios de estado se validan contra reglas explícitas (CU-025, CU-166 y CU-167): pendiente y en proceso admiten resolución directa; resuelto y rechazado solo se modifican reabriéndolos antes. Dos resoluciones simultáneas se serializan: la segunda se valida contra el estado que dejó la primera. El sistema no registra la fecha de la resolución ni el administrador que la firmó, de modo que el circuito de reclamos no es auditable por sí mismo (el registro de auditoría conserva la operación). El sistema no avisa al cliente el resultado de su reclamo: no tiene forma de enterarse si no vuelve a preguntar. |

---

#### Importante · automático CU-105 — Planificar el Mantenimiento y las Habilitaciones de la Flota

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-02, OBJ-05 |
| **Requisitos asociados** | IRQ-02, IRQ-03 |
| **Descripción** | El sistema proyecta el vencimiento de cada tarea de mantenimiento y de cada habilitación de la flota, y planifica la ventana de taller que menos perjudica a la operación. La ventana no se impone: se negocia con el chofer asignado, ofreciéndole una alternativa por vez con vigencia acotada. Cuando ninguna prospera, el caso queda a resolución del administrador con el cuadro completo a la vista. En paralelo, el vehículo con una habilitación bloqueante vencida deja de recibir ofertas de pedidos: el módulo alimenta al despacho automático de M1. |
| **Precondición** | El vehículo existe y pertenece a una distribuidora activa. Tiene al menos una regla de mantenimiento o de habilitación aplicable. Hay historial de uso suficiente para estimar el consumo, o está disponible el promedio de la flota del mismo tipo de vehículo como respaldo. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El proceso automático se ejecuta una vez por día, a la hora que fija la configuración de la distribuidora. |
| 2 | El sistema recorre la flota activa y, para cada vehículo, estima el consumo diario de kilómetros con una media que da más peso a las semanas recientes y corrige el resultado por la estacionalidad del mes. Si el historial no alcanza la muestra mínima configurada, toma el promedio de la flota del mismo tipo. |
| 3 | El sistema proyecta la fecha de vencimiento de cada tarea sobre la misma agrupación por vehículo y por chofer. Las de kilometraje, cruzando los kilómetros que faltan contra el consumo estimado; las de fecha fija —revisión técnica, seguro, matafuegos, licencia del chofer—, directamente contra su fecha. |
| 4 | El sistema selecciona las tareas cuya fecha proyectada entra dentro de la ventana de anticipación configurada para ese tipo, en días o en kilómetros según corresponda. |
| 5 | Para cada tarea seleccionada, el sistema enumera las ventanas de taller posibles entre hoy y la fecha proyectada, y descarta las que dejarían la zona de cobertura del vehículo por debajo del mínimo de unidades activas configurado. La zona del vehículo se deriva de las zonas donde entregó en los últimos días. |
| 6 | El sistema ordena las ventanas factibles por demanda histórica proyectada, de menor a mayor, y se queda con las mejores, en la cantidad que fija la configuración. |
| 7 | El sistema propone la primera ventana al chofer asignado al vehículo, con la vigencia de propuesta configurada, y le avisa por notificación. |
| 8 | El sistema espera la respuesta. Si el chofer acepta, la tarea queda pendiente de confirmación del administrador, que confirma el gasto del taller (paso 11); recién entonces el sistema bloquea la agenda del vehículo para esa fecha y da la tarea por programada. |
| 9 | Si el chofer rechaza, o la vigencia pasa sin respuesta, la propuesta se cierra y el sistema ofrece la ventana siguiente de la lista, repitiendo el paso 7. |
| 10 | Agotadas las alternativas sin acuerdo, el sistema arma el cuadro con la tarea, el vehículo, todas las ventanas evaluadas y el motivo de descarte de cada una, y lo escala al administrador. |
| 11 | El administrador revisa el cuadro, elige una ventana o define otra por su cuenta, y confirma la contratación del taller. El sistema registra la tarea como programada con esa ventana. |
| 12 | Al detectar una habilitación bloqueante vencida, el sistema deja el vehículo fuera de servicio y lo excluye de los candidatos del despacho automático, sin esperar ninguna confirmación. |

**Postcondición:** Toda tarea dentro de la ventana de anticipación tiene su fecha de vencimiento proyectada. Cada tarea alertada queda con una ventana acordada con el chofer y confirmada por el administrador, programada con la ventana que resolvió el administrador, o pendiente de su decisión. Ningún vehículo con una habilitación bloqueante vencida recibe ofertas de pedidos.

**Excepciones**

| Paso | Acción |
|------|--------|
| 2 | Si el vehículo no tiene historial de uso ni existe promedio de flota para su tipo, la proyección por kilometraje no se calcula: la tarea queda en observación y solo se evalúan sus habilitaciones por fecha fija. |
| 5 | Si ninguna ventana resulta factible porque toda opción deja la zona bajo el mínimo, el proceso salta la negociación con el chofer y escala directamente al administrador, indicando que la restricción de cobertura es la que impide programar. |
| 7 | Si el vehículo no tiene chofer asignado, no hay con quién negociar: el caso se escala al administrador desde el primer momento. |
| 8 | Si la tarea llega a su fecha proyectada sin ventana acordada, el sistema la marca vencida. Si es bloqueante, deja el vehículo fuera de servicio. |
| 11 | Si el administrador no resuelve antes del vencimiento proyectado, el caso permanece abierto y se reitera en cada ejecución del proceso, sin que el sistema contrate nada por su cuenta. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 1 | Proceso diario, a la hora configurada |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Automático, una vez por día a la hora configurada. |
| **Estabilidad** | Media |
| **Comentarios** | Módulo inteligente M2, implementado en el sistema, en el panel de administración (planificador de taller) y en la aplicación del chofer, que recibe la propuesta de ventana y la acepta o la rechaza. Su especificación de diseño está en el Documento 3. Las reglas y las tareas de mantenimiento son las de la gestión de la flota (CU-136 a CU-142). Los kilómetros de cada vehículo salen, por día, de la distancia entre las paradas entregadas; cuando hay lecturas del odómetro —en las cargas de combustible y en el cierre de las tareas—, la medición reemplaza a la estimación. Al cerrar la tarea, el gasto del taller sale de la caja. Es el único módulo que combina las tres partes: el sistema propone, el chofer negocia la ventana y el administrador confirma el gasto del taller; la contratación nunca la ejecuta el sistema. |

---

#### Importante · automático CU-106 — Anticipar la Recompra por Consumo Estimado

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-01 |
| **Requisitos asociados** | IRQ-01, IRQ-02, IRQ-04 |
| **Descripción** | El sistema recorre los clientes con historial suficiente, estima para cada uno cuándo se le termina el gas y le acerca la reposición antes de que la necesite, con el pedido armado y una vigencia acotada. El destinatario de la oferta es el propio cliente y la decisión es suya: el sistema no crea ningún pedido hasta que acepta. La caducidad y el período de enfriamiento evitan que la invitación se vuelva insistencia. |
| **Precondición** | El cliente tiene al menos la cantidad mínima configurada de pedidos entregados, no tiene un pedido activo y no recibió una invitación dentro del intervalo mínimo de reiteración. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El proceso automático se ejecuta una vez por día, a la hora que fija la configuración de la distribuidora. |
| 2 | El sistema recorre los clientes que alcanzan el mínimo de pedidos configurado y arma, para cada uno, la serie de fechas de compra con los kilos entregados en cada una. |
| 3 | El sistema calcula el intervalo medio entre compras ponderado por kilos: una carga de 45 kg dura más que una de 10 kg y pesa distinto en el promedio. |
| 4 | El sistema corrige el intervalo según la estacionalidad del mes en curso, porque el consumo de gas del invierno no es el del verano. |
| 5 | El sistema proyecta la fecha de agotamiento sumando el intervalo corregido a la última entrega. |
| 6 | El sistema se queda con los clientes cuya fecha proyectada cae dentro de la ventana de anticipación configurada. |
| 7 | El sistema descarta a los que tienen un pedido activo sin entregar, a los que recibieron una entrega reciente y a los que ya fueron invitados dentro del intervalo mínimo. |
| 8 | Para cada cliente que queda, el sistema arma el pedido con los productos y cantidades que sugiere su historial, sobre su última dirección de entrega, y emite la invitación con su vencimiento. |
| 9 | El sistema avisa al cliente por notificación y, de forma complementaria, por correo. |
| 10 | Si el cliente acepta dentro de la vigencia, el sistema crea el pedido con los datos armados, reserva el stock y lo entrega al despacho automático, que lo ofrece al chofer más cercano (CU-013). |
| 11 | Si el cliente rechaza la invitación, el sistema la cierra y registra el rechazo para no reiterarla antes del intervalo mínimo. |
| 12 | Si la vigencia pasa sin respuesta, el sistema da la invitación por caducada y guarda la fecha, que gobierna cuándo puede volver a invitar al mismo cliente. |

**Postcondición:** Cada cliente dentro de la ventana de anticipación tiene a lo sumo una invitación vigente. Los pedidos que nacieron de una invitación aceptada están pendientes dentro del circuito de despacho. Ninguna invitación caducada o rechazada se reitera antes del intervalo mínimo.

**Excepciones**

| Paso | Acción |
|------|--------|
| 2 | Si el cliente no llega al mínimo de pedidos configurado, el sistema estima con el consumo que el cliente declaró; si tampoco lo declaró, queda fuera de la evaluación: sin datos no hay estimación posible. |
| 5 | Si la serie de compras es demasiado irregular como para que el intervalo estimado tenga sentido, el cliente queda fuera de la invitación de esa corrida. |
| 8 | Si al armar la invitación no hay stock del producto que sugiere el historial, la invitación no se emite y el cliente se reevalúa en la corrida siguiente. |
| 10 | Si al aceptar el cliente el stock ya no alcanza, el pedido no se crea: el sistema le avisa y la invitación se cierra sin efecto. |
| 10 | Si el precio del producto cambió entre la emisión y la aceptación, la invitación se muestra con el precio vigente al aceptar y el cliente confirma sobre ese importe. |
| 10 | Si el cliente compró por su cuenta mientras la invitación corría, la invitación se cierra sin efecto y el conteo del intervalo se reinicia con esa compra. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 1 | Proceso diario, fuera del horario de mayor demanda |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Automático, una vez por día. |
| **Estabilidad** | Media |
| **Comentarios** | Módulo inteligente M3, implementado en el sistema y en el panel de administración, donde el administrador ve a qué clientes se les acaba el gas, las invitaciones emitidas y cuántas terminan en pedido, ajusta los parámetros y puede simular una corrida; la etapa de la aplicación del cliente, donde el cliente recibe y acepta la invitación, está en curso. El proceso viene apagado: cada distribuidora lo habilita desde sus parámetros. Su especificación de diseño está en el Documento 3. Es el único de los cuatro módulos que no reserva ninguna decisión al administrador: el destinatario de la oferta es el cliente y la decisión de comprar es suya. El mínimo de pedidos para estimar, la anticipación, la vigencia, el intervalo mínimo de reiteración y los coeficientes de estacionalidad se leen de la configuración de la distribuidora (CU-172). Un cliente pertenece a una distribuidora desde su primera compra: la invitación se emite a nombre de la distribuidora de la última compra y un cliente sin compras no recibe invitación. |

---

#### Importante · automático CU-107 — Agrupar Pedidos por Recorrido

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-02, OBJ-08 |
| **Requisitos asociados** | IRQ-02, IRQ-03, IRQ-05 |
| **Descripción** | El sistema arma lotes de pedidos que se pueden entregar en un mismo viaje sin incumplir el compromiso horario de ninguno ni exceder la capacidad del vehículo, y los negocia con los choferes de a uno por vez, igual que M1 negocia un pedido suelto. La diferencia es el objeto de la oferta: no un pedido, sino un recorrido con sus paradas ya ordenadas. El lote nunca se impone: ante el silencio o el rechazo generalizado, los pedidos siguen su camino individual y ninguno queda retenido. |
| **Precondición** | Hay al menos dos pedidos programados con franja futura, de la misma distribuidora, dentro del radio de agrupación configurado y con franjas compatibles, y al menos un chofer activo con capacidad de carga disponible. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El proceso automático se ejecuta con la frecuencia que fija la configuración de la distribuidora. |
| 2 | El sistema recupera los pedidos programados con franja futura y sin chofer, de la distribuidora y su zona de cobertura. |
| 3 | El sistema agrupa los candidatos por cercanía, sin superar el radio de agrupación configurado entre paradas del mismo lote. |
| 4 | Dentro de cada grupo, el sistema descarta las combinaciones cuyas franjas difieren más que la tolerancia configurada: el lote no puede hacer que un cliente reciba fuera de la franja que eligió. |
| 5 | El sistema arma los lotes candidatos respetando el tamaño máximo configurado y la capacidad de carga del vehículo en uso del chofer al que se le va a ofrecer (CU-161). |
| 6 | El sistema ordena las paradas de cada lote de modo que el recorrido cumpla las franjas comprometidas y minimice la distancia entre paradas. |
| 7 | El sistema ofrece el lote completo al primer chofer candidato —el más cercano al punto de partida que no fue contactado por este lote—, con el detalle de las paradas, el peso total y la vigencia de la oferta. |
| 8 | Si el chofer acepta dentro de la vigencia, el sistema le asigna los pedidos del lote en el orden establecido y cada uno sigue su ciclo de entrega normal. |
| 9 | Si el chofer rechaza, la oferta se cierra y el lote pasa de inmediato al siguiente candidato, sin esperar el vencimiento. |
| 10 | Si la vigencia pasa sin respuesta, la oferta se da por vencida y el lote pasa al siguiente candidato. |
| 11 | Agotados los candidatos, el sistema deshace el lote y devuelve los pedidos al circuito individual, donde cada uno se ofrece por separado (CU-013). |

**Postcondición:** Cada lote armado está asignado a un único chofer con sus paradas ordenadas, o fue deshecho y sus pedidos volvieron al circuito individual. Ningún pedido queda retenido por la agrupación ni asignado dos veces.

**Excepciones**

| Paso | Acción |
|------|--------|
| 2 | Si no hay pedidos suficientes para armar un lote, el proceso no hace nada y los pedidos siguen su curso individual. |
| 5 | Si ningún vehículo disponible tiene capacidad para el peso total del lote candidato, el lote se recorta hasta que entre, o se descarta si con dos paradas ya excede la capacidad. |
| 7 | Si un pedido del lote es aceptado o cancelado por otra vía mientras la oferta corre, el sistema recalcula el lote antes de ofrecerlo al candidato siguiente. |
| 8 | Si al aceptar el chofer alguno de los pedidos ya no está disponible, se le asigna el resto del lote y el faltante se descuenta del recorrido. |
| 11 | Si al deshacer el lote los pedidos ya superaron su franja comprometida, vuelven al circuito individual con la prioridad que corresponde a su demora. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 1 | Proceso periódico, fuera del horario de mayor demanda |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Automático, con la periodicidad configurada por la distribuidora. |
| **Estabilidad** | Media |
| **Comentarios** | Módulo inteligente M4, implementado en el sistema y en el panel de administración, donde el administrador sigue los recorridos ofrecidos, asignados, completados y deshechos; la etapa de la aplicación del chofer está en curso. El proceso viene apagado: cada distribuidora lo habilita desde sus parámetros. Su especificación de diseño está en el Documento 3. No reserva ninguna decisión al administrador: el destinatario de la oferta es el chofer, que acepta o rechaza el recorrido. Convive con M1 sin reemplazarlo: el lote que nadie toma se disuelve y sus pedidos vuelven a la asignación individual, de modo que la agrupación optimiza el costo por entrega pero nunca es condición para que un pedido salga. El tamaño máximo del lote, el radio de agrupación, la tolerancia de franja, la vigencia de la oferta y la frecuencia se leen de la configuración de la distribuidora. Decisión de diseño: se agrupan solo los pedidos programados con franja futura; los inmediatos quedan a cargo de M1. |

---

#### Importante · automático CU-108 — Recuperar Envases No Devueltos

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-04, OBJ-05 |
| **Requisitos asociados** | IRQ-01, IRQ-02 |
| **Descripción** | Detectar el envase retenido es una consulta; lo que este caso especifica es la secuencia de gestión que se abre después. Cada escalón tiene su propio plazo, el caso se reevalúa antes de cada paso —el envase puede haber vuelto mientras tanto— y el sistema aprovecha cualquier entrega ya planificada al mismo cliente como oportunidad de recupero sin costo adicional. Agotada la secuencia, el legajo completo queda a resolución del administrador: el sistema nunca cobra un depósito por su cuenta. |
| **Precondición** | Existe al menos un envase cuyo último movimiento lo deja en poder de un cliente, con antigüedad mayor al plazo de tolerancia de devolución configurado. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El proceso automático se ejecuta con la frecuencia que fija la configuración de la distribuidora. |
| 2 | El sistema recorre el historial de movimientos de envases (CU-071) y selecciona los que permanecen en poder de un cliente por encima del plazo de tolerancia. |
| 3 | Para cada envase retenido, el sistema abre un caso de recupero con el cliente, el envase, la fecha de entrega y el importe del depósito comprometido, o retoma el caso abierto si ya existe. |
| 4 | Antes de cada escalón, el sistema vuelve a leer el estado del envase: si registró su devolución mientras el caso corría, lo cierra sin más gestión. |
| 5 | Primer escalón: el sistema envía al cliente un recordatorio de devolución. |
| 6 | Si el cliente tiene una entrega programada dentro de la ventana del caso, el sistema le ofrece devolver el envase en ese mismo viaje, con la vigencia de oferta de retiro configurada. |
| 7 | Cumplido el plazo del escalón sin devolución, el sistema pasa al siguiente: un aviso con el detalle del depósito comprometido y las consecuencias de no devolver. |
| 8 | Si el cliente acepta devolver el envase en la próxima entrega, el sistema lo suma al recorrido del chofer y espera la confirmación del movimiento de retorno. |
| 9 | Confirmado el retorno del envase, el caso se cierra y el depósito queda liberado. |
| 10 | Agotados los escalones sin devolución, y si el importe en juego supera el umbral configurado para escalar, el sistema arma el legajo con el cliente, el historial completo del envase, los avisos enviados y el importe, y lo escala al administrador. |
| 11 | El administrador revisa el legajo y decide: cobrar el depósito, dar el envase de baja del inventario o cerrar el caso sin cargo. El sistema registra la decisión y el importe; el cobro del depósito se hace aparte, en el próximo pedido o en efectivo, sin pasarela. |

**Postcondición:** Cada envase retenido tiene un caso de recupero abierto en algún escalón, cerrado por devolución, o escalado al administrador con el legajo completo. Ningún depósito se cobra ni ningún envase se da de baja sin una decisión registrada del administrador.

**Excepciones**

| Paso | Acción |
|------|--------|
| 2 | Si el último movimiento del envase no permite determinar en poder de quién está, el envase queda marcado para revisión manual y no ingresa a la secuencia. |
| 4 | Si el envase vuelve en cualquier punto de la secuencia, el caso se cierra de inmediato y los escalones pendientes no se ejecutan. |
| 6 | Si el cliente no tiene ninguna entrega programada, el escalón de oferta de retiro se saltea y la secuencia continúa con el escalón siguiente. |
| 8 | Si el chofer no logra retirar el envase en la entrega acordada, el caso vuelve al escalón en el que estaba y la secuencia continúa. |
| 10 | Si el importe en juego no supera el umbral de escalamiento configurado, el caso no se eleva: queda registrado como envase perdido con su historial, y se informa en el reporte de la distribuidora. |
| 11 | Si el administrador no resuelve, el caso permanece abierto y se reitera en el reporte, sin que el sistema ejecute cobro alguno. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 1 | Proceso periódico, con la periodicidad configurada |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Automático, con la periodicidad configurada por la distribuidora. |
| **Estabilidad** | Media |
| **Comentarios** | Módulo inteligente M5, implementado en el sistema y en el panel de administración, donde el administrador sigue los casos por escalón y decide los escalados; la etapa de las aplicaciones del cliente y del chofer está en curso. El proceso viene apagado: cada distribuidora lo habilita desde sus parámetros. Su especificación de diseño está en el Documento 3. El plazo de tolerancia de devolución, el plazo de cada escalón, el umbral de importe para escalar y la vigencia de la oferta de retiro se leen de la configuración de la distribuidora. La decisión que compromete dinero —cobrar el depósito o dar el envase de baja— la asume siempre el administrador: el sistema prepara el legajo, nunca ejecuta el cobro. |

---

#### Importante CU-152 — Consultar el Registro de Auditoría

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-04, OBJ-05 |
| **Requisitos asociados** | IRQ-16, NFR-09 |
| **Descripción** | El administrador consulta qué se hizo en el sistema y quién lo hizo. Puede acotar la búsqueda por persona, por tipo de recurso, por un recurso puntual, por período y por resultado. Cada asiento trae, además, lo que se pidió, con las credenciales depuradas. También consulta la auditoría de datos, que la base de datos registra sola por cada cambio: qué registro de qué entidad cambió, con qué acción, con qué origen y, por cada campo, el valor anterior y el nuevo; y los ingresos al sistema, correctos o fallidos, y las salidas. Puede exportar lo que consulta. |
| **Precondición** | El solicitante está identificado como administrador o Administrador General. |
| **Estado** | Implementado |

**Secuencia Normal**

| Paso | Acción |
|------|--------|
| 1 | El administrador indica, si quiere, los filtros: quién hizo la operación, qué tipo de recurso, qué recurso puntual, desde y hasta qué fecha y con qué resultado (éxito o falla), y la página que quiere ver (hasta 200 asientos, 50 por omisión). |
| 2 | El sistema valida los filtros. Si hay una distribuidora elegida —la del administrador de empresa, o la que eligió el Administrador General—, restringe la consulta a los asientos de esa distribuidora; el Administrador General sin distribuidora elegida ve los de todas. |
| 3 | El sistema muestra los asientos que coinciden, del más reciente al más antiguo, con el total de coincidencias. |
| 4 | Por cada asiento, el sistema informa quién lo originó y con qué rol, a qué distribuidora corresponde, qué operación fue, sobre qué recurso, cuándo, desde qué aplicación y desde qué dirección de red, con qué resultado, el motivo si fue rechazada y lo que se pidió, depurado. |
| 5 | Para la auditoría de datos, el administrador indica, si quiere, la entidad afectada, el registro, quién hizo el cambio, el tipo de acción (alta, modificación, baja lógica, reactivación, baja física, ingreso, ingreso fallido o salida), el origen (un usuario, un proceso automático del sistema o un cambio hecho directamente sobre la base de datos) y el período. |
| 6 | El sistema aplica la misma restricción por distribuidora. Los registros que no pertenecen a ninguna distribuidora —los de la persona o globales, como las cuentas de usuario, los clientes y los roles— solo los ve el Administrador General. |
| 7 | El sistema muestra las auditorías que coinciden, de la más reciente a la más antigua, con el total. Cada una trae el tipo de acción, el usuario (nombre y correo, aunque después se lo haya dado de baja; vacío si el cambio lo hizo el sistema), la distribuidora, la entidad afectada, el registro, el origen, la dirección de red, el momento y sus detalles: por cada campo que cambió, el valor anterior y el nuevo. |
| 8 | El administrador puede abrir una sola auditoría con todos sus detalles y ver el catálogo de acciones. |
| 9 | El administrador puede exportar la auditoría de datos que coincide con los filtros, en formato de planilla de texto separado por comas o de Excel. |

**Postcondición:** Ninguna: la consulta no modifica nada. La propia consulta no genera un asiento, porque leer no es una operación de escritura.

**Excepciones**

| Paso | Acción |
|------|--------|
| 1 | Si el solicitante es un cliente o un chofer, el sistema deniega la consulta. |
| 2 | Si un filtro no tiene el formato esperado —un autor que no es válido, un resultado distinto de éxito o falla, una fecha inválida, un tamaño de página fuera de 1 a 200 o un dato no previsto—, el sistema rechaza la consulta. |
| 2 | Si la fecha de inicio es posterior a la de fin, el sistema no lo rechaza: ningún asiento cae en ese período y la respuesta es una lista vacía. |
| 3 | Si ningún asiento coincide con los filtros, el sistema muestra una lista vacía con total cero. No es un error. |
| 5 | Si un filtro de la auditoría de datos no tiene el formato esperado —un usuario inválido, un tipo de acción fuera de los ocho, un origen distinto de los tres, una fecha inválida, un tamaño de página fuera de 1 a 200 o un dato no previsto—, el sistema rechaza la consulta. |
| 5 | Si el solicitante es un cliente o un chofer, el sistema deniega la consulta también de la auditoría de datos. |
| 8 | Si la auditoría pedida no existe o es de otra distribuidora, el sistema informa «Auditoría no encontrada», sin distinguir los casos. |
| 1 | El sistema no ofrece ninguna operación de modificación ni de borrado sobre la bitácora ni sobre la auditoría de datos, para ningún rol. |

**Rendimiento**

| Paso | Cota de tiempo |
|------|----------------|
| 4 | 2 segundos |

| Campo | Detalle |
|-------|---------|
| **Frecuencia** | Baja: se consulta ante una disputa o una sospecha, no a diario. |
| **Estabilidad** | Alta |
| **Comentarios** | El registro se consulta pero no se administra: no hay alta, modificación ni baja, y la base de datos rechaza toda modificación y todo borrado de un asiento, también los que se intenten directamente sobre ella. El panel ofrece la pantalla de consulta en la sección de auditoría, con una solapa para los cambios de datos y otra para las operaciones. La depuración por antigüedad no está construida; si llega a hacer falta, será una tarea programada del sistema y no una operación del administrador, justamente para que nadie pueda borrar el asiento que lo incrimina. Quién y cuándo lo hizo son datos que el sistema registra solo en cada operación que modifica datos (requisito de trazabilidad NFR-10). |

---

## 9. Requisitos No Funcionales

### Crítico NFR-01 — Seguridad

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-01, OBJ-05 |
| **Requisitos asociados** | IRQ-01, IRQ-09, CU-001 |
| **Descripción** | El sistema debe garantizar que cada usuario solo acceda a las funciones y a los datos que corresponden a su rol (cliente, chofer, administrador o Administrador General). Toda solicitud y toda conexión en tiempo real deben estar autenticadas. La identidad se delega en un proveedor de identidad externo: el sistema no guarda contraseñas ni emite credenciales propias, y verifica la identidad y el rol en cada solicitud. |
| **Estabilidad** | Alta |
| **Comentarios** | Las limitaciones conocidas respecto de este requisito se registran en el campo Comentarios de los casos de uso afectados. El requisito describe la meta; su cumplimiento efectivo es parcial. |

### Crítico NFR-02 — Rendimiento

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-01, OBJ-03 |
| **Requisitos asociados** | IRQ-02, CU-005, CU-013, CU-017 |
| **Descripción** | El sistema debe responder con tiempos que no degraden la experiencia del usuario: el ingreso, en menos de 3 segundos; la creación de un pedido, en menos de 5 segundos; la búsqueda de los choferes cercanos, en menos de medio segundo; la actualización de la posición del chofer, en menos de una décima de segundo; el catálogo de productos, en menos de 2 segundos; y el tablero, en menos de 3 segundos. El cliente debe recibir cada cambio de estado de su pedido y la posición del chofer en tiempo real, sin consultar. |
| **Estabilidad** | Alta |
| **Comentarios** | Las cotas de tiempo se declaran caso por caso en el campo Rendimiento de cada caso de uso expandido. Son estimaciones de diseño: no se realizó una campaña de medición formal sobre el sistema desplegado. |

### Importante NFR-03 — Disponibilidad

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-01, OBJ-02 |
| **Requisitos asociados** | IRQ-15, CU-104 |
| **Descripción** | El sistema debe estar disponible durante el horario operativo del distribuidor (estimado de 8:00 a 21:00) y volver a funcionar solo ante una caída, sin intervención de una persona. El mantenimiento programado se hace fuera del horario operativo. |
| **Estabilidad** | Alta |
| **Comentarios** | El sistema expone sondas de vida y de disponibilidad que verifican base de datos, cache, memoria y disco (CU-104). No hay redundancia de instancias ni conmutación automática ante falla, de modo que la disponibilidad depende de un único nodo. |

### Importante NFR-04 — Escalabilidad

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-05 |
| **Requisitos asociados** | IRQ-09, IRQ-15, CU-104 |
| **Descripción** | La arquitectura debe admitir el crecimiento de la cantidad de usuarios, distribuidoras y pedidos sin rediseño: debe poder sumar instancias del servidor sin perder avisos en tiempo real, y separar la base de datos y el caché en equipos propios si el volumen lo requiere. |
| **Estabilidad** | Alta |
| **Comentarios** | La arquitectura es un monolito modular sin estado en el proceso: la sesión se valida contra el proveedor de identidad y el estado compartido vive en la base y en el caché. Eso habilita agregar instancias detrás de un balanceador sin rediseño, aunque se ejecuta una sola. |

### Importante NFR-05 — Portabilidad

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-01 |
| **Requisitos asociados** | CU-002, CU-005 |
| **Descripción** | Las aplicaciones móviles deben funcionar en los sistemas operativos móviles más usados por el mercado objetivo: Android 8.0 o superior e iOS 14 o superior, desde una misma base de código. |
| **Estabilidad** | Alta |
| **Comentarios** | Las dos aplicaciones móviles se construyen con Flutter desde una única base de código, lo que da soporte simultáneo a Android e iOS. El panel de administración es una aplicación web y queda fuera del alcance de este requisito. |

### Importante NFR-06 — Usabilidad

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-01 |
| **Requisitos asociados** | CU-005, CU-044, CU-046 |
| **Descripción** | Las interfaces deben ser intuitivas para usuarios con conocimientos tecnológicos básicos, el perfil típico del cliente de una distribuidora de gas: hacer un pedido no debe requerir más de cinco pasos; los avisos deben usar un lenguaje claro, en español rioplatense; los estados del pedido deben distinguirse a simple vista, con íconos y colores; y la aplicación del chofer debe permitir cada acción de una entrega con no más de tres toques. |
| **Estabilidad** | Alta |
| **Comentarios** | Los wireframes de las pantallas están en el documento de diseño. No se realizaron pruebas de usabilidad con usuarios reales: el requisito se sostiene por criterio de diseño y no por evidencia empírica. |

### Importante NFR-07 — Mantenibilidad

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-05 |
| **Requisitos asociados** | CU-104 |
| **Descripción** | El sistema debe ser comprensible, modular y fácil de modificar para agregar funcionalidades en fases posteriores: organizado en módulos por dominio, con la interfaz separada de la lógica del negocio en las aplicaciones y en el panel, y con un esquema de base de datos que evoluciona por migraciones versionadas. |
| **Estabilidad** | Alta |
| **Comentarios** | El núcleo de pedidos sigue una separación en dominio, aplicación e infraestructura; el resto de los módulos mantiene una estructura de servicio y controlador más directa. La suite de pruebas del backend cubre el comportamiento de los casos críticos. |

### Importante NFR-08 — Confiabilidad

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-06, OBJ-04 |
| **Requisitos asociados** | IRQ-02, IRQ-04, CU-005, CU-008 |
| **Descripción** | El sistema debe garantizar la integridad de los datos críticos —stock, pedidos y dinero— aun ante fallas parciales: la reserva de stock al crear un pedido y su restitución al cancelarlo se hacen en una única operación indivisible que impide que dos pedidos simultáneos se lleven la misma garrafa; no puede quedar stock comprometido sin un pedido válido; y los importes se calculan con aritmética decimal exacta. |
| **Estabilidad** | Alta |
| **Comentarios** | La reserva de stock al crear el pedido es exclusiva: dos pedidos simultáneos no pueden llevarse la misma garrafa. La cancelación del pedido es una única operación indivisible. La asignación de envases es atómica: CU-135 valida todos los envases antes de asignar. |

### Crítico NFR-09 — Aislamiento entre Distribuidoras

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-09, OBJ-05 |
| **Requisitos asociados** | IRQ-01, IRQ-02, IRQ-03, IRQ-07, IRQ-09, NFR-01; los casos de uso de gestión que operan sobre pedidos, choferes, vehículos, clientes, direcciones de entrega, reclamos, incidencias, notificaciones y administradores |
| **Descripción** | Con una distribuidora en contexto, el sistema debe comportarse como si los datos de las demás distribuidoras no existieran: quien opera para una empresa no puede leer ni modificar lo que pertenece a otra, ni enterarse de que existe. La distribuidora en contexto es la del administrador de empresa o la del chofer, o la que eligió el Administrador General; sin distribuidora elegida, el Administrador General opera sobre todas. Un recurso de otra distribuidora se trata igual que uno inexistente. El cliente no pertenece a ninguna distribuidora, porque puede comprarle a varias: para cada distribuidora, sus clientes son los que le compraron al menos una vez, y la cuenta del cliente la administran el propio cliente o el Administrador General. |
| **Estabilidad** | Alta |
| **Comentarios** | El requisito se verifica con una batería automática de 205 casos contra el sistema en ejecución: siembra datos en una segunda distribuidora y comprueba, operación por operación, que el administrador, el chofer y el cliente de la primera, y el Administrador General que opera sobre ella, no los alcanzan. La corrida del 25/09/2026 terminó con los 205 casos aprobados. Cada caso de uso afectado describe su control en sus precondiciones y excepciones. |

### Crítico NFR-10 — Trazabilidad y Auditoría

| Campo | Detalle |
|-------|---------|
| **Objetivos asociados** | OBJ-04, OBJ-05 |
| **Requisitos asociados** | IRQ-16, NFR-01, NFR-09 |
| **Descripción** | El sistema debe dejar constancia, sin que nadie lo pida, de todo cambio de datos —alta, modificación, baja lógica, reactivación o baja física— con quién lo hizo, cuándo, desde dónde, con qué origen y, por cada campo, el valor anterior y el nuevo; de cada ingreso al sistema, correcto o fallido, y de cada salida; y de cada operación de escritura, exitosa o rechazada. Ese registro no se puede modificar, borrar ni vaciar. Este requisito reemplaza al caso de uso retirado «Registrar Toda Operación de Escritura»: es una propiedad transversal del sistema y no un proceso que inicie un actor. |
| **Estabilidad** | Alta |
| **Comentarios** | Lo registra la propia base de datos, con un disparador en cada tabla y dentro de la misma operación que hace el cambio: alcanza también a los procesos automáticos y a un cambio hecho directamente sobre la base. Quedan fuera, deliberadamente, los registros que ya son un historial de solo agregado (el historial de estados del pedido, los movimientos de los envases y del stock) y la posición del chofer, que cambia a cada instante. El registro crece con el uso y su plazo de conservación no está definido; la depuración por antigüedad, cuando exista, será un proceso del sistema y nunca una operación disponible para un usuario. La consulta, con filtros y exportación, es el caso de uso CU-152. |

---

## 10. Matriz de Rastreabilidad Objetivos / Requisitos

La matriz relaciona cada requisito con los objetivos del sistema que contribuye a alcanzar: primero los
19 requisitos de información (RI), después los requisitos funcionales (RF), que son los 21 casos de uso
expandidos de la sección 8.3, y por último los 10 requisitos no funcionales (RNF). Las marcas de los
casos de uso se derivan del campo **Objetivos asociados** que cada uno declara.

|  | OBJ-01 | OBJ-02 | OBJ-03 | OBJ-04 | OBJ-05 | OBJ-06 | OBJ-07 | OBJ-08 | OBJ-09 | OBJ-10 | OBJ-11 | OBJ-12 | OBJ-13 | OBJ-14 | OBJ-15 |
|--|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
| **IRQ-01** | ● |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |
| **IRQ-02** | ● | ● |  |  |  | ● |  |  |  |  |  |  |  |  |  |
| **IRQ-03** |  | ● |  |  | ● |  |  |  |  |  |  |  |  |  |  |
| **IRQ-04** |  |  |  |  |  | ● | ● |  |  |  |  |  |  |  |  |
| **IRQ-05** | ● |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |
| **IRQ-06** |  |  |  | ● | ● |  |  |  |  |  |  |  |  |  |  |
| **IRQ-07** | ● | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **IRQ-08** |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |
| **IRQ-09** |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |
| **IRQ-10** |  |  |  |  |  |  |  |  | ● | ● |  |  |  |  |  |
| **IRQ-11** |  |  |  | ● |  |  |  |  |  |  | ● |  |  |  |  |
| **IRQ-12** |  |  |  | ● |  |  |  |  |  |  |  | ● |  |  |  |
| **IRQ-13** |  |  |  | ● |  |  |  |  |  |  |  |  | ● |  |  |
| **IRQ-14** |  |  |  |  |  | ● | ● |  |  |  |  |  |  | ● |  |
| **IRQ-15** |  |  |  |  | ● |  |  |  |  |  |  |  |  |  | ● |
| **IRQ-16** |  |  |  | ● | ● |  |  |  |  |  |  |  |  |  |  |
| **IRQ-17** |  |  |  |  | ● |  |  |  | ● |  |  |  |  |  |  |
| **IRQ-18** |  |  |  |  | ● | ● |  |  |  |  |  |  |  |  |  |
| **IRQ-19** |  |  |  |  | ● |  | ● |  |  |  |  |  |  |  |  |
| **CU-001** | ● | ● |  |  | ● |  |  |  |  |  |  |  |  |  |  |
| **CU-002** | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **CU-005** | ● | ● |  |  |  | ● | ● |  |  |  |  |  |  |  |  |
| **CU-008** | ● |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |
| **CU-013** |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **CU-014** |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **CU-015** |  | ● | ● |  |  |  |  |  |  |  |  |  |  |  |  |
| **CU-017** |  | ● | ● |  |  |  |  |  |  |  |  |  |  |  |  |
| **CU-022** |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **CU-023** |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |
| **CU-025** |  |  |  | ● | ● |  |  |  |  |  |  |  |  |  |  |
| **CU-048** |  | ● |  |  |  |  | ● |  |  |  |  |  |  |  |  |
| **CU-078** |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |
| **CU-079** |  |  | ● | ● |  |  | ● |  |  |  |  |  |  |  |  |
| **CU-105** |  | ● |  |  | ● |  |  |  |  |  |  |  |  |  |  |
| **CU-106** | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **CU-107** |  | ● |  |  |  |  |  | ● |  |  |  |  |  |  |  |
| **CU-108** |  |  |  | ● | ● |  |  |  |  |  |  |  |  |  |  |
| **CU-152** |  |  |  | ● | ● |  |  |  |  |  |  |  |  |  |  |
| **CU-292** |  |  |  | ● |  |  | ● |  |  |  |  |  |  |  |  |
| **CU-301** |  |  |  | ● |  |  | ● |  |  |  |  |  |  |  |  |
| **NFR-01** | ● |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |
| **NFR-02** | ● |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |
| **NFR-03** | ● | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **NFR-04** |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |
| **NFR-05** | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **NFR-06** | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **NFR-07** |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |
| **NFR-08** |  |  |  | ● |  | ● |  |  |  |  |  |  |  |  |  |
| **NFR-09** |  |  |  |  | ● |  |  |  | ● |  |  |  |  |  |  |
| **NFR-10** |  |  |  | ● | ● |  |  |  |  |  |  |  |  |  |  |

El símbolo ● indica que el requisito contribuye al objetivo de esa columna.

---

## 11. Glosario de Términos

| Término | Categoría | Comentarios |
|---------|-----------|-------------|
| Garrafa | Dominio | Recipiente metálico presurizado que contiene gas licuado de petróleo. Se comercializa por peso: 10 kg, 15 kg y 45 kg. Es el producto principal del sistema. |
| Envase | Dominio | El recipiente físico individual, identificado por su número de serie, que se entrega al cliente y se espera recuperar vacío. El cliente compra un producto (la garrafa) pero recibe un envase concreto. |
| Distribuidora | Dominio | Empresa que comercializa y reparte garrafas de gas. Varias distribuidoras operan sobre la misma instancia del sistema con sus datos aislados. |
| Chofer | Actor | Repartidor de la distribuidora, encargado de llevar y entregar las garrafas en el domicilio del cliente con la aplicación del chofer. |
| Administrador | Actor | Persona que gestiona una distribuidora desde el panel de administración. |
| Administrador General | Actor | Persona que opera la plataforma sobre todas las distribuidoras; especializa al Administrador. |
| Pedido | Dominio | Solicitud de compra de un cliente: productos y cantidades, dirección de entrega, medio de pago y, si corresponde, franja horaria. |
| Estado del pedido | Dominio | Etapa en la que está un pedido: pendiente (recién creado, sin chofer), aceptado (un chofer lo tomó), en camino, entregado o cancelado. Cada cambio queda en el historial de estados. |
| Franja horaria | Dominio | Rango de horas del día habilitado para las entregas (por ejemplo, mañana de 9 a 13), con una capacidad máxima de pedidos por día. |
| Zona de cobertura | Dominio | Área dentro de la cual la distribuidora acepta pedidos, con el recargo que corresponde a cada una. |
| Stock | Dominio | Cantidad de garrafas disponibles para la venta. Se reserva al crear un pedido y se restituye si el pedido se cancela. |
| Despacho automático | Proceso | Proceso que ofrece cada pedido nuevo al chofer disponible más cercano, de a uno por vez y con una vigencia acotada, ampliando el radio de búsqueda si nadie acepta (módulo M1). |
| Oferta de despacho | Proceso | Propuesta que el sistema le hace a un chofer para que tome un pedido, con un plazo para aceptarla o rechazarla. |
| Disponibilidad del chofer | Proceso | Condición del chofer en línea, que lo hace candidato a recibir ofertas de pedidos. |
| Código de entrega | Dominio | Código secreto de seis dígitos que el sistema genera al aceptarse el pedido y que el cliente confirma al recibirlo, escaneando el QR que le muestra el chofer o escribiendo el número que este le dicta. Es la prueba objetiva de la entrega. |
| Cobro en efectivo | Proceso | Confirmación, por parte del chofer, de que cobró en mano el importe de un pedido entregado. |
| Transferencia | Proceso | Pago de un pedido por transferencia bancaria, que el administrador confirma al verificar el comprobante. |
| Pasarela de pago | Integración | Servicio externo que procesa el cobro en línea (MercadoPago) y avisa al sistema el resultado. |
| Recargo | Dominio | Importe que se suma al pedido según la zona de entrega, la modalidad express o el pago en línea. |
| Reclamo | Dominio | Queja formal del cliente sobre un pedido entregado, con una fotografía opcional como evidencia, que gestiona y resuelve el administrador. |
| Seña | Dominio | Pago parcial que el cliente deja en garantía al reservar garrafas para una fecha futura. |
| Rendición | Proceso | Cierre diario del dinero que cobró un chofer, que el administrador revisa y aprueba para que entre a la caja. |
| Caja | Dominio | Registro del dinero de la distribuidora —efectivo, banco o billetera— con su saldo y su libro de movimientos. |
| Módulo inteligente | Proceso | Proceso automatizado que decide por su cuenta, se parametriza por distribuidora y nunca ejecuta sin una persona lo que compromete dinero. El sistema tiene cinco: M1 a M5. |
| Ventana de taller | Proceso | Fecha y horario propuestos para llevar un vehículo al taller sin dejar la zona sin vehículos (módulo M2). |
| Invitación de recompra | Proceso | Propuesta de reposición que el sistema le envía al cliente cuando estima que se le acaba el gas, con el pedido ya armado (módulo M3). |
| Lote de recorrido | Proceso | Conjunto de pedidos programados cercanos que se ofrece completo a un chofer, con sus paradas ordenadas (módulo M4). |
| Caso de recupero | Proceso | Seguimiento de un envase que un cliente retiene más allá del plazo de tolerancia, con avisos escalonados y la decisión final del administrador (módulo M5). |
| Auditoría | Dominio | Registro de todo cambio de datos, de cada ingreso al sistema y de cada operación de escritura, que nadie puede modificar ni borrar. |
| Baja lógica | Dominio | Baja que conserva el registro, marcado como dado de baja, en lugar de borrarlo. Toda baja del sistema es lógica y queda auditada. |
| Proveedor de identidad | Integración | Servicio externo (Firebase) que verifica la identidad del usuario al ingresar. El sistema no guarda contraseñas. |
| Notificación | Integración | Aviso que el sistema envía al dispositivo del usuario o por correo, aun con la aplicación cerrada. |
