# Plan del Proyecto
**Proyecto:** SPLG – Sistema de Pedidos y Logística de Garrafas de Gas  
**Versión:** 2.0
**Fecha:** 2026-10-15
**Realizado por:** Nahuel Wagner  
**Realizado para:** Distribuidor de Gas Envasado (Cliente Real)  
**Institución:** FCEQyN – UNaM  
**Metodología:** Proceso Unificado (PU)

---


## Índice de Figuras

- Figura 1 — Cronograma del proyecto: diagrama de Gantt
- Figura 2 — Actores del sistema y el canal por el que operan
- Figura 3 — Diagrama de casos de uso del sistema por subsistemas
- Figura 4 — Diagrama de casos de uso del sistema (todos los casos de uso)
- Figura 5 — Diagrama de casos de uso, lámina 1 de 28: Actores del sistema y generalización de ACT-05 en ACT-03
- Figura 6 — Diagrama de casos de uso, lámina 2 de 28: Cliente (ACT-01), parte 1 de 3
- Figura 7 — Diagrama de casos de uso, lámina 3 de 28: Cliente (ACT-01), parte 2 de 3
- Figura 8 — Diagrama de casos de uso, lámina 4 de 28: Cliente (ACT-01), parte 3 de 3
- Figura 9 — Diagrama de casos de uso, lámina 5 de 28: Chofer (ACT-02), parte 1 de 2
- Figura 10 — Diagrama de casos de uso, lámina 6 de 28: Chofer (ACT-02), parte 2 de 2
- Figura 11 — Diagrama de casos de uso, lámina 7 de 28: Administrador (ACT-03), parte 1 de 13
- Figura 12 — Diagrama de casos de uso, lámina 8 de 28: Administrador (ACT-03), parte 2 de 13
- Figura 13 — Diagrama de casos de uso, lámina 9 de 28: Administrador (ACT-03), parte 3 de 13
- Figura 14 — Diagrama de casos de uso, lámina 10 de 28: Administrador (ACT-03), parte 4 de 13
- Figura 15 — Diagrama de casos de uso, lámina 11 de 28: Administrador (ACT-03), parte 5 de 13
- Figura 16 — Diagrama de casos de uso, lámina 12 de 28: Administrador (ACT-03), parte 6 de 13
- Figura 17 — Diagrama de casos de uso, lámina 13 de 28: Administrador (ACT-03), parte 7 de 13
- Figura 18 — Diagrama de casos de uso, lámina 14 de 28: Administrador (ACT-03), parte 8 de 13
- Figura 19 — Diagrama de casos de uso, lámina 15 de 28: Administrador (ACT-03), parte 9 de 13
- Figura 20 — Diagrama de casos de uso, lámina 16 de 28: Administrador (ACT-03), parte 10 de 13
- Figura 21 — Diagrama de casos de uso, lámina 17 de 28: Administrador (ACT-03), parte 11 de 13
- Figura 22 — Diagrama de casos de uso, lámina 18 de 28: Administrador (ACT-03), parte 12 de 13
- Figura 23 — Diagrama de casos de uso, lámina 19 de 28: Administrador (ACT-03), parte 13 de 13
- Figura 24 — Diagrama de casos de uso, lámina 20 de 28: Administrador General (ACT-05), parte 1 de 3
- Figura 25 — Diagrama de casos de uso, lámina 21 de 28: Administrador General (ACT-05), parte 2 de 3
- Figura 26 — Diagrama de casos de uso, lámina 22 de 28: Administrador General (ACT-05), parte 3 de 3
- Figura 27 — Diagrama de casos de uso, lámina 23 de 28: Sistema Automático (ACT-04)
- Figura 28 — Diagrama de casos de uso, lámina 24 de 28: Operador Técnico (ACT-10)
- Figura 29 — Diagrama de casos de uso, lámina 25 de 28: MercadoPago (ACT-06)
- Figura 30 — Diagrama de casos de uso, lámina 26 de 28: Firebase (ACT-07)
- Figura 31 — Diagrama de casos de uso, lámina 27 de 28: Servicio de correo (ACT-08)
- Figura 32 — Diagrama de casos de uso, lámina 28 de 28: Plataforma de despliegue (ACT-09)
- Figura 33 — Mapa de navegación del sistema (no es un diagrama UML)

---

## Lista de Cambios

| Nro | Fecha | Descripción | Autor |
|-----|-------|-------------|-------|
| 0 | 2026-04-16 | Versión inicial | Nahuel Wagner |
| 1 | 2026-04-16 | Se incorporan las 2 apps móviles y se ajustan iteraciones de Construcción a 5 | Nahuel Wagner |
| 2 | 2026-05-03 | Nombre corregido a SPLG, Gantt con fechas reales, tabla de actores ampliada, CUs de alto nivel completos, tabla de calificación completa | Nahuel Wagner |
| 3 | 2026-08-30 | Revisión de los casos de uso de alto nivel y de su calificación contra el sistema construido. | Nahuel Wagner |
| 4 | 2026-10-01 | Casos de uso de alto nivel CU-161 a CU-167: vehículo en uso por chofer y reclamos. | Nahuel Wagner |
| 5 | 2026-10-01 | Casos de uso de alto nivel CU-168 a CU-175: reintegro de pagos, historial de estados del pedido, configuración de procesos y de tareas programadas, y fotografía del reclamo. Estado y iteración de cada caso en el catálogo. Plan de construcción de los casos de uso planificados (I-1 a I-10) y decisiones de diseño incorporadas. | Nahuel Wagner |
| 6 | 2026-10-01 | Cronograma como diagrama de Gantt con las seis iteraciones de Construcción, las diez iteraciones de los casos planificados y los hitos; fechas de las fases alineadas con la Planificación de Iteraciones; despliegue en un servidor virtual con Docker Compose. | Nahuel Wagner |
| 7 | 2026-10-01 | Cierre de la documentación: los 195 casos de uso con sus cuatro artefactos, el catálogo de 194 operaciones del sistema y las cifras del plan coherentes con los Documentos 1, 2 y 3 y con el sistema construido. | Nahuel Wagner |
| 8 | 2026-10-01 | Revisión final: mapa del sistema como diagrama principal y diagrama completo como lámina anexa, actor ACT-09 (plataforma de despliegue), cronograma con I-1, I-2, I-3 e I-5 cerrando en C-06 y el resto postergado, recargo del 10 % del pago en línea, catálogo de 194 operaciones. | Nahuel Wagner |
| 9 | 2026-10-03 | Módulo de Personal: casos de uso de alto nivel CU-176 a CU-194 y CU-246 (subsistema SS-19, iteración I-11), con su fila en el catálogo, su plan de construcción y su barra en el cronograma. | Nahuel Wagner |
| 10 | 2026-10-03 | Módulo de flota ampliada: casos de uso de alto nivel CU-195 a CU-206 y CU-247 (combustible, multas, siniestros, costos y neumáticos), iteración I-12 y calificación de los casos nuevos. | Nahuel Wagner |
| 11 | 2026-10-03 | Módulo de stock y compras: casos de uso de alto nivel CU-207 a CU-224 y CU-248 a CU-250 (stock físico por depósito y camión, compras a proveedores, carga y rendición del camión), subsistema SS-20 e iteración I-13. | Nahuel Wagner |
| 12 | 2026-10-03 | Módulo de caja y rendición: casos de uso de alto nivel CU-225 a CU-245 (subsistema SS-21, iteración I-14) y catálogo de los casos de uso hasta CU-250. | Nahuel Wagner |
| 13 | 2026-10-07 | Los casos de uso que agrupaban varias operaciones de un ABM se parten en un caso de uso por operación, con su propia asociación del actor y con la consulta como «include» de la modificación y de la baja: CU-251 a CU-272 (22 casos nuevos; CU-004, CU-022, CU-032, CU-033, CU-040, CU-050, CU-083, CU-089, CU-176, CU-207, CU-214, CU-225 y CU-230 pasan a nombrar su primera operación) y catálogo de 278 casos de uso. | Nahuel Wagner |
| 14 | 2026-10-07 | Personal construido en el backend: puestos de trabajo y legajos (CU-176 a CU-182, CU-186 y CU-255 a CU-257) pasan a «Implementado» —CU-178, CU-180 y CU-181 con funcionalidad planificada—, con sus diagramas, contratos y tablas verificados contra el código y la API; las jornadas, las licencias y el resto de SS-19 siguen planificados. | Nahuel Wagner |
| 15 | 2026-10-11 | Stock físico construido en el backend: depósitos, ubicaciones, saldos, libro de movimientos, conteo inicial, ajustes, transferencias, mínimos y conciliación (CU-207 a CU-213, CU-220, CU-224, CU-250, CU-258 a CU-260 y CU-273 a CU-279) pasan a «Implementado», con sus diagramas, contratos y tablas verificados contra el código y la API; se suman siete casos de uso (CU-273 a CU-279) y CU-020, CU-038 y CU-079 quedan conectados al descuento del stock físico. Las compras y la carga del camión siguen planificadas. | Nahuel Wagner |
| 16 | 2026-10-11 | Compras construidas en el backend: proveedores, órdenes de compra, recepciones y costo promedio (CU-214 a CU-217 y CU-261 a CU-263) pasan a «Implementado», con sus diagramas, contratos y tablas verificados contra el código y la API; se suman nueve casos de uso (CU-280 a CU-288): anular una recepción, marcar su pago, cerrar una orden con faltante, modificar y enviar una orden, y las consultas de órdenes, recepciones, costo promedio e historial de un proveedor, que salían de CU-215 y CU-217. La carga del camión sigue planificada. | Nahuel Wagner |
| 17 | 2026-10-12 | Carga y rendición del camión construidas en el backend: CU-218, CU-219 y CU-221 a CU-223 pasan a «Implementado», con el control del despacho por carga abierta (CU-248 y CU-249) y tres casos nuevos (CU-289 a CU-291); el catálogo llega a 290 casos de uso. | Nahuel Wagner |
| 18 | 2026-10-14 | Documentación al día con el sistema: CU-020 pasa a ser del administrador (el chofer ya no cierra la entrega), CU-292 a CU-294 (cobro en efectivo: confirmar, informar el impago y resolverlo), CU-218 partido en CU-218, CU-295 y CU-296, y la consulta de CU-210 y CU-249 en CU-297 y CU-298 (295 → 303 casos de uso); retiro de ofertas en CU-012 y CU-015; I-13 con 50 casos y quince tablas. | Nahuel Wagner |
| 19 | 2026-10-14 | Blindaje de pedidos, cobros y stock: CU-299 a CU-304 (cobros manuales del administrador, cotización, ruta de un pedido y cobros pendientes), CU-169 implementado, datos del chofer y quién canceló en el detalle del pedido, 410 al chofer que tuvo el pedido, X-Distributor obligatorio para el administrador general en las escrituras, mensajes 401 propios del inicio de sesión y del token, y las reglas de stock del 14/10 (déficit de reservas, costo promedio exacto, transiciones de la carga en 409, clave de idempotencia obligatoria); 297 → 303 casos de uso (CU-299 a CU-304). | Nahuel Wagner |
| 20 | 2026-10-14 | Revisión integral: 303 → 340 casos de uso. Un caso de uso por operación (CU-305 a CU-341: polígonos de cobertura, caja, personal, flota, compras, cuentas corrientes y pedidos, con la modificación del pedido por el cliente y la cotización de edición), cobros en SS-14, CU-169 como caso incluido, plan e iteraciones con su estado real, y «Aprobar», «Crear» y «Tablero» en los nombres. | Nahuel Wagner |
| 21 | 2026-10-14 | Revisión independiente: 340 casos de uso (CU-001 a CU-343, sin CU-021 y CU-091, retirados por no ser casos de uso, ni CU-093), actor ACT-10 Operador Técnico, activar y desactivar franja (CU-342 y CU-343), transición desplazada a después de la construcción (T-01 del 21/12/2026 al 19/02/2027) y formato único de actores. | Nahuel Wagner |
| 22 | 2026-10-15 | Módulo inteligente M1 construido: CU-171 y CU-173 pasan a «Implementado» (parámetros del despacho y frecuencia de las tareas programadas por distribuidora), con sus endpoints, campos, validaciones y mensajes verificados contra el código y la API; CU-014 refleja el aviso `order:no-drivers` y el ciclo por distribuidora. | Nahuel Wagner |
| 23 | 2026-10-15 | Plan con las cuatro fases del Proceso Unificado: los catorce paquetes de casos de uso dejan de estar anidados en C-06 y pasan a ser las iteraciones C-07 a C-20 de la Fase de Construcción, con un solo calendario (documentos 0 y 0.1), fechas reales de lo construido y estimadas para lo pendiente, toda la construcción antes de la Transición y sin la fila «Construcción posterior a la defensa»; CU-043, CU-171 y CU-173 figuran como construidos; actor ACT-10 en la tabla de actores, con los tipos del Documento 1 y descripción ampliada de los diez actores. | Nahuel Wagner |
| 24 | 2026-10-16 | Pasada de coherencia: las iteraciones se identifican solo como C-07 a C-20 (el paquete de la sección 4 es el nombre de cada conjunto de casos), CU-103 retirado por duplicar CU-343 (334 casos de uso, diez retirados) y casos retirados fuera del catálogo. | Nahuel Wagner |
| 25 | 2026-10-18 | Casos de uso construidos el 17/10/2026 pasan a «Implementado» en el catálogo (CU-122 a CU-128, CU-132 a CU-135, CU-143, CU-144, CU-147 a CU-149, CU-151, CU-168, CU-172, CU-183 a CU-206, CU-225 a CU-247, CU-264, CU-265, CU-268, CU-269, CU-309, CU-310, CU-313 a CU-335 y CU-340); plan de construcción y cronograma con las fechas reales; quedan planificados seis casos (CU-105 a CU-108, CU-145 y CU-146). Calendario: la construcción termina el 20/11/2026 con C-19 y la transición va del 23/11/2026 al 22/01/2027; 338 casos de uso con CU-345 a CU-348. | Nahuel Wagner |
| 26 | 2026-10-22 | Auditoría de contenido: el actor ACT-04 se define como el Tiempo (actor externo, convención de Larman); el alcance pendiente se distingue entre ampliaciones planificadas con iteración (CU-017, CU-116, CU-118) y mejoras diferidas a Trabajo futuro (CU-013, CU-180, CU-181). Re-auditoría: ACT-04 como el Tiempo, con CU-013 como excepción documentada. | Nahuel Wagner |
| 27 | 2026-10-22 | Cuentas de clientes: CU-050, CU-270 y CU-085 suman al Administrador General (ACT-05) junto al Administrador (ACT-03), que no administra la cuenta de un cliente, y CU-131 pasa a ACT-05; conteos por actor y láminas al día. | Nahuel Wagner |
| 28 | 2026-10-22 | Reservas contra el panel: el CUA de CU-072 suma que el administrador también crea la reserva, con la seña acotada al total; el de CU-073, la franja y el enlace de pago; el de CU-074, que la seña se confirma en efectivo o por transferencia y la de MercadoPago sólo por la pasarela; el de CU-006, el enlace de pago. | Nahuel Wagner |

---

## 1. Componentes del Sistema

El sistema SPLG está compuesto por **4 componentes** que trabajan en conjunto:

| Componente | Tecnología | Descripción |
|------------|-----------|-------------|
| **Backend API** | NestJS (TypeScript) | Servidor principal. Gestiona toda la lógica de negocio, base de datos PostgreSQL, caché Redis, WebSockets y notificaciones push. |
| **App Cliente** | Flutter (iOS / Android) | App móvil para usuarios finales. Permite realizar pedidos, elegir franjas horarias, pagar y hacer seguimiento en tiempo real del repartidor en el mapa. |
| **App Chofer** | Flutter (Android) | App móvil para repartidores. Recibe pedidos cercanos mediante WebSocket, actualiza ubicación GPS, gestiona el estado de la entrega y confirma la recepción. |
| **Panel Administrativo** | React + Vite (Web) | Panel web para el operador del distribuidor. Gestiona choferes, vehículos, productos, stock, precios, franjas horarias, reclamos y reportes. |

---

## 2. Plan de las Fases

El desarrollo se lleva a cabo en las cuatro fases del Proceso Unificado, con una o más iteraciones en cada una. La tabla muestra la distribución de tiempos y el número de iteraciones de cada fase.

| Fase | Nro. Iteraciones | Duración | Período |
|------|:---------------:|:--------:|---------|
| Fase de Inicio | 0 | 3 semanas | 07/04/2026 – 28/04/2026 |
| Fase de Elaboración | 1 (E-01) | 3 semanas | 28/04/2026 – 19/05/2026 |
| Fase de Construcción | 20 (C-01 a C-20) | 26 semanas | 19/05/2026 – 20/11/2026 |
| Fase de Transición | 1 (T-01) | 9 semanas | 23/11/2026 – 22/01/2027 |

La Fase de Construcción reúne las iteraciones C-01 a C-05, que llevaron al Release 2.0, y las iteraciones C-06 a C-20, que construyen el alcance ampliado. Estas últimas se superponen en parte, porque el trabajo avanza en carriles que tocan módulos distintos del sistema; todas terminan el 20/11/2026, antes de que empiece la Fase de Transición. Cada iteración desde C-07 construye un paquete de casos de uso; la sección 4 da la correspondencia.

---

## 3. Hitos por Fase

Los hitos que marcan el final de cada fase se describen en la siguiente tabla.

| Fase | Descripción | Hito |
|------|-------------|------|
| Fase de Inicio | Identificación del escenario real (distribuidor de gas con operación telefónica y sin trazabilidad), relevamiento de necesidades con el cliente, identificación de actores y casos de uso principales, redacción de la Propuesta de Proyecto y presentación del Plan del Proyecto. | Plan del Proyecto aprobado por el docente (28/04/2026). |
| Fase de Elaboración | Análisis de los casos de uso arquitectónicamente más críticos (CU-001, CU-005, CU-013, CU-017, CU-020); definición y validación de la arquitectura técnica (NestJS, Flutter, React, PostgreSQL, Redis, Firebase Auth); Modelo Conceptual preliminar; prototipo de arquitectura que valida el despacho automático con Redis GEORADIUS. | Arquitectura validada con el cliente y prototipo funcional demostrado (19/05/2026). |
| Fase de Construcción | C-01: autenticación con Firebase Auth, roles y base del backend. C-02: pedidos con reserva atómica de stock y despacho automático por geolocalización. C-03: seguimiento GPS en tiempo real y App Chofer. C-04: reclamos, reportes, tablero, vehículos, notificaciones y Panel Admin. C-05: App Cliente completa. C-06: alcance ampliado, con el modelo de datos, el registro de auditoría y el mantenimiento de la flota. C-07 a C-20: construcción de los paquetes de casos de uso planificados: cimientos y huecos cortos (C-07), personal y legajos (C-08), stock y compras (C-09), pedido en curso (C-10), vigencia de envases (C-11), carrito persistente (C-12), consumo declarado (C-13), módulo M2 de flota (C-14), módulo M5 de recupero de envases (C-15), módulo M3 de recompra (C-16), compra express y reintegros (C-17), flota ampliada (C-18), módulo M4 de recorridos (C-19) y caja y rendición (C-20). | Release 2.0 al cierre de C-05 (08/09/2026); al 15/10/2026 están construidos los paquetes de stock y compras (C-09) y parte de C-07, C-08 y C-10; toda la construcción termina el 18/12/2026, con la última iteración (C-20), antes de empezar la Transición. |
| Fase de Transición | Pruebas de aceptación con usuarios reales (choferes y clientes del distribuidor), corrección de los defectos detectados, despliegue en producción (Docker Compose sobre un servidor virtual, VPS) y entrega de la documentación (manuales de usuario y guías de despliegue). | Sistema en producción, usuarios capacitados y documentación entregada (19/02/2027). |

---

## 4. Calendario del Proyecto — Diagrama de Gantt

El cronograma abarca **41 semanas**, desde el **07/04/2026** hasta el **22/01/2027**. Es el único calendario del proyecto: el documento 0.1 (Planificación de Iteraciones) usa las mismas fechas para cada iteración. Los días sábado y domingo no se cuentan como laborables. Las fechas de lo ya construido son las del historial de los repositorios del sistema; las de lo pendiente son estimaciones al 15/10/2026 que respetan las dependencias entre iteraciones.

### Cronograma (Diagrama de Gantt)

![Cronograma del proyecto: diagrama de Gantt](../diagramas/uml/UML_Gantt.png)

**Figura 1 — Cronograma del proyecto: diagrama de Gantt**


Las barras de color pleno son las fases y las iteraciones de Construcción hasta C-06; las iteraciones C-07 a C-20 se dibujan en dos tonos: más oscuro las que ya empezaron y más claro las pendientes. Las iteraciones construidas en un solo día (17/10/2026: C-11, C-12, C-17, C-18 y C-20) se dibujan como un rombo, porque ese día es sábado y una barra no tendría ancho. Los rombos son los hitos: Plan del Proyecto aprobado (28/04/2026), arquitectura validada (19/05/2026), Release 2.0 (08/09/2026), construcción terminada (20/11/2026) y sistema en producción (22/01/2027). La columna Duración cuenta días corridos.

| Fase | Iteración | Paquete de casos de uso | Desde | Hasta | Duración (días corridos) | Estado al 17/10/2026 | Hito de cierre |
|------|:---------:|:-----------------------:|:-----:|:-----:|:--------:|---|----------------|
| Inicio | — | — | 07/04/2026 | 28/04/2026 | 21 días (3 semanas) | Cerrada | Plan del Proyecto aprobado |
| Elaboración | E-01 | — | 28/04/2026 | 19/05/2026 | 21 días (3 semanas) | Cerrada | Arquitectura validada y prototipo demostrado |
| Construcción | C-01 | — | 19/05/2026 | 02/06/2026 | 14 días (2 semanas) | Cerrada | Autenticación, roles y base del backend |
| Construcción | C-02 | — | 02/06/2026 | 23/06/2026 | 21 días (3 semanas) | Cerrada | Pedidos, stock atómico y despacho automático |
| Construcción | C-03 | — | 23/06/2026 | 14/07/2026 | 21 días (3 semanas) | Cerrada | Seguimiento en tiempo real y App Chofer |
| Construcción | C-04 | — | 14/07/2026 | 04/08/2026 | 21 días (3 semanas) | Cerrada | Reclamos, reportes, tablero y Panel |
| Construcción | C-05 | — | 04/08/2026 | 08/09/2026 | 35 días (5 semanas) | Cerrada | App Cliente y Release 2.0 |
| Construcción | C-06 | — | 09/09/2026 | 30/09/2026 | 21 días (3 semanas) | Cerrada | Modelo de datos del alcance ampliado, registro de auditoría y mantenimiento de la flota |
| Construcción | C-07 | C-07 | 01/10/2026 | 17/10/2026 | 16 días | Cerrada: construida | Cimientos y huecos cortos |
| Construcción | C-08 | C-08 | 04/10/2026 | 17/10/2026 | 13 días | Cerrada: construida; lo que falta de CU-180 y CU-181 pasó a Trabajo futuro (Doc 3, §10) | Personal y legajos |
| Construcción | C-09 | C-09 | 11/10/2026 | 14/10/2026 | 3 días | Cerrada | Stock, compras y carga del camión |
| Construcción | C-10 | C-10 | 14/10/2026 | 29/10/2026 (estimada) | 15 días | En curso: construidos los nueve casos; quedan planificados los tramos de CU-017, CU-116 y CU-118 | Pedido en curso |
| Construcción | C-11 | C-11 | 17/10/2026 | 17/10/2026 | 1 día | Cerrada: construida | Vigencia de envases |
| Construcción | C-12 | C-12 | 17/10/2026 | 17/10/2026 | 1 día | Cerrada: construida | Carrito persistente |
| Construcción | C-13 | C-13 | 17/10/2026 | 26/10/2026 (estimada) | 9 días | En curso: construidos CU-143 y CU-144; CU-145 y CU-146 siguen planificados | Consumo declarado |
| Construcción | C-14 | C-14 | 19/10/2026 (estimada) | 30/10/2026 (estimada) | 11 días | Pendiente | Módulo M2: flota |
| Construcción | C-15 | C-15 | 26/10/2026 (estimada) | 02/11/2026 (estimada) | 7 días | Pendiente | Módulo M5: recupero de envases |
| Construcción | C-16 | C-16 | 27/10/2026 (estimada) | 03/11/2026 (estimada) | 7 días | Pendiente | Módulo M3: recompra |
| Construcción | C-17 | C-17 | 17/10/2026 | 17/10/2026 | 1 día | Cerrada: construida | Compra express y reintegros |
| Construcción | C-18 | C-18 | 17/10/2026 | 17/10/2026 | 1 día | Cerrada: construida | Flota ampliada |
| Construcción | C-19 | C-19 | 11/11/2026 (estimada) | 20/11/2026 (estimada) | 9 días | Pendiente | Módulo M4: agrupación por recorrido |
| Construcción | C-20 | C-20 | 17/10/2026 | 17/10/2026 | 1 día | Cerrada: construida | Caja y rendición |
| Transición | T-01 | — | 23/11/2026 | 22/01/2027 | 61 días (9 semanas) | Pendiente | Sistema en producción y usuarios capacitados |

### Plan de construcción de los casos de uso planificados

El sistema construido no realiza seis casos de uso, que están especificados con sus artefactos completos y figuran como «Planificado» en el catálogo de la sección 8: los cuatro módulos inteligentes (CU-105, CU-106, CU-107 y CU-108) y los dos casos de recompra del cliente (CU-145 y CU-146). Los demás casos que la documentación venía señalando como no construidos se construyeron: la modificación de la franja horaria (CU-043) el 07/10/2026; el historial de estados (CU-169 y CU-170) el 14/10/2026; los parámetros del despacho y de las tareas programadas (CU-171 y CU-173) el 15/10/2026; y el 17/10/2026 todos los de las iteraciones C-11, C-12, C-17, C-18 y C-20, los de C-07 (CU-151, CU-172, CU-268 y CU-269), C-08 (personal), C-10 (CU-127 y CU-128) y C-13 (CU-143 y CU-144). Lo pendiente de los casos construidos se distingue en dos clases. Tres tienen una ampliación planificada con su iteración (C-10): el tiempo estimado de llegada (CU-017) y la resolución de la dirección contra el servicio de mapas (CU-116 y CU-118). Otros tres tienen una mejora diferida a Trabajo futuro (Documento 3, §10), sin iteración asignada: el estado de la documentación en el listado de empleados (CU-180), el egreso del chofer con una rendición pendiente (CU-181) y la admisión de los choferes que están por terminar su entrega en la asignación automática (CU-013). La fotografía del reclamo (CU-174 y CU-175, y el tramo de CU-023) ya está construida. Cada caso muestra su estado en el catálogo y en su caso de uso expandido: «Planificado (C-n)» mientras no se construye, e «Implementado» cuando se construyó.

El plan agrupa los casos en catorce paquetes, I-1 a I-14, de acuerdo con el módulo del sistema que tocan y con sus dependencias, y construye cada uno en una iteración de la Fase de Construcción (C-07 a C-20).

| Iteración | Paquete | Casos de uso | Tamaño | Qué se puede mostrar al cerrarla |
|---|:---:|---|:---:|---|
| **C-07** Cimientos y huecos cortos | I-1 | CU-043, CU-151, CU-171, CU-172, CU-173; CU-268 y CU-269 (reactivación de un producto dado de baja y listado de los dados de baja) | M | La franja se edita sin darla de baja; una zona vencida se desactiva sola; los parámetros del despacho, de los procesos automáticos y de las tareas programadas se editan desde el panel; un producto dado de baja vuelve al catálogo. Construidos: la modificación de la franja (CU-043, 07/10/2026) y los parámetros del despacho (CU-171) y la frecuencia de las tareas programadas (CU-173), el 15/10/2026; el 17/10/2026, la desactivación de las zonas vencidas (CU-151), los parámetros de los procesos automáticos (CU-172) y la reactivación de productos (CU-268 y CU-269). |
| **C-08** Personal y legajos | I-11 | CU-176 a CU-194, CU-246, CU-255 a CU-257 y CU-311 a CU-319 | L+ | El administrador lleva el legajo de cada persona de la distribuidora, su asistencia y sus licencias, y un chofer con la documentación vencida o con licencia aprobada queda fuera del despacho. Construido desde el 04/10/2026: puestos, legajos, egreso y cuenta de acceso; el 17/10/2026, la documentación, la asistencia, las licencias, el saldo de vacaciones, el tablero y la habilitación laboral del chofer. Quedan diferidos a Trabajo futuro (Documento 3, §10) el estado de la documentación en el listado de empleados (CU-180) y el egreso con una rendición pendiente (CU-181). |
| **C-09** Stock y compras | I-13 | CU-207 a CU-224, CU-248 a CU-250, CU-258 a CU-263 y CU-273 a CU-301 y CU-304; CU-038 (ajuste de stock) y CU-020 (descuento del stock al entregar) | L+ | El administrador ve el stock físico por depósito y por camión, compra a una planta de llenado y recibe el remito, carga el camión, lo rinde al volver y el sistema concilia el stock vendible con el físico. Construido el 11/10/2026 (stock físico y compras), el 12/10/2026 (carga y rendición del camión) y el 14/10/2026 (cobros y blindaje). |
| **C-10** Pedido en curso | I-4 | CU-127, CU-128, CU-169, CU-170, CU-302, CU-303, CU-338, CU-339 y CU-341 | M | El cliente cambia la dirección de un pedido en curso y el chofer lo ve, con quién recibe; el cliente y el administrador ven el historial de estados del pedido; la cotización y la ruta de un pedido las calcula el sistema, el chofer retoma su pedido en curso al abrir la aplicación y el administrador y el cliente editan un pedido pendiente. Construido el 14/10/2026: el historial de estados (CU-169 y CU-170), la cotización, la ruta, el pedido en curso del chofer y la edición del pedido pendiente (del administrador y del cliente); el 17/10/2026, el cambio de dirección y quién recibe el pedido. Quedan planificados el tiempo estimado de llegada (CU-017) y la resolución de la dirección contra el servicio de mapas (CU-116 y CU-118). |
| **C-11** Vigencia de envases | I-2 | CU-132, CU-133, CU-134, CU-135 | M | Un envase con la revisión vencida no puede asignarse a ningún pedido. Construida el 17/10/2026. |
| **C-12** Carrito persistente | I-3 | CU-122, CU-123, CU-124, CU-125, CU-126 | L | El cliente arma el carrito, cierra la app, la vuelve a abrir y el carrito sigue ahí. Construida el 17/10/2026 en el backend. |
| **C-13** Consumo declarado y reclamos con imagen | I-5 | CU-143, CU-144, CU-145, CU-146 | M | El administrador ve qué clientes se quedan sin gas esta semana. Construidos el 17/10/2026 CU-143 y CU-144; CU-145 y CU-146 siguen planificados. |
| **C-14** Módulo M2: flota | I-10 | CU-105 | L+ | El planificador propone una ventana de taller al chofer y escala si se agotan las alternativas. |
| **C-15** Módulo M5: recupero de envases | I-8 | CU-108 | L | Un envase retenido abre su caso, escala y el administrador lo resuelve. |
| **C-16** Módulo M3: recompra | I-6 | CU-106 | L | Un cliente recibe la invitación a reponer y, al aceptarla, el pedido entra al despacho. |
| **C-17** Compra express y reintegros | I-7 | CU-148, CU-147, CU-149, CU-168; CU-008 y CU-010 (reintegro) | L | Un pedido express sale a un chofer en moto o se degrada a reparto común avisándole al cliente; el pago de un pedido cancelado se devuelve por la pasarela. Construida el 17/10/2026. |
| **C-18** Flota ampliada | I-12 | CU-195 a CU-206, CU-247 y CU-320 a CU-328 | L | El administrador y el chofer registran las cargas de combustible, las multas y los siniestros de cada vehículo, y el administrador ve el costo y el rendimiento de cada unidad y de toda la flota. Construida el 17/10/2026. |
| **C-19** Módulo M4: agrupación por recorrido | I-9 | CU-107 | L | Tres pedidos programados cercanos se ofrecen como un solo recorrido ordenado. |
| **C-20** Caja y rendición | I-14 | CU-225 a CU-245, CU-264, CU-265, CU-309, CU-310, CU-329 a CU-335 y CU-340 | L+ | El administrador abre y cierra la caja con arqueo, el chofer rinde su cobranza del día y el administrador la aprueba; un cliente compra a cuenta corriente y paga después; las entregas devengan comisiones que se liquidan y se pagan desde una caja. Construida el 17/10/2026. |

El tamaño es relativo, para una persona, e incluye el backend, el panel, las aplicaciones y la prueba
contra el sistema en funcionamiento: S hasta un día, M de dos a cuatro días, L de cuatro a siete días y
L+ más de siete.

**Iteración C-08: Personal y legajos.** A diferencia de las que cierran lo que el sistema ya tenía especificado, la C-08 incorpora un módulo de gestión de la distribuidora: el personal. Son los veintitrés casos de uso CU-176 a CU-194, CU-246 y CU-255 a CU-257 del subsistema SS-19, con sus cinco artefactos. **Está construida:** los once casos de los puestos de trabajo y de los legajos (CU-176 a CU-182, CU-186 y CU-255 a CU-257, con las tablas `job_position` y `employee`) pasaron a «Implementado» desde el 04/10/2026, y el 17/10/2026 los demás —la documentación con vencimiento, la asistencia, las licencias, el saldo de vacaciones, el tablero y la habilitación laboral del chofer: CU-183 a CU-185, CU-187 a CU-194, CU-246 y CU-313 a CU-319—, con las tablas `employee_attendance` y `employee_leave` y las columnas nuevas de `maintenance_plan` y `maintenance_task` que hacen que la documentación con vencimiento del personal (curso de mercancías peligrosas, examen psicofísico y alta en la ART; la licencia de conducir ya existía) reutilice los planes, las tareas, los adjuntos, el aviso diario y el bloqueo de despacho de la flota. CU-180 y CU-181 conservan una mejora diferida a Trabajo futuro (Documento 3, §10). No hay roles nuevos: el personal administrativo que entra al panel es un administrador, y ayudantes, depósito y vendedores son legajos sin cuenta. Se estimó en 12 jornadas de una persona (tres de tablas y alta unificada del chofer, de dos a tres de documentación y bloqueo de despacho, dos de asistencia y licencias, de tres a cuatro de panel, más las pruebas contra el sistema en funcionamiento) y se construyó entre el 04/10/2026 y el 17/10/2026. Depende de los adjuntos genéricos y de la numeración del legajo. Modifica casos existentes sin reescribirlos: el alta de un chofer (CU-031) crea además su legajo en la misma transacción (construido); la licencia de conducir (CU-138) sigue colgando del perfil de reparto del chofer y se une con el legajo en la ficha, el tablero y el bloqueo; el tablero y el aviso de vencimientos de la flota (CU-139, CU-142) suman a las personas; y el bloqueo de despacho (CU-012, CU-013 y CU-015, que incluyen el caso nuevo CU-246) considera también las licencias aprobadas y el estado del legajo.

**Iteración C-18: Flota ampliada.** Suma los doce casos CU-195 a CU-206 y el caso CU-247 (Reactivar un Vehículo), más los nueve de las operaciones por separado (CU-320 a CU-328), al subsistema SS-07, con sus cinco artefactos y su modelo de datos: las tablas `fuel_load`, `traffic_fine`, `vehicle_accident`, `tire` y `tire_event`, y las columnas nuevas de `car` (migración `FlotaAmpliada`). **Está construida desde el 17/10/2026**, en el backend y en el panel, incluida la funcionalidad opcional de neumáticos: el chofer y el administrador registran las cargas de combustible, las multas y los siniestros de cada vehículo, y el administrador ve el costo y el rendimiento de cada unidad y de toda la flota. Depende del legajo del personal (C-08) y de los adjuntos genéricos, tiene tamaño L y se estimó del 06/11/2026 al 19/11/2026.

**Iteración C-09: Stock y compras.** Incorpora el stock físico por depósito y por camión, las compras a plantas de llenado y la carga y rendición del camión: los cincuenta y cuatro casos CU-207 a CU-224, CU-258 a CU-263, CU-273 a CU-301 y CU-304 (subsistemas SS-08 ampliado, SS-20 Compras y, para el cobro del efectivo, SS-14 y SS-06) y los tres casos incluidos CU-248 (verificar la carga de camión abierta), CU-249 (configurar ese control) y CU-250 (aplicar un movimiento de stock), con quince tablas nuevas. **Está construida entre el 11 y el 14/10/2026:** el stock físico —veintiún casos de uso (CU-207 a CU-213, CU-220, CU-224, CU-250, CU-258 a CU-260, CU-273 a CU-279 y CU-297), con las tablas `warehouse`, `stock_location`, `stock_balance`, `stock_movement`, `stock_adjustment`, `stock_adjustment_item`, `stock_threshold` y `stock_reconciliation_alert`— pasó a «Implementado» el 11/10/2026, con CU-020, CU-038 y CU-079 ya conectados a él, y las compras —dieciséis casos de uso (CU-214 a CU-217, CU-261 a CU-263 y CU-280 a CU-288), con las tablas `supplier`, `purchase_order`, `purchase_order_item`, `purchase_receipt` y `purchase_receipt_item`— pasaron a «Implementado» el mismo día y la carga y la rendición del camión —trece casos de uso (CU-218, CU-219, CU-221 a CU-223, CU-248, CU-249, CU-289 a CU-291, CU-295, CU-296 y CU-298), con las tablas `truck_load` y `truck_load_item`— pasaron a «Implementado» el 12/10/2026. El cobro en efectivo de lo entregado (CU-292 a CU-294: el chofer confirma lo cobrado o informa el impago, y el administrador lo resuelve) alimenta el efectivo de la jornada de la rendición y está construido desde el 11/10/2026. El blindaje de cobros del 14/10/2026 suma los cobros manuales del administrador (CU-299 a CU-301) y los cobros pendientes (CU-304, SS-06). La cotización de un pedido (CU-302), la ruta de un pedido (CU-303), el pedido en curso del chofer (CU-338), la edición del administrador (CU-339) y el historial de estados (CU-169 y CU-170) pertenecen a C-10. Modifica casos existentes sin reescribirlos: el ajuste de stock (CU-038) y el descuento del camión al entregar (CU-020), el despacho (CU-012, CU-013, CU-015 y CU-080), que controla la carga del chofer, y el cambio de vehículo (CU-161 y CU-162), que se bloquea con una carga abierta. Depende de la numeración correlativa por distribuidora y del evento de pedido entregado, que ya están implementados; tiene tamaño L+. Lo que depende de la caja —cargar al chofer la diferencia de una rendición— se construyó en la iteración C-20.

**Módulo de caja y rendición (C-20).** A los casos planificados se suman los treinta y tres casos del subsistema SS-21 Caja, Rendiciones y Cuentas Corrientes (CU-225 a CU-245, CU-264, CU-265, CU-309, CU-310, CU-329 a CU-335 y CU-340), un caso por operación, que no tienen construcción previa y se agrupan en una única iteración. Depende de la tanda de cimientos de los módulos de empresa (numeración correlativa por distribuidora, adjuntos genéricos y evento de pedido entregado) y del vehículo en uso del chofer; las comisiones por entrega y los cargos a cuenta se asientan al entregar el pedido. Se construyó el 17/10/2026, después de las iteraciones C-08, C-09 y C-18, porque las comisiones se anclan en el legajo del personal: cinco módulos (`cash`, `driver-settlement`, `customer-account`, `commission` y `finance`), tres procesos temporales (a las 23:30, las 08:00 y las 03:30, hora de Argentina) y las pantallas del panel. Su tamaño estimado era L+ (más de siete jornadas). Lo que queda fuera: la rendición propia y las comisiones en la App Chofer, el egreso de caja de las cargas de combustible, de las multas imputadas y de los pagos de compras, y el ingreso a caja del cobro que registra un administrador sobre un pedido en efectivo.

**Piezas transversales.** La primera iteración del plan (C-07) construye cuatro piezas que reutilizan las siguientes.
La primera es la configuración de procesos por distribuidora: la tabla ya existe y falta el servicio
que la lee y la valida, con un esquema de validación por proceso; sin ella la compra express y los
cuatro módulos inteligentes quedarían con parámetros fijos en el código, que es lo que el criterio de
parametrización del proyecto no admite. La segunda es el evento de dominio de pedido entregado, que
necesitan el recálculo de la recompra, el registro de uso de la flota y el recupero de envases. La
tercera es la plantilla del proceso temporal con cerrojo distribuido, que estrena la desactivación de
zonas vencidas (CU-151) con el caso más simple y repiten los módulos inteligentes; para los procesos
cuya frecuencia u hora es configurable por distribuidora, el decorador de la tarea es un tic fijo y
cada ejecución evalúa adentro, contra la configuración y la última corrida de cada distribuidora, a
quién le toca. La cuarta son los datos de demostración: cada iteración suma al juego de datos lo que su
caso necesita para verse.

**Dependencias y orden.** C-07 no depende de nada. C-15 depende de C-11, porque comparte el módulo y el
ciclo del envase. C-16 depende de C-13, por el consumo declarado y el aviso de recompra, y del evento de
pedido entregado de C-07. C-10 depende de C-12, porque el cambio de dirección se ofrece sobre el pedido que sale del carrito. C-17 depende de C-12 y de C-10, porque la modalidad se elige dentro de la compra desde el
carrito y el reintegro actúa sobre el pedido en curso, y del vehículo en uso del chofer (CU-161 a CU-165). C-19 y C-14 dependen del vehículo en uso,
para conocer la capacidad de carga y el kilometraje, y C-19 depende además de C-17, porque los pedidos
express no se agrupan. C-18 depende de C-08, por el legajo del empleado, y C-20 de C-08, C-09 y C-18. En el diseño de datos, los cambios que no están en la base se reparten
entre las iteraciones que los necesitan: la columna del recargo express y la baja del envase y el pedido del aviso de recupero en C-15, y los dos valores
nuevos de la configuración de procesos en C-07.

**Carga estimada.** Al 18/10/2026 queda por hacer el trabajo de los cuatro módulos inteligentes
(C-14, 10 jornadas de una persona; C-15, 6; C-16, 6; C-19, 8), los dos casos de recompra del cliente de C-13
(unas 3) y los tramos de C-10 (unas 3), contra 25 jornadas laborables hasta el 20/11/2026. Por eso las
iteraciones se superponen y el trabajo se reparte en carriles que tocan módulos distintos del backend
—envases (C-15), pedido (C-10 y C-19), cliente (C-13 y C-16) y flota (C-14)—. La última iteración de
construcción es C-19, que termina el 20/11/2026, y la Transición empieza el 23/11/2026. Si el avance
real se atrasa, se recortan primero los módulos inteligentes (C-19, C-14 y C-15); dentro de C-14, lo
primero que se posterga es la negociación de ventana, el bloqueo del vehículo y la captura de kilómetros.

**Decisiones de diseño incorporadas.** Los casos planificados recogen las siguientes decisiones, que
quedaron escritas en sus casos de uso expandidos, diagramas y contratos.

| Decisión | Casos de uso |
|---|---|
| Si la capacidad nueva de una franja es menor que lo ya agendado para algún día desde hoy, se rechaza el cambio (409). | CU-043 |
| El carrito no fija el precio: se cobra el precio vigente del catálogo y se avisa la diferencia antes de confirmar. | CU-122, CU-125, CU-126 |
| Si el pedido está pagado en línea y el recargo de la zona de la dirección nueva cambia, se rechaza el cambio de dirección; en efectivo se recalcula el total. | CU-127 |
| Los datos de quien recibe se conservan hasta que vence el plazo de reclamo y después se anulan; el documento queda fuera del registro de auditoría. | CU-128 |
| El envase lo elige una persona por número de serie y el sistema valida la elección; el bloqueo alcanza al despacho y no al llenado. | CU-132, CU-135 |
| Un envase rechazado en la revisión queda con el vencimiento en la fecha de la revisión. | CU-132 |
| La estimación de recompra vive en un módulo propio que depende de `customer`, para no crear un ciclo con `order`. | CU-143 a CU-146, CU-106 |
| Un cliente pertenece a una distribuidora desde su primera compra: aparece en el listado de recompras y recibe invitaciones desde entonces. | CU-146, CU-106 |
| La cobertura express es un radio máximo en la configuración del proceso, no una zona aparte; la modalidad se guarda al crear el pedido. | CU-147, CU-148 |
| Si el pedido express no consigue chofer en moto, pasa a reparto común: se descuenta el recargo express del total y, si ya se pagó en línea, se reintegra esa parte. | CU-149, CU-168 |
| Solo se agrupan los pedidos programados con franja futura; los inmediatos los atiende M1. | CU-107 |
| El depósito de un envase no devuelto se registra con la decisión y el importe, y se cobra aparte, en el próximo pedido o en efectivo, sin pasarela. | CU-108 |
| La zona de un vehículo se deriva de las zonas donde entregó en los últimos días; el chofer acepta la ventana de taller y el administrador confirma el gasto. | CU-105 |

---

## 5. Actores del Sistema

| Código | Actor | Tipo | Descripción |
|--------|-------|:----:|-------------|
| ACT-01 | **Cliente** | Humano | Usuario final que compra garrafas de gas. Usa la aplicación del cliente en su teléfono: hace pedidos, elige la franja de entrega y el medio de pago, sigue el pedido en el mapa, administra sus direcciones y puede reclamar si algo sale mal. Inicia 48 casos de uso. |
| ACT-02 | **Chofer** | Humano | Repartidor de la distribuidora. Usa la aplicación del chofer en su teléfono: se pone en línea, recibe las ofertas de pedidos cercanos, las acepta o las rechaza, informa su posición, entrega y rinde lo cobrado. Inicia 45 casos de uso. |
| ACT-03 | **Administrador** | Humano | Operador de una distribuidora, con alcance acotado a su propia empresa. Usa el panel web para gestionar choferes, vehículos, productos, stock, compras, personal, caja, cuentas corrientes, franjas horarias, reclamos y reportes. Tiene acceso total dentro de su distribuidora, salvo la cuenta de un cliente, que administra el Administrador General. Inicia 248 casos de uso. |
| ACT-04 | **Sistema Automático** | Automático | Actor externo que representa el Tiempo, según la convención de Larman: el reloj o temporizador que dispara los casos de uso programados —el vencimiento de las ofertas de despacho, la activación y el vencimiento de las reservas, los avisos y las conciliaciones, y las revisiones periódicas de los cinco procesos automatizados: asignación secuencial de pedidos, planificación predictiva del mantenimiento, anticipación de la recompra, agrupación de pedidos por recorrido y recuperación de envases no devueltos— sin que los inicie una persona ni un sistema externo. Lo que el backend hace al ser disparado es comportamiento del sistema, no del actor. Única excepción documentada: la primera oferta de CU-013 sale por dentro de CU-005, al confirmarse el alta del pedido; se mantiene bajo este actor porque sus reintentos los dispara el reloj (CU-014). Es el actor principal de 22 casos de uso. |
| ACT-05 | **Administrador General** | Humano | Operador de la plataforma, con alcance sobre todas las distribuidoras. Especializa al Administrador: hace todo lo que éste hace y además lo que es exclusivo de la plataforma —dar de alta las distribuidoras, designar a sus administradores y administrar los roles—. Es el único actor cuyo alcance no está acotado a una distribuidora; cuando escribe sobre pedidos, cobros, incidencias, reclamos, adjuntos o las cuentas del personal de una empresa, debe indicar con qué distribuidora trabaja: sin esa indicación el sistema no escribe nada. Participa en 71 casos de uso. |
| ACT-06 | **MercadoPago** | Secundario (sistema externo) | Pasarela de cobro, externa al sistema. El sistema le pide el cobro de cada pedido o seña que se paga por ese medio y recibe de ella el aviso de pago aprobado. Inicia CU-048 con ese aviso y participa como actor secundario en CU-005, CU-072 y CU-147. |
| ACT-07 | **Firebase** | Secundario (sistema externo) | Servicio externo de identidad y mensajería. Verifica quién es el usuario que ingresa, crea y deshabilita cuentas, genera el enlace de recuperación de contraseña y entrega las notificaciones a los dispositivos. No inicia ningún caso de uso; participa como actor secundario en CU-001, CU-004, CU-005, CU-013, CU-014, CU-015, CU-016, CU-018, CU-019, CU-020, CU-047, CU-072, CU-079, CU-082, CU-085, CU-100, CU-101 y CU-147. |
| ACT-08 | **Servicio de correo** | Secundario (sistema externo) | Servicio externo que envía los correos del sistema: bienvenida al cliente, recuperación de contraseña, prueba del servicio y avisos de vencimientos, de stock bajo, de rendiciones sin cerrar y de multas por vencer. No inicia ningún caso de uso; participa como actor secundario en CU-002, CU-047, CU-102, CU-142, CU-188, CU-211, CU-224, CU-234 y CU-326. |
| ACT-09 | **Plataforma de despliegue** | Primario (sistema externo) | Orquestador de contenedores, balanceador de carga o servicio de monitoreo, externo al sistema, que sondea el estado del backend para decidir si le envía tráfico o si reinicia la instancia. Es quien inicia CU-104. |
| ACT-10 | **Operador Técnico** | Humano | Persona con acceso al servidor donde corre el sistema, que lo pone en marcha. No usa el panel ni las aplicaciones: ejecuta una orden en el servidor para crear la cuenta inicial. Es quien inicia CU-087. |


![Actores del sistema y el canal por el que operan](../diagramas/uml/CU_Sistema_Actores.png)

**Figura 2 — Actores del sistema y el canal por el que operan**

> Los cinco actores humanos operan siempre a través de una aplicación o del panel web, salvo el Operador Técnico,
> que lo hace desde una consola del servidor; ninguno accede directamente a la base de datos. El Sistema
> Automático no tiene interfaz: son los procesos que el backend dispara por sí mismo, y es el
> actor principal de los casos de uso que la documentación marca como automáticos.
> MercadoPago, Firebase y el servicio de correo son sistemas externos que el backend invoca:
> participan como actores secundarios y no inician ningún caso de uso. La plataforma de
> despliegue es un sistema externo que, al revés, es quien consulta el estado del backend.
> El Operador Técnico es una persona que no usa ninguna aplicación: trabaja en el servidor y
> sólo interviene en la puesta en marcha.


### Descripción Ampliada de Actores

**ACT-01 — Cliente:**
Persona que contrata el servicio de entrega de garrafas. Perfil tecnológico variado (usuarios con conocimientos básicos de teléfonos inteligentes). Accede al sistema únicamente desde la App Cliente Flutter. Sus principales necesidades son: realizar pedidos rápidamente, conocer el estado en tiempo real y poder reclamar si algo sale mal. Inicia los casos de uso de la compra, el seguimiento del pedido, las direcciones y los reclamos, y sólo ve sus propios datos.

**ACT-02 — Chofer:**
Empleado del distribuidor que ejecuta las entregas físicas. Trabaja principalmente en horario de 9 a 21 hs. Maneja la App Chofer en un dispositivo Android provisto por el distribuidor. Su principal necesidad es recibir pedidos de forma ordenada, conocer la ruta y confirmar entregas de manera simple. Inicia los casos de uso de su disponibilidad, la aceptación y el avance de cada pedido, el cobro en efectivo y su vehículo; no recibe pedidos hasta que el administrador lo habilita.

**ACT-03 — Administrador:**
Operador de oficina de una distribuidora. Su alcance está acotado a la empresa a la que pertenece: no ve ni gestiona datos de otras distribuidoras. Puede ser una o más personas. Accede al Panel Web desde una PC o computadora portátil con conexión a internet. Sus principales necesidades son: visibilidad completa del estado operativo, control de inventario y reportes de ventas para la toma de decisiones.

**ACT-04 — Sistema Automático:**
No es un actor humano ni el conjunto de procesos del backend: es el Tiempo, el actor «Tiempo» de Larman (el reloj o temporizador), externo al sistema. Se mantiene como actor porque el paso del tiempo es lo que dispara esos casos de uso desde fuera; lo que el backend hace al ser disparado es comportamiento del sistema. Son cinco los **procesos automatizados** que el reloj pone en marcha: la negociación secuencial de asignación de pedidos (M1), la planificación predictiva de mantenimiento y habilitaciones de flota (M2), la anticipación de recompra por consumo estimado (M3), la agrupación inteligente de pedidos por recorrido (M4) y la recuperación de envases no devueltos (M5). Su especificación completa está en el Documento 3, sección 6. Hay una excepción documentada: la primera oferta de CU-013 sale por dentro de CU-005, al confirmarse el alta del pedido, porque un evento interno de otro caso de uso no es un actor; el caso queda bajo el Tiempo porque sus reintentos y vencimientos los dispara el reloj (CU-014).

No hay que confundirlos con las tareas de mantenimiento del propio sistema, que también corren solas pero no deciden nada: vencer una oferta de despacho y devolver el pedido al circuito, activar una reserva que llegó a su fecha, liberar el stock de un pedido que caducó sin pagarse. Son la ejecución programada de los circuitos que los procesos automatizados gobiernan, no procesos en sí mismos. Los tres módulos que deciden por su cuenta —M2, M3 y M5— siempre proponen y nunca ejecutan: la contratación de un taller, el cobro de un depósito y la baja de un envase los confirma una persona.

**ACT-05 — Administrador General:**
Responsable de la plataforma, distinto del administrador de cada empresa. Da de alta las distribuidoras que operan en el sistema, designa a sus administradores y define los roles disponibles. Es el único actor que ve datos de más de una distribuidora; todos los demás quedan confinados a la suya. Accede por el mismo panel web, con un alcance ampliado. Especializa al Administrador: en los diagramas se une a todos sus casos de uso, también a los que comparte con el Administrador, y la generalización entre los dos se mantiene.

**ACT-06 — MercadoPago:**
Pasarela de cobro, externa al sistema. Cuando un pedido o una seña se paga por ese medio, el sistema le pide el cobro y espera su aviso de pago aprobado, que es lo que inicia el caso de uso de confirmación del pago. No tiene interfaz propia dentro del sistema y no decide nada: informa el resultado de un cobro.

**ACT-07 — Firebase:**
Servicio externo de identidad y mensajería. El sistema no guarda las contraseñas: le delega la verificación de quién es cada usuario, la creación y el bloqueo de cuentas y la recuperación de la contraseña, y le entrega las notificaciones para que lleguen a los dispositivos. Nunca inicia un caso de uso.

**ACT-08 — Servicio de correo:**
Servicio externo que envía los correos del sistema. Participa cuando un caso de uso necesita avisar por correo —bienvenida, recuperación de contraseña, avisos diarios de vencimientos, de stock bajo, de rendiciones sin cerrar y de multas por vencer— y no inicia ningún caso de uso.

**ACT-09 — Plataforma de despliegue:**
Orquestador de contenedores, balanceador de carga o servicio de monitoreo, externo al sistema. Consulta periódicamente si el sistema está vivo y disponible para decidir si le envía tráfico o si reinicia la instancia. Es actor principal del caso de uso de verificación de la salud del sistema.

**ACT-10 — Operador Técnico:**
Persona con acceso al servidor donde corre el sistema. Interviene solo en la puesta en marcha: crea la primera cuenta de Administrador General con una orden ejecutada en el servidor, porque no existe ninguna operación pública para hacerlo. No usa el panel ni las aplicaciones.

---

**ACT-06 — MercadoPago:**
Pasarela de cobro externa. El sistema le crea el checkout de cada pedido o seña que se paga en línea y recibe de ella el aviso de pago aprobado; no tiene interfaz propia dentro del sistema. Es actor primario sólo de CU-048, que inicia cuando avisa el pago, y participa como secundario en CU-005, CU-072 y CU-147.

**ACT-07 — Firebase:**
Servicio externo de identidad y mensajería. El sistema le pide crear y deshabilitar cuentas, verificar el token de identidad en cada solicitud y generar el enlace de recuperación de contraseña, y le entrega las notificaciones que llegan a los dispositivos. No inicia ningún caso de uso: es siempre un actor secundario.

**ACT-08 — Servicio de correo:**
Servicio externo que envía los correos transaccionales: bienvenida al cliente, recuperación de contraseña, prueba del servicio y avisos de vencimientos de la flota y del personal. No inicia ningún caso de uso ni recibe respuestas del usuario.

**ACT-09 — Plataforma de despliegue:**
Sistema externo de operación (orquestador de contenedores, balanceador de carga o servicio de monitoreo) que consulta periódicamente el estado del backend para decidir si le envía tráfico o si reinicia la instancia. Es quien inicia CU-104. No maneja datos del negocio.

**ACT-10 — Operador Técnico:**
Persona con acceso al servidor donde corre el sistema, responsable de ponerlo en marcha. No usa el panel ni las aplicaciones: ejecuta por consola el comando de alta inicial, que crea la primera cuenta de administrador general (CU-087), porque el sistema no ofrece ninguna operación pública para hacerlo. Interviene una sola vez por instalación.

## 6. Diagrama de Casos de Uso del Sistema

Con 338 casos de uso, el diagrama de casos de uso del sistema se presenta en dos niveles, ambos en notación UML. La figura principal es el **diagrama por subsistemas**: los 21 subsistemas dibujados como paquetes dentro del límite del sistema y los actores fuera de él, cada uno unido a los subsistemas en los que participa; el Administrador General especializa al Administrador. El detalle —los 338 casos de uso, uno por uno, con sus relaciones «include» y «extend»— está en el **diagrama completo** y en sus **láminas** (anexo `catedra/entregables/diagramas-cu/`), que siguen a esta figura. Después, el **mapa de navegación** (que no es un diagrama UML) resume los paquetes y los actores en una página, como ayuda para ubicarse.

**Figura 3 — Diagrama de casos de uso del sistema por subsistemas**

![Diagrama de casos de uso del sistema por subsistemas](../diagramas/uml/CU_Sistema_Diagrama-De-Subsistemas.png)

<!-- cu-completo:inicio -->
> **Diagrama completo de casos de uso del sistema (anexo).** Una sola imagen con los casos de uso del sistema, cada uno una vez, en tres columnas: a la izquierda, los actores, cada uno a la altura del centro de sus casos de uso; en la columna del medio, dentro del límite del sistema, los casos de uso que esos actores inician; y a la derecha, los casos incluidos que ningún actor inicia. Cada relación `«include»` y `«extend»` tiene su propio trazo ortogonal, con el estereotipo junto al trazo; la base de una extensión lleva el compartimiento de puntos de extensión con su identificador PE-n. Los casos planificados van en rosado. La imagen está también en `catedra/entregables/diagramas-cu/` en PNG, SVG y PDF.

**Figura 4 — Diagrama de casos de uso del sistema (todos los casos de uso)**

![Diagrama de casos de uso del sistema (todos los casos de uso)](../diagramas/uml/CU_Sistema_Diagrama-Completo.png)

> **Láminas complementarias.** El mismo diagrama, en 28 láminas más cortas, con la misma grilla de tres columnas: la de los actores con la generalización del Administrador General en el Administrador y, por cada actor, sus casos de uso en la columna del medio (el Administrador y el Cliente se parten en varias partes) y, a la derecha, los casos relacionados con ellos por `«include»` o `«extend»`; un caso que inicia otro actor o que es de otro subsistema figura con borde discontinuo, solo como referencia. Los diagramas de cada subsistema (Documento 1 §4.3) usan la misma grilla.

**Figura 5 — Diagrama de casos de uso, lámina 1 de 28: Actores del sistema y generalización de ACT-05 en ACT-03**

![Diagrama de casos de uso, lámina 1 de 28: Actores del sistema y generalización de ACT-05 en ACT-03](../diagramas/uml/CU_Sistema_Actores.png)

**Figura 6 — Diagrama de casos de uso, lámina 2 de 28: Cliente (ACT-01), parte 1 de 3**

![Diagrama de casos de uso, lámina 2 de 28: Cliente (ACT-01), parte 1 de 3](../diagramas/uml/CU_Sistema_Completo-Lamina-01_Cliente_Parte-1.png)

**Figura 7 — Diagrama de casos de uso, lámina 3 de 28: Cliente (ACT-01), parte 2 de 3**

![Diagrama de casos de uso, lámina 3 de 28: Cliente (ACT-01), parte 2 de 3](../diagramas/uml/CU_Sistema_Completo-Lamina-02_Cliente_Parte-2.png)

**Figura 8 — Diagrama de casos de uso, lámina 4 de 28: Cliente (ACT-01), parte 3 de 3**

![Diagrama de casos de uso, lámina 4 de 28: Cliente (ACT-01), parte 3 de 3](../diagramas/uml/CU_Sistema_Completo-Lamina-03_Cliente_Parte-3.png)

**Figura 9 — Diagrama de casos de uso, lámina 5 de 28: Chofer (ACT-02), parte 1 de 2**

![Diagrama de casos de uso, lámina 5 de 28: Chofer (ACT-02), parte 1 de 2](../diagramas/uml/CU_Sistema_Completo-Lamina-04_Chofer_Parte-1.png)

**Figura 10 — Diagrama de casos de uso, lámina 6 de 28: Chofer (ACT-02), parte 2 de 2**

![Diagrama de casos de uso, lámina 6 de 28: Chofer (ACT-02), parte 2 de 2](../diagramas/uml/CU_Sistema_Completo-Lamina-05_Chofer_Parte-2.png)

**Figura 11 — Diagrama de casos de uso, lámina 7 de 28: Administrador (ACT-03), parte 1 de 13**

![Diagrama de casos de uso, lámina 7 de 28: Administrador (ACT-03), parte 1 de 13](../diagramas/uml/CU_Sistema_Completo-Lamina-06_Administrador_Parte-1.png)

**Figura 12 — Diagrama de casos de uso, lámina 8 de 28: Administrador (ACT-03), parte 2 de 13**

![Diagrama de casos de uso, lámina 8 de 28: Administrador (ACT-03), parte 2 de 13](../diagramas/uml/CU_Sistema_Completo-Lamina-07_Administrador_Parte-2.png)

**Figura 13 — Diagrama de casos de uso, lámina 9 de 28: Administrador (ACT-03), parte 3 de 13**

![Diagrama de casos de uso, lámina 9 de 28: Administrador (ACT-03), parte 3 de 13](../diagramas/uml/CU_Sistema_Completo-Lamina-08_Administrador_Parte-3.png)

**Figura 14 — Diagrama de casos de uso, lámina 10 de 28: Administrador (ACT-03), parte 4 de 13**

![Diagrama de casos de uso, lámina 10 de 28: Administrador (ACT-03), parte 4 de 13](../diagramas/uml/CU_Sistema_Completo-Lamina-09_Administrador_Parte-4.png)

**Figura 15 — Diagrama de casos de uso, lámina 11 de 28: Administrador (ACT-03), parte 5 de 13**

![Diagrama de casos de uso, lámina 11 de 28: Administrador (ACT-03), parte 5 de 13](../diagramas/uml/CU_Sistema_Completo-Lamina-10_Administrador_Parte-5.png)

**Figura 16 — Diagrama de casos de uso, lámina 12 de 28: Administrador (ACT-03), parte 6 de 13**

![Diagrama de casos de uso, lámina 12 de 28: Administrador (ACT-03), parte 6 de 13](../diagramas/uml/CU_Sistema_Completo-Lamina-11_Administrador_Parte-6.png)

**Figura 17 — Diagrama de casos de uso, lámina 13 de 28: Administrador (ACT-03), parte 7 de 13**

![Diagrama de casos de uso, lámina 13 de 28: Administrador (ACT-03), parte 7 de 13](../diagramas/uml/CU_Sistema_Completo-Lamina-12_Administrador_Parte-7.png)

**Figura 18 — Diagrama de casos de uso, lámina 14 de 28: Administrador (ACT-03), parte 8 de 13**

![Diagrama de casos de uso, lámina 14 de 28: Administrador (ACT-03), parte 8 de 13](../diagramas/uml/CU_Sistema_Completo-Lamina-13_Administrador_Parte-8.png)

**Figura 19 — Diagrama de casos de uso, lámina 15 de 28: Administrador (ACT-03), parte 9 de 13**

![Diagrama de casos de uso, lámina 15 de 28: Administrador (ACT-03), parte 9 de 13](../diagramas/uml/CU_Sistema_Completo-Lamina-14_Administrador_Parte-9.png)

**Figura 20 — Diagrama de casos de uso, lámina 16 de 28: Administrador (ACT-03), parte 10 de 13**

![Diagrama de casos de uso, lámina 16 de 28: Administrador (ACT-03), parte 10 de 13](../diagramas/uml/CU_Sistema_Completo-Lamina-15_Administrador_Parte-10.png)

**Figura 21 — Diagrama de casos de uso, lámina 17 de 28: Administrador (ACT-03), parte 11 de 13**

![Diagrama de casos de uso, lámina 17 de 28: Administrador (ACT-03), parte 11 de 13](../diagramas/uml/CU_Sistema_Completo-Lamina-16_Administrador_Parte-11.png)

**Figura 22 — Diagrama de casos de uso, lámina 18 de 28: Administrador (ACT-03), parte 12 de 13**

![Diagrama de casos de uso, lámina 18 de 28: Administrador (ACT-03), parte 12 de 13](../diagramas/uml/CU_Sistema_Completo-Lamina-17_Administrador_Parte-12.png)

**Figura 23 — Diagrama de casos de uso, lámina 19 de 28: Administrador (ACT-03), parte 13 de 13**

![Diagrama de casos de uso, lámina 19 de 28: Administrador (ACT-03), parte 13 de 13](../diagramas/uml/CU_Sistema_Completo-Lamina-18_Administrador_Parte-13.png)

**Figura 24 — Diagrama de casos de uso, lámina 20 de 28: Administrador General (ACT-05), parte 1 de 3**

![Diagrama de casos de uso, lámina 20 de 28: Administrador General (ACT-05), parte 1 de 3](../diagramas/uml/CU_Sistema_Completo-Lamina-19_Administrador-General_Parte-1.png)

**Figura 25 — Diagrama de casos de uso, lámina 21 de 28: Administrador General (ACT-05), parte 2 de 3**

![Diagrama de casos de uso, lámina 21 de 28: Administrador General (ACT-05), parte 2 de 3](../diagramas/uml/CU_Sistema_Completo-Lamina-20_Administrador-General_Parte-2.png)

**Figura 26 — Diagrama de casos de uso, lámina 22 de 28: Administrador General (ACT-05), parte 3 de 3**

![Diagrama de casos de uso, lámina 22 de 28: Administrador General (ACT-05), parte 3 de 3](../diagramas/uml/CU_Sistema_Completo-Lamina-21_Administrador-General_Parte-3.png)

**Figura 27 — Diagrama de casos de uso, lámina 23 de 28: Sistema Automático (ACT-04)**

![Diagrama de casos de uso, lámina 23 de 28: Sistema Automático (ACT-04)](../diagramas/uml/CU_Sistema_Completo-Lamina-22_Sistema-Automatico.png)

**Figura 28 — Diagrama de casos de uso, lámina 24 de 28: Operador Técnico (ACT-10)**

![Diagrama de casos de uso, lámina 24 de 28: Operador Técnico (ACT-10)](../diagramas/uml/CU_Sistema_Completo-Lamina-23_Operador-Tecnico.png)

**Figura 29 — Diagrama de casos de uso, lámina 25 de 28: MercadoPago (ACT-06)**

![Diagrama de casos de uso, lámina 25 de 28: MercadoPago (ACT-06)](../diagramas/uml/CU_Sistema_Completo-Lamina-24_MercadoPago.png)

**Figura 30 — Diagrama de casos de uso, lámina 26 de 28: Firebase (ACT-07)**

![Diagrama de casos de uso, lámina 26 de 28: Firebase (ACT-07)](../diagramas/uml/CU_Sistema_Completo-Lamina-25_Firebase.png)

**Figura 31 — Diagrama de casos de uso, lámina 27 de 28: Servicio de correo (ACT-08)**

![Diagrama de casos de uso, lámina 27 de 28: Servicio de correo (ACT-08)](../diagramas/uml/CU_Sistema_Completo-Lamina-26_Servicio-De-Correo.png)

**Figura 32 — Diagrama de casos de uso, lámina 28 de 28: Plataforma de despliegue (ACT-09)**

![Diagrama de casos de uso, lámina 28 de 28: Plataforma de despliegue (ACT-09)](../diagramas/uml/CU_Sistema_Completo-Lamina-27_Plataforma-De-Despliegue.png)

<!-- cu-completo:fin -->

**Figura 33 — Mapa de navegación del sistema (no es un diagrama UML)**

![Mapa de navegación del sistema (no es un diagrama UML)](../diagramas/uml/CU_Sistema_Mapa.png)

> Resumen de una página del sistema: los 21 paquetes con su cantidad de casos de uso y una
> matriz que indica, con un punto, qué actores participan en cada paquete. Los actores se dibujan
> fuera del límite del sistema, una sola vez cada uno. El Administrador General especializa al
> Administrador.



---

## 7. Casos de Uso de Alto Nivel

> Los casos de uso CU-001 a CU-051 corresponden al alcance relevado inicialmente. Los casos CU-052 a CU-104 se incorporaron al contrastar la documentación contra el sistema construido: son comportamientos que el sistema ya realiza y que el relevamiento original no había registrado. Los casos CU-105 a CU-108 son los cuatro módulos inteligentes (M2 a M5). Los casos CU-109 a CU-175 desglosan en casos propios los ABM de choferes, vehículos, clientes, direcciones y franjas horarias, y suman el carrito, el pedido en curso, la vigencia de los envases, la flota, el consumo declarado, la compra express, los reintegros, el registro de auditoría y la configuración de los procesos automáticos. Los casos CU-176 a CU-344 son los módulos de gestión de la distribuidora —personal y legajos, flota ampliada, stock físico y carga del camión, compras, caja, rendiciones, cuentas corrientes y comisiones— con sus ABM. El catálogo tiene 334 casos: de CU-001 a CU-344 faltan diez, retirados (§8).
> La especificación expandida de cada caso está en el Documento 1; sus diagramas de
> secuencia del sistema, en el Documento 2, y los de interacción de diseño, en el
> Documento 3.

---

**Código:** CU-001 | **Caso de Uso:** Iniciar Sesión  
**Actor/es:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03); actores secundarios: Firebase (ACT-07)  
**Subsistema:** SS-01 Autenticación y Usuarios  
**Calificación:** Crítico  
**Descripción:** Un usuario —cliente, chofer o administrador— se identifica ante el sistema con su correo y su contraseña para empezar a operar con las funciones que corresponden a su rol. El sistema verifica la identidad sin guardar contraseñas propias. El ingreso no consulta si el chofer está habilitado: eso se exige recién cuando el chofer se pone en línea (CU-022).

---


**Código:** CU-002 | **Caso de Uso:** Registrarse como Cliente  
**Actor/es:** Cliente (ACT-01); actores secundarios: Servicio de correo (ACT-08)  
**Subsistema:** SS-01 Autenticación y Usuarios  
**Calificación:** Crítico  
**Descripción:** Una persona nueva se registra como cliente informando su nombre, su correo, su teléfono y una contraseña. Es la única alta que no requiere haber iniciado sesión y siempre crea un cliente: nunca otro rol. El registro no abre la sesión: para operar, el usuario inicia sesión a continuación (CU-001). La creación de la cuenta la resuelve CU-082, que este caso incluye.

---


**Código:** CU-004 | **Caso de Uso:** Consultar el Perfil de Usuario  
**Actor/es:** Cliente (ACT-01), Chofer (ACT-02); actores secundarios: Firebase (ACT-07)  
**Subsistema:** SS-01 Autenticación y Usuarios  
**Calificación:** Importante  
**Descripción:** El usuario consulta los datos de su propio perfil: nombre completo, correo, teléfono, foto, rol y, si es cliente, su ficha con las direcciones de entrega. Un usuario solo ve su propio perfil; un administrador puede ver el de los usuarios de su distribuidora.

---


**Código:** CU-251 | **Caso de Uso:** Modificar el Perfil de Usuario  
**Actor/es:** Cliente (ACT-01), Chofer (ACT-02)  
**Subsistema:** SS-01 Autenticación y Usuarios  
**Calificación:** Importante  
**Descripción:** El usuario corrige sus datos personales: nombre completo, teléfono y foto. Los cambios se ven de inmediato en las aplicaciones y en el panel del administrador. Un usuario solo puede modificarse a sí mismo; el correo, el rol y el bloqueo quedan reservados al administrador.

---


**Código:** CU-005 | **Caso de Uso:** Crear un Pedido  
**Actor/es:** Cliente (ACT-01); actores secundarios: MercadoPago (ACT-06), Firebase (ACT-07)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Crítico  
**Descripción:** El cliente arma un pedido eligiendo productos, cantidades, dirección de entrega, medio de pago y, si quiere, una franja horaria. El sistema comprueba la cobertura de la dirección, reserva el stock y el cupo de la franja de forma conjunta, calcula el total con promociones y recargos, registra el pedido y —salvo que el pago sea por MercadoPago o el pedido sea una reserva— lo ofrece a un chofer.

---


**Código:** CU-006 | **Caso de Uso:** Consultar el Detalle de un Pedido  
**Actor/es:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Crítico  
**Descripción:** El usuario ve el detalle completo de un pedido: ítems y cantidades, precios, descuentos, estado, chofer asignado, dirección, franja, medio y estado del pago —con el enlace para completarlo si el pago es por MercadoPago y sigue pendiente, salvo para el chofer— y el momento de cada cambio de estado. Cada rol ve lo mismo con acciones distintas. El acceso está acotado por distribuidora, por propiedad para el cliente y por lo que le corresponde para el chofer.

---


**Código:** CU-302 | **Caso de Uso:** Cotizar un Pedido  
**Actor/es:** Cliente (ACT-01), Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente, o el administrador por un cliente, pide el desglose de lo que costaría un pedido —renglones con la promoción por volumen, recargo de la zona, recargo por el medio de pago, total y saldo— sin crearlo ni reservar stock. También puede cotizar cómo quedaría un pedido pendiente al modificarlo.

---


**Código:** CU-007 | **Caso de Uso:** Consultar el Historial de Pedidos  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente ve el listado de todos sus pedidos anteriores, con el resumen de cada uno —fecha, total y estado— y acceso a su detalle. La consulta trae siempre la totalidad del historial: no tiene filtro por estado ni por fecha.

---


**Código:** CU-348 | **Caso de Uso:** Consultar el Reintegro de un Pedido  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-14 Pagos y Cobros  
**Calificación:** Secundario  
**Descripción:** El cliente ve en el detalle de su pedido las devoluciones de dinero que se le hicieron o que están en trámite: de qué tipo son, cuánto se devuelve, en qué estado están y cuándo se acreditaron. Solo puede verlas el dueño del pedido.

---


**Código:** CU-169 | **Caso de Uso:** Registrar el Cambio de Estado de un Pedido  
**Actor/es:** Ninguno directo: es un caso incluido; lo inician CU-005, CU-008, CU-009, CU-010, CU-012, CU-015, CU-018, CU-020, CU-072, CU-075, CU-077, CU-079 y CU-147  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** Es el comportamiento común de todo caso que crea un pedido o le cambia el estado: el sistema asienta en el historial de estados cada transición —la creación, la aceptación, el paso a en camino, la entrega, la cancelación, la liberación, la activación de una reserva y el vencimiento por falta de pago—, con el estado anterior, el nuevo, quién originó el cambio, el motivo y el momento. No lo inicia un actor por sí solo.

---


**Código:** CU-170 | **Caso de Uso:** Consultar el Historial de Estados de un Pedido  
**Actor/es:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Secundario  
**Descripción:** Quien puede leer un pedido ve la secuencia de estados por la que pasó: el cliente desde el detalle de su pedido, el chofer desde el que tiene a cargo y el administrador desde la ficha del pedido. Cada cambio muestra el momento, quién lo provocó y el motivo, si lo hubo; el nombre de quien lo hizo solo lo ve el personal de la distribuidora.

---


**Código:** CU-143 | **Caso de Uso:** Declarar el Consumo Promedio al Registrarse  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** Al crear su cuenta, el cliente puede declarar cuánto gas consume por mes y qué tipo de garrafa usa habitualmente. Con ese dato el sistema estima cuándo se le va a acabar y le avisa antes, sin esperar a tener historial de compras. Es una extensión opcional del registro (CU-002).

---


**Código:** CU-144 | **Caso de Uso:** Modificar el Consumo Promedio Declarado  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente corrige cuánto gas consume por mes cuando su situación cambia: se mudó, sumó gente en la casa o cambió de estufa. El sistema recalcula la fecha estimada de la próxima recompra con el valor nuevo.

---


**Código:** CU-145 | **Caso de Uso:** Configurar los Días de Aviso Previo a la Recompra  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Menor  
**Descripción:** El cliente elige con cuántos días de anticipación quiere que le avisen que se le está por acabar la garrafa, o desactiva el aviso. Sin esto, la anticipación sería la misma para todos y el aviso terminaría siendo ruido.

---


**Código:** CU-146 | **Caso de Uso:** Consultar la Fecha Estimada de Recompra  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El administrador ve qué clientes están por quedarse sin gas dentro de una ventana de tiempo, con su consumo declarado y su última compra. Le permite anticipar la demanda de la semana y, si quiere, ofrecer antes de que el cliente pida.

---


**Código:** CU-147 | **Caso de Uso:** Realizar una Compra Express  
**Actor/es:** Cliente (ACT-01); actores secundarios: MercadoPago (ACT-06), Firebase (ACT-07)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Crítico  
**Descripción:** El cliente que necesita una garrafa compra en un solo paso: una garrafa, su dirección predeterminada y listo, sin elegir franja horaria. El pedido sale a un chofer en moto y se entrega dentro de la hora. Es el segundo flujo de compra, en paralelo al que arma un pedido con franja (CU-005).

---


**Código:** CU-148 | **Caso de Uso:** Elegir la Modalidad de Entrega del Pedido  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** Antes de confirmar, el cliente puede elegir cómo quiere recibir el pedido: programado, eligiendo una franja horaria, o express, dentro de la hora y con recargo. El sistema le muestra las dos con su precio y su tiempo estimado, y solo ofrece la express si hay cobertura, horario y chofer. Es una extensión opcional de la creación del pedido (CU-005).

---


**Código:** CU-008 | **Caso de Uso:** Cancelar un Pedido (Cliente)  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente cancela un pedido propio que todavía no salió hacia su domicilio (pendiente, reservado o aceptado). El sistema cambia el estado a cancelado, devuelve al inventario el stock de cada ítem y avisa al chofer asignado, si lo había, que ya no hace falta ir.

---


**Código:** CU-009 | **Caso de Uso:** Liberar un Pedido (Chofer)  
**Actor/es:** Chofer (ACT-02)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El chofer que ya aceptó un pedido decide que no puede realizarlo. El pedido vuelve a pendiente, sin chofer, para que otro pueda tomarlo; no se cancela. El stock no se restituye porque el pedido sigue vivo.

---


**Código:** CU-010 | **Caso de Uso:** Cancelar un Pedido (Administrador)  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El administrador cancela cualquier pedido activo de su distribuidora —en cualquier estado anterior a la entrega— indicando un motivo. El sistema marca el pedido como cancelado, restituye el stock y avisa al cliente y al chofer asignado, si lo había.

---


**Código:** CU-011 | **Caso de Uso:** Consultar Todos los Pedidos  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El administrador ve los pedidos de su distribuidora, del más reciente al más antiguo, con paginación. Puede acotar el listado por estado, por rango de fechas y por un texto de búsqueda. Cada registro muestra el resumen del pedido, con acceso al detalle.

---


**Código:** CU-012 | **Caso de Uso:** Asignar un Chofer Manualmente  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-03 Despacho y Asignación  
**Calificación:** Secundario  
**Descripción:** Cuando el despacho automático agota los candidatos y el pedido queda pendiente sin que ningún chofer lo tome, el administrador interviene desde el panel y asigna a mano un chofer habilitado. También puede reasignar a otro chofer un pedido que ya había sido aceptado.

---


**Código:** CU-149 | **Caso de Uso:** Despachar un Pedido Express a un Chofer en Moto  
**Actor/es:** Sistema Automático (ACT-04)  
**Subsistema:** SS-03 Despacho y Asignación  
**Calificación:** Crítico  
**Descripción:** El sistema ofrece el pedido express al chofer en moto más cercano y le da menos tiempo para aceptar que en el despacho normal, porque la promesa de entrega es dentro de la hora. Si nadie acepta, no amplía la búsqueda como en CU-014: cancela la modalidad express y pasa el pedido al reparto común.

---


**Código:** CU-013 | **Caso de Uso:** Asignar un Pedido Automáticamente por Proximidad  
**Actor/es:** Sistema Automático (ACT-04); actores secundarios: Firebase (ACT-07)  
**Subsistema:** SS-03 Despacho y Asignación  
**Calificación:** Crítico  
**Descripción:** Al crearse un pedido, el sistema no lo ofrece a todos los choferes a la vez: abre una negociación secuencial, ofreciéndolo a un solo chofer por vez —el más cercano al domicilio entre los que todavía no fueron contactados— con un plazo acotado para aceptar. Si acepta, el pedido queda asignado (CU-015); si no responde a tiempo o lo rechaza, la oferta pasa al siguiente.

---


**Código:** CU-014 | **Caso de Uso:** Vencer la Oferta y Ofrecer al Siguiente Chofer  
**Actor/es:** Sistema Automático (ACT-04); actores secundarios: Firebase (ACT-07)  
**Subsistema:** SS-03 Despacho y Asignación  
**Calificación:** Crítico  
**Descripción:** Un proceso automático revisa periódicamente las ofertas cuya ventana de aceptación venció: las cierra y, si el pedido sigue sin chofer, abre la oferta para el siguiente candidato. El mismo proceso vuelve a poner en circulación los pedidos que quedaron sin ninguna oferta activa, por ejemplo porque al crearse no había ningún chofer cerca o porque el chofer que lo tenía lo liberó. Cada distribuidora recibe el ciclo con su propio intervalo (CU-173).

---


**Código:** CU-171 | **Caso de Uso:** Configurar los Parámetros de Despacho de la Distribuidora  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-03 Despacho y Asignación  
**Calificación:** Crítico  
**Descripción:** El administrador define para su distribuidora los pasos de radio con que el despacho busca choferes y el plazo que cada chofer tiene para aceptar una oferta. Los valores que regían cuando eran fijos —cuatro pasos de 5, 10, 15 y 20 km, y 30 segundos— quedan como valores por omisión.

---


**Código:** CU-015 | **Caso de Uso:** Aceptar un Pedido  
**Actor/es:** Chofer (ACT-02); actores secundarios: Firebase (ACT-07)  
**Subsistema:** SS-03 Despacho y Asignación  
**Calificación:** Crítico  
**Descripción:** El chofer recibe la oferta de un pedido y la acepta. El sistema se lo asigna, genera el código secreto de entrega, cierra la oferta y avisa al cliente en tiempo real y por notificación.

---


**Código:** CU-016 | **Caso de Uso:** Rechazar un Pedido Ofrecido  
**Actor/es:** Chofer (ACT-02); actores secundarios: Firebase (ACT-07)  
**Subsistema:** SS-03 Despacho y Asignación  
**Calificación:** Importante  
**Descripción:** El chofer que recibió la oferta de un pedido decide no tomarlo, rechazándola explícitamente o dejando vencer el plazo. El sistema cierra esa oferta y ofrece el pedido al siguiente chofer más cercano que no haya sido contactado. El rechazo no afecta el estado del pedido ni el stock.

---


**Código:** CU-017 | **Caso de Uso:** Modificar la Ubicación GPS del Chofer  
**Actor/es:** Chofer (ACT-02)  
**Subsistema:** SS-04 Seguimiento en Tiempo Real  
**Calificación:** Crítico  
**Descripción:** Mientras el chofer está en línea, su aplicación envía periódicamente la posición del dispositivo, cada vez que detecta un desplazamiento de unos diez metros. El sistema la mantiene disponible tanto para el despacho (CU-013) como para el mapa en tiempo real del cliente.

---


**Código:** CU-018 | **Caso de Uso:** Marcar un Pedido "En Camino"  
**Actor/es:** Chofer (ACT-02); actores secundarios: Firebase (ACT-07)  
**Subsistema:** SS-04 Seguimiento en Tiempo Real  
**Calificación:** Crítico  
**Descripción:** El chofer indica que salió hacia el domicilio del cliente. El sistema pasa el pedido a en camino, registra el momento, avisa al cliente y abre el seguimiento en vivo de la posición del chofer.

---


**Código:** CU-019 | **Caso de Uso:** Avisar la Llegada al Cliente  
**Actor/es:** Chofer (ACT-02); actores secundarios: Firebase (ACT-07)  
**Subsistema:** SS-04 Seguimiento en Tiempo Real  
**Calificación:** Importante  
**Descripción:** El chofer avisa, antes de confirmar la entrega, que llegó al domicilio del cliente, para que éste esté preparado a recibirlo. El aviso le llega en tiempo real y como notificación, aunque tenga la aplicación cerrada. No queda registrado como un estado ni como una marca de tiempo del pedido.

---


**Código:** CU-020 | **Caso de Uso:** Confirmar una Entrega Manualmente  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05); actores secundarios: Firebase (ACT-07)  
**Subsistema:** SS-04 Seguimiento en Tiempo Real  
**Calificación:** Crítico  
**Descripción:** El administrador da por entregado un pedido que está en camino cuando el cliente no puede confirmarlo con el código —por ejemplo, no tiene el celular a mano— y deja el motivo asentado. El sistema cierra el ciclo del pedido, registra el momento, descuenta el stock y avisa al cliente. El chofer no cierra la entrega por su cuenta: la confirma el cliente con el código (CU-079).

---


**Código:** CU-022 | **Caso de Uso:** Activar la Disponibilidad  
**Actor/es:** Chofer (ACT-02)  
**Subsistema:** SS-04 Seguimiento en Tiempo Real  
**Calificación:** Crítico  
**Descripción:** El chofer activa su disponibilidad para recibir pedidos con un interruptor en su aplicación. Al activarse no reaparece de inmediato para el despacho: recién lo hace cuando su aplicación informa una nueva posición.

---


**Código:** CU-266 | **Caso de Uso:** Desactivar la Disponibilidad  
**Actor/es:** Chofer (ACT-02)  
**Subsistema:** SS-04 Seguimiento en Tiempo Real  
**Calificación:** Crítico  
**Descripción:** El chofer desactiva su disponibilidad para recibir pedidos con un interruptor en su aplicación. Al desactivarse, el sistema lo retira del seguimiento que usa el despacho para elegir candidatos.

---


**Código:** CU-023 | **Caso de Uso:** Registrar un Reclamo  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-05 Reclamos  
**Calificación:** Importante  
**Descripción:** El cliente registra un reclamo sobre un pedido propio indicando el motivo, una descripción detallada y, si quiere, una foto como evidencia. El sistema comprueba que el pedido le pertenezca y crea el reclamo pendiente, sin exigir que el pedido esté entregado: también puede reclamarse uno pendiente, aceptado o incluso cancelado.

---


**Código:** CU-024 | **Caso de Uso:** Consultar los Reclamos  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-05 Reclamos  
**Calificación:** Importante  
**Descripción:** El administrador ve en el panel todos los reclamos de su distribuidora, del más reciente al más antiguo, sin filtro por estado ni por fecha. Cada registro muestra el cliente, el pedido, el motivo y el estado: pendiente, en proceso, resuelto o rechazado.

---


**Código:** CU-025 | **Caso de Uso:** Resolver un Reclamo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-05 Reclamos  
**Calificación:** Importante  
**Descripción:** El administrador revisa un reclamo pendiente o en proceso y lo cierra como resuelto o rechazado, ingresando obligatoriamente una nota que explique la decisión. Un reclamo ya cerrado no se vuelve a resolver sin reabrirlo antes (CU-167). El sistema no avisa al cliente del resultado.

---


**Código:** CU-166 | **Caso de Uso:** Tomar un Reclamo Pendiente  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-05 Reclamos  
**Calificación:** Importante  
**Descripción:** El administrador marca un reclamo pendiente como en proceso para que el resto del equipo sepa que ya lo está revisando. No exige nota: se la pide recién al resolverlo (CU-025).

---


**Código:** CU-167 | **Caso de Uso:** Reabrir un Reclamo  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-05 Reclamos  
**Calificación:** Importante  
**Descripción:** El administrador reabre un reclamo ya resuelto o rechazado, con un motivo obligatorio, y lo deja en proceso. Es el único camino para cambiar un cierre: un reclamo cerrado no se vuelve a resolver sin reabrirlo antes.

---


**Código:** CU-174 | **Caso de Uso:** Adjuntar la Fotografía de un Reclamo  
**Actor/es:** Cliente (ACT-01), Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-05 Reclamos  
**Calificación:** Importante  
**Descripción:** El cliente adjunta una fotografía como evidencia de su reclamo, al registrarlo o después, mientras el reclamo no esté resuelto ni rechazado. La imagen (JPG, PNG o WEBP, de hasta 10 MB) se guarda en un almacenamiento privado y el reclamo conserva su referencia. Es una extensión opcional de CU-023.

---


**Código:** CU-175 | **Caso de Uso:** Consultar la Fotografía de un Reclamo  
**Actor/es:** Cliente (ACT-01), Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-05 Reclamos  
**Calificación:** Secundario  
**Descripción:** El cliente y el administrador ven la fotografía que respalda un reclamo, aunque el reclamo esté cerrado. El sistema la entrega por una dirección firmada, de corta vigencia.

---


**Código:** CU-026 | **Caso de Uso:** Consultar el Tablero General  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-06 Reportes y Tablero  
**Calificación:** Importante  
**Descripción:** El administrador ve en el panel el estado operativo de su distribuidora: pedidos por estado, entregas del día, ventas del día, la semana, el mes y acumuladas, choferes activos, valor promedio de pedido y la evolución de las ventas de los últimos siete días.

---


**Código:** CU-027 | **Caso de Uso:** Consultar el Reporte de Ventas por Chofer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-06 Reportes y Tablero  
**Calificación:** Importante  
**Descripción:** El administrador consulta el total de pedidos entregados y el monto vendido por cada chofer en un rango de fechas. El reporte se puede ordenar por cantidad de pedidos o por monto total.

---


**Código:** CU-028 | **Caso de Uso:** Consultar el Reporte de Ventas por Producto  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-06 Reportes y Tablero  
**Calificación:** Importante  
**Descripción:** El administrador consulta las unidades vendidas y el monto total por tipo de garrafa en un rango de fechas. Permite identificar qué producto tiene mayor demanda.

---


**Código:** CU-029 | **Caso de Uso:** Consultar el Reporte por Método de Pago  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-06 Reportes y Tablero  
**Calificación:** Secundario  
**Descripción:** El administrador consulta, para un rango de fechas, cómo se reparten los pedidos entregados y sus montos entre los medios de pago —efectivo, MercadoPago y transferencia—, para analizar el comportamiento de pago de sus clientes. Mide entregas concretadas, no pedidos creados.

---


**Código:** CU-030 | **Caso de Uso:** Consultar el Gráfico de Ventas (últimos 7 días)  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-06 Reportes y Tablero  
**Calificación:** Secundario  
**Descripción:** Dentro del panel, el administrador ve un gráfico de barras con el monto vendido en cada uno de los últimos siete días. Los días sin ventas muestran barra en cero: no se omiten.

---


**Código:** CU-304 | **Caso de Uso:** Consultar los Cobros Pendientes  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-06 Reportes y Tablero  
**Calificación:** Secundario  
**Descripción:** El administrador consulta, por rango de entrega, el dinero que todavía no suma a las ventas: efectivo pendiente de confirmar, impagos, pérdidas, transferencias sin confirmar o no recibidas, y reintegros pendientes.

---


**Código:** CU-031 | **Caso de Uso:** Registrar un Chofer (Gestión de la Flota)  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Crítico  
**Descripción:** El administrador da de alta a un repartidor de su distribuidora, cargando sus datos personales y de contacto. El sistema crea la cuenta con el rol de chofer y su perfil operativo, que queda a la espera de la habilitación. La creación de la cuenta la resuelve CU-082, que este caso incluye.

---


**Código:** CU-032 | **Caso de Uso:** Validar un Chofer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Crítico  
**Descripción:** El administrador marca a un chofer como validado. Es un dato declarativo que queda registrado y alimenta el conteo de choferes habilitados del panel de control, pero no condiciona la operación real del chofer. El único control que tiene efecto sobre si un chofer puede operar es su estado de actividad (CU-033).

---


**Código:** CU-271 | **Caso de Uso:** Invalidar un Chofer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Crítico  
**Descripción:** El administrador retira a un chofer la marca de validado. Es un dato declarativo: invalidar a un chofer no le impide seguir apareciendo para el despacho ni aceptando pedidos. El único control que tiene efecto sobre si un chofer puede operar es su estado de actividad (CU-267).

---


**Código:** CU-033 | **Caso de Uso:** Activar un Chofer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador activa a un chofer, con independencia de la disponibilidad que el chofer declare desde su aplicación. Es el modo de volver a habilitar a un chofer suspendido temporalmente (CU-267) sin tocar su validación.

---


**Código:** CU-267 | **Caso de Uso:** Desactivar un Chofer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador desactiva a un chofer, con independencia de la disponibilidad que el chofer declare desde su aplicación. Sirve para suspender temporalmente a un chofer sin revocar su validación.

---


**Código:** CU-034 | **Caso de Uso:** Registrar un Vehículo del Chofer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador registra el vehículo de un chofer: tipo (auto, moto, camioneta), patente, marca, modelo, año, color y capacidad de carga. El vehículo queda asociado al chofer. Un chofer puede tener varios vehículos registrados.

---


**Código:** CU-035 | **Caso de Uso:** Consultar el Listado de Choferes  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador consulta el listado paginado de choferes de su distribuidora, con sus datos de contacto, si están validados, si están activos y su calificación promedio. El listado no incluye el vehículo de cada chofer: para conocerlo hay que consultarlo aparte (CU-051).

---


**Código:** CU-036 | **Caso de Uso:** Crear un Producto (Garrafa)  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Crítico  
**Descripción:** El administrador registra un tipo de garrafa con tipo (por ejemplo «10kg»), peso, precio de venta, stock inicial y descripción opcional. El producto queda activo y disponible en el catálogo del cliente. Opcionalmente puede configurar promociones por volumen en el mismo formulario.

---


**Código:** CU-037 | **Caso de Uso:** Modificar el Precio de un Producto  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Crítico  
**Descripción:** El administrador modifica el precio de venta de un producto. El cambio aplica solo a los pedidos futuros: los pedidos existentes conservan el precio con el que fueron creados.

---


**Código:** CU-038 | **Caso de Uso:** Modificar el Stock de un Producto  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Crítico  
**Descripción:** El administrador ajusta manualmente el stock de un producto para reflejar una reposición de inventario o una corrección. El valor que ingresa no reemplaza el stock existente sino que se suma a él: un valor positivo repone unidades y uno negativo las descuenta.

---


**Código:** CU-039 | **Caso de Uso:** Configurar las Promociones por Cantidad  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador define descuentos automáticos por volumen para un producto, indicando para cada regla la cantidad mínima de unidades y el porcentaje de descuento. Cada regla se guarda como una promoción propia del producto, una por cantidad. Las reglas se aplican automáticamente al calcular el subtotal de cada ítem del pedido.

---


**Código:** CU-040 | **Caso de Uso:** Desactivar un Producto  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador da de baja un producto del catálogo. El producto deja de aparecer en la aplicación del cliente y no puede seleccionarse en pedidos nuevos, aunque su stock y sus datos se conservan. La reactivación (CU-268) y la vista para ubicar un producto dado de baja (CU-269) lo complementan.

---


**Código:** CU-268 | **Caso de Uso:** Reactivar un Producto  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador reactiva un producto dado de baja del catálogo de su distribuidora. El producto vuelve a aparecer en la aplicación del cliente y a poder seleccionarse en pedidos nuevos, con su stock y sus promociones intactos.

---


**Código:** CU-269 | **Caso de Uso:** Consultar los Productos Inactivos  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador consulta los productos de su distribuidora que fueron dados de baja, para ubicar el que quiere reactivar.

---


**Código:** CU-041 | **Caso de Uso:** Consultar el Catálogo de Productos (Cliente)  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Crítico  
**Descripción:** El cliente ve en su aplicación los productos disponibles de una distribuidora: los activos y con stock, con su precio, sus promociones por cantidad y los medios de pago con su recargo. También puede ver el detalle de un producto. La consulta es abierta: no requiere haber iniciado sesión.

---


**Código:** CU-344 | **Caso de Uso:** Consultar el Catálogo de Productos (Administrador)  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador ve el catálogo de su distribuidora con paginación: los productos activos, con su tipo, precio y stock, incluidos los que tienen stock en cero. Puede buscar por tipo. Desde el listado abre el detalle para modificar el precio, ajustar el stock, configurar promociones o dar de baja el producto.

---


**Código:** CU-042 | **Caso de Uso:** Crear una Franja Horaria  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-09 Franjas Horarias  
**Calificación:** Importante  
**Descripción:** El administrador crea una franja horaria de entrega con nombre (por ejemplo «Mañana»), hora de inicio, hora de fin y capacidad máxima diaria de pedidos. La franja queda activa y disponible para que el cliente la elija al crear un pedido.

---


**Código:** CU-043 | **Caso de Uso:** Modificar una Franja Horaria  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-09 Franjas Horarias  
**Calificación:** Importante  
**Descripción:** El administrador modifica una franja horaria ya creada —su nombre, su rango horario o su capacidad máxima diaria— para ajustarla a la disponibilidad real. Si la capacidad nueva queda por debajo de lo ya agendado para algún día desde hoy, el sistema la rechaza.

---


**Código:** CU-342 | **Caso de Uso:** Activar una Franja Horaria  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-09 Franjas Horarias  
**Calificación:** Importante  
**Descripción:** El administrador activa una franja horaria de su distribuidora. Una franja activa puede elegirse al agendar un pedido y figura en la disponibilidad.

---


**Código:** CU-343 | **Caso de Uso:** Desactivar una Franja Horaria  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-09 Franjas Horarias  
**Calificación:** Importante  
**Descripción:** El administrador desactiva una franja horaria de su distribuidora. Una franja inactiva no se ofrece a los clientes ni cuenta para la disponibilidad, pero conserva sus pedidos ya agendados.

---


**Código:** CU-044 | **Caso de Uso:** Seleccionar una Franja Horaria al Crear un Pedido  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-09 Franjas Horarias  
**Calificación:** Importante  
**Descripción:** Durante la creación de un pedido, el cliente puede elegir una fecha de entrega y una franja horaria; si no indica ninguna de las dos, el pedido se despacha de inmediato. Cuando sí las indica, el sistema controla el cupo de esa franja para esa fecha antes de registrar el pedido. Es una extensión opcional de CU-005.

---


**Código:** CU-045 | **Caso de Uso:** Consultar las Franjas Horarias Disponibles  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-09 Franjas Horarias  
**Calificación:** Importante  
**Descripción:** El cliente consulta qué franjas horarias están disponibles para una fecha antes de confirmar su pedido. El sistema muestra las franjas activas con su capacidad remanente para esa fecha.

---


**Código:** CU-046 | **Caso de Uso:** Consultar las Direcciones de Entrega del Cliente  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente abre su libreta de direcciones y ve todas las que tiene registradas, con la predeterminada primero y el resto de la más nueva a la más vieja. Es la consulta del listado: el alta, la modificación, la baja y la marca de predeterminada son los casos CU-116 a CU-121.

---


**Código:** CU-116 | **Caso de Uso:** Registrar una Dirección de Entrega  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente da de alta una dirección donde quiere recibir sus garrafas: calle, altura, piso y departamento, ciudad, código postal, ubicación e indicaciones para el repartidor, y puede marcarla como predeterminada en el mismo acto. Es el alta del ABM de direcciones.

---


**Código:** CU-117 | **Caso de Uso:** Consultar Detalle de una Dirección de Entrega  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente abre una dirección puntual y ve todos sus datos. Es la lectura de la que dependen la modificación, la baja y la marca de predeterminada, y la que aplica el control de pertenencia.

---


**Código:** CU-118 | **Caso de Uso:** Modificar una Dirección de Entrega  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente corrige los datos de una dirección registrada: calle, altura, piso, departamento, ciudad, código postal, ubicación o indicaciones para el repartidor. Es la modificación del ABM de direcciones.

---


**Código:** CU-119 | **Caso de Uso:** Dar de Baja una Dirección de Entrega  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente da de baja una dirección que ya no usa. La baja es lógica: la dirección deja de aparecer, pero los pedidos que la usaron la siguen mostrando. Si era la predeterminada, el sistema promueve a predeterminada la más reciente de las que quedan, para que el cliente nunca se quede sin una.

---


**Código:** CU-120 | **Caso de Uso:** Marcar una Dirección como Predeterminada  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente elige cuál de sus direcciones se propone sola al armar un pedido. El sistema marca esa y desmarca las demás, de modo que siempre hay exactamente una.

---


**Código:** CU-121 | **Caso de Uso:** Consultar la Dirección Predeterminada  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** La aplicación recupera la dirección que el cliente dejó marcada como predeterminada, para proponerla sola cuando arranca un pedido. Evita que el cliente tenga que elegir dirección en cada compra.

---


**Código:** CU-122 | **Caso de Uso:** Agregar un Ítem al Carrito  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente elige un tipo de garrafa del catálogo y lo suma a su carrito con una cantidad. El carrito sobrevive al cierre de la aplicación y al cambio de dispositivo, de modo que el cliente puede armar la compra en varios momentos. Es el primer paso del proceso de compra que termina en CU-005.

---


**Código:** CU-123 | **Caso de Uso:** Modificar la Cantidad de un Ítem del Carrito  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente cambia cuántas garrafas de un tipo quiere, sin tener que sacar el ítem y volver a agregarlo.

---


**Código:** CU-124 | **Caso de Uso:** Quitar un Ítem del Carrito  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente saca del carrito un tipo de garrafa que había agregado. Es la contracara de CU-122.

---


**Código:** CU-125 | **Caso de Uso:** Consultar el Carrito  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente ve lo que lleva armado: los tipos de garrafa, las cantidades, el precio de cada uno y el total. Es la lectura de la que dependen las demás operaciones del carrito.

---


**Código:** CU-126 | **Caso de Uso:** Vaciar el Carrito  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Menor  
**Descripción:** El cliente descarta de una vez todo lo que había armado, en lugar de quitar los ítems de a uno. El sistema también vacía el carrito cuando la compra se confirma, para que el cliente no arranque la próxima con lo que ya compró.

---


**Código:** CU-127 | **Caso de Uso:** Cambiar la Dirección de Entrega del Pedido  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente cambia a dónde quiere que le lleven un pedido ya confirmado, mientras todavía no salió el repartidor. El sistema comprueba que la dirección nueva sea suya y esté dentro de la cobertura, y guarda el cambio con su motivo para que el chofer y el administrador vean qué pasó.

---


**Código:** CU-128 | **Caso de Uso:** Indicar Quién Recibe el Pedido  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente aclara que la garrafa la va a recibir otra persona —un familiar, el encargado del edificio o un vecino— y registra su nombre, su documento y su relación con él, para que el chofer sepa a quién puede entregar y quede asentado quién recibió.

---


**Código:** CU-047 | **Caso de Uso:** Recuperar la Contraseña  
**Actor/es:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03); actores secundarios: Firebase (ACT-07), Servicio de correo (ACT-08)  
**Subsistema:** SS-01 Autenticación y Usuarios  
**Calificación:** Importante  
**Descripción:** Un usuario que olvidó su contraseña pide restablecerla informando su correo. El sistema le envía un correo con un enlace para definir una contraseña nueva y, cuando el usuario la define, recupera el acceso. El cambio del correo es otro caso (CU-336).

---


**Código:** CU-336 | **Caso de Uso:** Cambiar el Correo del Usuario  
**Actor/es:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03)  
**Subsistema:** SS-01 Autenticación y Usuarios  
**Calificación:** Importante  
**Descripción:** El usuario cambia el correo de su cuenta. El sistema lo actualiza, lo deja pendiente de verificación y avisa a la dirección anterior. Recuperar una contraseña olvidada es otro caso (CU-047).

---


**Código:** CU-048 | **Caso de Uso:** Procesar el Pago con MercadoPago  
**Actor/es:** MercadoPago (ACT-06)  
**Subsistema:** SS-14 Pagos y Conciliación  
**Calificación:** Crítico  
**Descripción:** Cuando un pedido se paga con MercadoPago, la pasarela avisa al sistema. El sistema consulta el estado real del pago, marca el pedido como pagado si corresponde y recién entonces dispara el despacho, de forma que un aviso repetido no produzca efectos nuevos. Un pago rechazado no tiene un circuito propio: el pedido queda pendiente con su stock reservado hasta que el sistema lo cancele por vencimiento.

---


**Código:** CU-168 | **Caso de Uso:** Reintegrar el Pago de un Pedido  
**Actor/es:** Administrador (ACT-03), Sistema Automático (ACT-04)  
**Subsistema:** SS-14 Pagos y Conciliación  
**Calificación:** Importante  
**Descripción:** Cuando se cancela un pedido que el cliente ya pagó por una pasarela, o cuando un pedido express pasa al reparto común y deja de corresponder su recargo, el sistema pide a la pasarela que devuelva el importe y deja constancia. Si la pasarela rechaza la devolución, avisa al panel y el administrador puede reintentarla. Es una extensión de la cancelación del cliente (CU-008) y del administrador (CU-010) y del despacho express (CU-149).

---


**Código:** CU-292 | **Caso de Uso:** Confirmar el Cobro en Efectivo  
**Actor/es:** Chofer (ACT-02)  
**Subsistema:** SS-14 Pagos y Conciliación  
**Calificación:** Crítico  
**Descripción:** El chofer confirma que cobró el efectivo de un pedido que ya entregó. El pago pasa de pendiente a pagado y queda registrado quién lo confirmó y cuándo.

---


**Código:** CU-293 | **Caso de Uso:** Informar el Cobro Impago  
**Actor/es:** Chofer (ACT-02)  
**Subsistema:** SS-14 Pagos y Conciliación  
**Calificación:** Importante  
**Descripción:** El chofer informa que el cliente no pagó el efectivo de un pedido entregado. El pago pasa a impago, el sistema abre una incidencia de cobro impago y avisa a los administradores en el panel.

---


**Código:** CU-294 | **Caso de Uso:** Resolver un Cobro Impago  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-14 Pagos y Conciliación  
**Calificación:** Importante  
**Descripción:** El administrador cierra un cobro impago: el cliente pagó después o se da por perdido. Deja la nota con el motivo, queda registrado quién y cuándo, y se cierra la incidencia de cobro impago.

---


**Código:** CU-299 | **Caso de Uso:** Registrar el Cobro en Efectivo como Administrador  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-14 Pagos y Conciliación  
**Calificación:** Importante  
**Descripción:** El administrador registra que cobró el efectivo de un pedido entregado cuyo chofer no lo confirmó, porque no lo hizo o ya no está. Deja el motivo y queda una nota en el historial de estados.

---


**Código:** CU-300 | **Caso de Uso:** Registrar el Cobro Impago como Administrador  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-14 Pagos y Conciliación  
**Calificación:** Importante  
**Descripción:** El administrador informa que el cliente no pagó el efectivo de un pedido entregado cuyo chofer no lo informó. El pago pasa a impago, se abre la incidencia de cobro impago y queda una nota en el historial.

---


**Código:** CU-301 | **Caso de Uso:** Confirmar una Transferencia  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-14 Pagos y Conciliación  
**Calificación:** Importante  
**Descripción:** El administrador confirma que la transferencia de un pedido llegó, o la marca como no recibida, con el motivo. Recién confirmada, el pedido cuenta como venta.

---


**Código:** CU-049 | **Caso de Uso:** Consultar las Ganancias del Chofer  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El chofer consulta desde su aplicación el saldo acumulado de sus ganancias; el administrador consulta ese mismo saldo desde el panel. El ajuste manual del saldo es otro caso (CU-337).

---


**Código:** CU-337 | **Caso de Uso:** Ajustar el Saldo del Chofer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador suma o descuenta un monto al saldo acumulado de un chofer.

---


**Código:** CU-050 | **Caso de Uso:** Bloquear un Usuario  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-01 Autenticación y Usuarios  
**Calificación:** Secundario  
**Descripción:** El administrador bloquea a un usuario por moderación o seguridad: el de empresa, a los choferes y administradores de su distribuidora; el Administrador General, también a los clientes, porque un cliente puede comprarle a varias distribuidoras. Un usuario bloqueado no puede iniciar sesión ni operar mientras dure el bloqueo. Es la alternativa reversible a dar de baja la cuenta (CU-085).

---


**Código:** CU-270 | **Caso de Uso:** Desbloquear un Usuario  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-01 Autenticación y Usuarios  
**Calificación:** Secundario  
**Descripción:** El administrador levanta el bloqueo de un usuario: el de empresa, el de los choferes y administradores de su distribuidora; el Administrador General, también el de los clientes. El usuario vuelve a poder iniciar sesión y operar.

---


**Código:** CU-051 | **Caso de Uso:** Consultar el Listado de Vehículos  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador consulta el listado de los vehículos de su distribuidora, con el tipo, la patente y el chofer al que pertenece cada uno. La edición, la baja, el detalle, la búsqueda por patente y los vehículos de un chofer son casos propios (CU-111 a CU-115).

---


**Código:** CU-052 | **Caso de Uso:** Registrar una Distribuidora  
**Actor/es:** Administrador General (ACT-05)  
**Subsistema:** SS-10 Multi-Distribuidora  
**Calificación:** Crítico  
**Descripción:** El Administrador General registra una nueva distribuidora, validando su nombre y su nombre corto.

---


**Código:** CU-053 | **Caso de Uso:** Consultar las Distribuidoras  
**Actor/es:** Administrador General (ACT-05)  
**Subsistema:** SS-10 Multi-Distribuidora  
**Calificación:** Crítico  
**Descripción:** El Administrador General consulta todas las distribuidoras o el detalle de una específica.

---


**Código:** CU-054 | **Caso de Uso:** Modificar los Datos de una Distribuidora  
**Actor/es:** Administrador General (ACT-05)  
**Subsistema:** SS-10 Multi-Distribuidora  
**Calificación:** Crítico  
**Descripción:** El Administrador General modifica los datos de una distribuidora, su estado o su plan, con validación previa.

---


**Código:** CU-055 | **Caso de Uso:** Dar de Baja una Distribuidora  
**Actor/es:** Administrador General (ACT-05)  
**Subsistema:** SS-10 Multi-Distribuidora  
**Calificación:** Importante  
**Descripción:** El Administrador General da de baja una distribuidora. La baja es lógica: el registro se conserva.

---


**Código:** CU-056 | **Caso de Uso:** Crear un Polígono de Cobertura  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-11 Cobertura Geográfica  
**Calificación:** Importante  
**Descripción:** El administrador registra una nueva zona de cobertura, un polígono dibujado en el mapa, asociada a su distribuidora, con su recargo de entrega.

---


**Código:** CU-057 | **Caso de Uso:** Consultar los Polígonos de Cobertura  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-11 Cobertura Geográfica  
**Calificación:** Secundario  
**Descripción:** El administrador consulta las zonas de cobertura de su distribuidora, ordenadas por prioridad. El panel las dibuja en el mapa.

---


**Código:** CU-058 | **Caso de Uso:** Validar la Cobertura de una Dirección  
**Actor/es:** Cliente (ACT-01), Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-11 Cobertura Geográfica  
**Calificación:** Crítico  
**Descripción:** El sistema evalúa unas coordenadas contra las zonas de cobertura de la distribuidora y responde si están cubiertas y con qué recargo.

---


**Código:** CU-059 | **Caso de Uso:** Dar de Baja un Polígono de Cobertura  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-11 Cobertura Geográfica  
**Calificación:** Secundario  
**Descripción:** El administrador da de baja una zona de cobertura de su distribuidora. La baja es lógica: la zona se conserva, pero deja de aparecer y de contar para la validación de cobertura.

---


**Código:** CU-305 | **Caso de Uso:** Modificar un Polígono de Cobertura  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-11 Cobertura Geográfica  
**Calificación:** Importante  
**Descripción:** El administrador cambia la forma de un polígono de cobertura ya dibujado, su nombre o su recargo —y también la prioridad, la etiqueta y el color—. La validación del polígono y del recargo es la de la creación (CU-056).

---


**Código:** CU-306 | **Caso de Uso:** Consultar un Polígono de Cobertura  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-11 Cobertura Geográfica  
**Calificación:** Secundario  
**Descripción:** El administrador abre un polígono de cobertura de su distribuidora y ve su forma, su nombre, su recargo, su prioridad, su vigencia y si está activo.

---


**Código:** CU-307 | **Caso de Uso:** Activar un Polígono de Cobertura  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-11 Cobertura Geográfica  
**Calificación:** Importante  
**Descripción:** El administrador activa un polígono de cobertura de su distribuidora sin tocar su forma ni su recargo. La zona vuelve a aplicar cobertura y recargo a los pedidos nuevos.

---


**Código:** CU-308 | **Caso de Uso:** Desactivar un Polígono de Cobertura  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-11 Cobertura Geográfica  
**Calificación:** Importante  
**Descripción:** El administrador desactiva un polígono de cobertura de su distribuidora sin tocar su forma ni su recargo. La zona deja de aplicar cobertura y recargo a los pedidos nuevos, pero se conserva para volver a activarla.

---


**Código:** CU-150 | **Caso de Uso:** Programar la Vigencia de un Polígono de Cobertura  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-11 Cobertura Geográfica  
**Calificación:** Importante  
**Descripción:** El administrador le pone fecha de fin a una zona de cobertura, para que su recargo valga solo por un tiempo: una calle cortada por obra, un barrio anegado, un fin de semana largo. Sin esto, tendría que acordarse de volver al panel a desactivar la zona a mano, y mientras tanto se le seguiría cobrando el recargo al cliente.

---


**Código:** CU-151 | **Caso de Uso:** Desactivar los Polígonos de Cobertura Vencidos  
**Actor/es:** Sistema Automático (ACT-04)  
**Subsistema:** SS-11 Cobertura Geográfica  
**Calificación:** Importante  
**Descripción:** Un proceso automático desactiva las zonas cuya fecha de fin ya pasó, de modo que su recargo deje de aplicarse sin que nadie intervenga. La zona no se borra: queda inactiva con su historia intacta, porque los pedidos que ya se cobraron con ese recargo tienen que poder explicarse después.

---


**Código:** CU-060 | **Caso de Uso:** Registrar una Incidencia de Entrega  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-12 Incidencias y Calidad de Servicio  
**Calificación:** Crítico  
**Descripción:** El chofer, o un administrador, registra una incidencia sobre un pedido: una demora, un siniestro o cualquier inconveniente surgido durante el reparto. La incidencia queda abierta, enlazada al pedido, a la espera de resolución (CU-063).

---


**Código:** CU-061 | **Caso de Uso:** Consultar las Incidencias  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-12 Incidencias y Calidad de Servicio  
**Calificación:** Importante  
**Descripción:** El administrador ve las incidencias de entrega registradas en su distribuidora, de la más reciente a la más antigua, con el pedido afectado y su cliente.

---


**Código:** CU-062 | **Caso de Uso:** Consultar las Incidencias de un Pedido  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-12 Incidencias y Calidad de Servicio  
**Calificación:** Secundario  
**Descripción:** Se listan las incidencias ocurridas en un pedido específico de la distribuidora.

---


**Código:** CU-063 | **Caso de Uso:** Resolver una Incidencia  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-12 Incidencias y Calidad de Servicio  
**Calificación:** Importante  
**Descripción:** El administrador cierra una incidencia con una nota de resolución, para que deje de figurar entre las pendientes del panel.

---


**Código:** CU-064 | **Caso de Uso:** Calificar un Pedido (cliente↔chofer)  
**Actor/es:** Cliente (ACT-01), Chofer (ACT-02)  
**Subsistema:** SS-12 Incidencias y Calidad de Servicio  
**Calificación:** Crítico  
**Descripción:** El cliente y el chofer se califican mutuamente cuando el pedido quedó entregado. El sistema guarda la calificación tras verificar que el pedido está entregado y corresponde a quien califica. Se admite una calificación por pedido y por lado.

---


**Código:** CU-065 | **Caso de Uso:** Consultar el Promedio de Calificaciones de un Usuario  
**Actor/es:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-12 Incidencias y Calidad de Servicio  
**Calificación:** Secundario  
**Descripción:** Se consulta el promedio de estrellas y la cantidad de calificaciones de un usuario.

---


**Código:** CU-066 | **Caso de Uso:** Consultar el Historial de Calificaciones Recibidas  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-12 Incidencias y Calidad de Servicio  
**Calificación:** Secundario  
**Descripción:** El administrador consulta las calificaciones, con su comentario, que recibió un usuario.

---


**Código:** CU-067 | **Caso de Uso:** Dar de Alta un Envase Físico  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-13 Trazabilidad de Envases  
**Calificación:** Importante  
**Descripción:** El administrador da de alta un envase físico en el inventario de su distribuidora, identificado por su número de serie, que nace en depósito con su primer movimiento asentado. El número de serie no puede repetirse dentro de la distribuidora.

---


**Código:** CU-068 | **Caso de Uso:** Asignar los Envases a un Pedido  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-13 Trazabilidad de Envases  
**Calificación:** Crítico  
**Descripción:** El administrador o el chofer ata al pedido los envases llenos que salen a repartir y los despacha, dejando cada movimiento asentado con la firma de quien lo hizo. Se controla el estado de cada envase.

---


**Código:** CU-069 | **Caso de Uso:** Consultar el Parque de Envases  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-13 Trazabilidad de Envases  
**Calificación:** Importante  
**Descripción:** El administrador consulta el inventario actual de envases de su distribuidora, opcionalmente filtrado por estado.

---


**Código:** CU-070 | **Caso de Uso:** Registrar un Movimiento de Envase (cambio de estado)  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-13 Trazabilidad de Envases  
**Calificación:** Crítico  
**Descripción:** El administrador o el chofer hace avanzar un envase por su ciclo de vida físico, con las reglas del ciclo decidiendo si el paso es admisible y con la titularidad del envase ajustada en consecuencia.

---


**Código:** CU-071 | **Caso de Uso:** Consultar el Historial de Movimientos de un Envase  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-13 Trazabilidad de Envases  
**Calificación:** Importante  
**Descripción:** El administrador ve el historial de movimientos y estados por los que pasó un envase.

---


**Código:** CU-132 | **Caso de Uso:** Registrar la Revisión Periódica de un Envase  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-13 Trazabilidad de Envases  
**Calificación:** Crítico  
**Descripción:** El administrador asienta la prueba hidráulica de un envase: la fecha en que se hizo, el resultado y cuándo vence. Las garrafas de gas licuado tienen una vida útil regulada y no se pueden llenar ni despachar una vez vencida la revisión, así que el sistema necesita saber la fecha de cada una.

---


**Código:** CU-133 | **Caso de Uso:** Consultar la Vigencia de un Envase  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-13 Trazabilidad de Envases  
**Calificación:** Importante  
**Descripción:** El administrador consulta hasta cuándo puede circular un envase y cuándo fue su última revisión. Es la lectura que necesita antes de llenarlo, de despacharlo o de decidir si lo manda al taller.

---


**Código:** CU-134 | **Caso de Uso:** Consultar los Envases Próximos a Vencer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-13 Trazabilidad de Envases  
**Calificación:** Importante  
**Descripción:** El administrador ve qué envases de su parque vencen dentro de una ventana de tiempo, para mandarlos a revisar antes de que queden fuera de circulación.

---


**Código:** CU-135 | **Caso de Uso:** Bloquear el Despacho de un Envase Vencido  
**Actor/es:** Sistema Automático (ACT-04)  
**Subsistema:** SS-13 Trazabilidad de Envases  
**Calificación:** Crítico  
**Descripción:** El sistema impide que un envase con la revisión vencida se asigne a un pedido. Es el control que le da sentido a registrar las fechas: sin él, el dato existe pero no evita que salga a la calle un envase fuera de norma. Es una extensión de la asignación de envases (CU-068).

---


**Código:** CU-072 | **Caso de Uso:** Crear una Reserva Programada con Seña  
**Actor/es:** Cliente (ACT-01), Chofer (ACT-02), Administrador (ACT-03); actores secundarios: MercadoPago (ACT-06), Firebase (ACT-07)  
**Subsistema:** SS-15 Reservas Programadas  
**Calificación:** Crítico  
**Descripción:** El cliente aparta garrafas para una fecha futura dejando una seña, indicando explícitamente que se trata de una reserva. El pedido nace reservado y no se ofrece a ningún chofer: el stock se descuenta en el acto y la entrega espera al día agendado, cuando un proceso automático la devuelve al circuito normal. Lo que determina que el pedido sea una reserva es ese indicador explícito y no el solo hecho de traer una fecha futura. La operación admite al cliente, pero hoy la reserva se crea solo desde el panel, por el administrador, en nombre del cliente al cargar un pedido a mano cuando llama: elige la fecha, la franja horaria con cupo y el monto de la seña. La seña no puede superar el total del pedido, y una reserva no se modifica: para cambiarla se cancela y se crea otra.

---


**Código:** CU-073 | **Caso de Uso:** Consultar las Reservas y el Estado de la Seña  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-15 Reservas Programadas  
**Calificación:** Importante  
**Descripción:** El administrador ve las reservas programadas de su distribuidora, con el día y la franja de entrega, si la seña fue abonada y, cuando la seña es por MercadoPago y sigue pendiente, el enlace para pagarla.

---


**Código:** CU-074 | **Caso de Uso:** Confirmar la Seña Cobrada en Efectivo  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-15 Reservas Programadas  
**Calificación:** Crítico  
**Descripción:** El administrador confirma que la seña de una reserva fue recibida fuera del sistema, en efectivo o por transferencia. La seña de MercadoPago no se confirma a mano: la marca cobrada el aviso de la pasarela.

---


**Código:** CU-075 | **Caso de Uso:** Activar las Reservas Vencidas Automáticamente  
**Actor/es:** Sistema Automático (ACT-04)  
**Subsistema:** SS-15 Reservas Programadas  
**Calificación:** Crítico  
**Descripción:** El sistema activa automáticamente las reservas cuyo día de entrega llegó y que ya tienen la seña pagada: las devuelve al circuito normal como pedidos pendientes y las ofrece a los choferes.

---


**Código:** CU-076 | **Caso de Uso:** Expirar las Reservas sin Seña Pagada  
**Actor/es:** Sistema Automático (ACT-04)  
**Subsistema:** SS-15 Reservas Programadas  
**Calificación:** Importante  
**Descripción:** El sistema cancela las reservas cuya seña nunca fue pagada dentro del plazo, devolviendo el stock que tenían reservado.

---


**Código:** CU-077 | **Caso de Uso:** Expirar los Pedidos de MercadoPago sin Pagar  
**Actor/es:** Sistema Automático (ACT-04)  
**Subsistema:** SS-15 Reservas Programadas  
**Calificación:** Importante  
**Descripción:** El sistema cancela los pedidos pagados por MercadoPago que llevan demasiado tiempo sin que la pasarela confirme el pago, devolviendo el stock al inventario.

---


**Código:** CU-078 | **Caso de Uso:** Consultar el Código de Entrega (QR del chofer)  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-04 Seguimiento en Tiempo Real  
**Calificación:** Crítico  
**Descripción:** El chofer recupera el código secreto de entrega del pedido que está llevando, para mostrarlo como QR al cliente al llegar al domicilio. El código se genera cuando el pedido es aceptado y no cambia mientras el pedido conserve el mismo chofer.

---


**Código:** CU-079 | **Caso de Uso:** Confirmar una Entrega Escaneando el QR (cliente)  
**Actor/es:** Cliente (ACT-01), Administrador (ACT-03), Administrador General (ACT-05); actores secundarios: Firebase (ACT-07)  
**Subsistema:** SS-04 Seguimiento en Tiempo Real  
**Calificación:** Crítico  
**Descripción:** El sistema registra la entrega del pedido tras comprobar que el código que muestra el chofer coincide con el guardado. Lo confirma el cliente con su aplicación o, con el motivo por escrito, un administrador. No marca el pago como cobrado: el efectivo lo confirma el chofer aparte (CU-292).

---


**Código:** CU-303 | **Caso de Uso:** Consultar la Ruta de un Pedido  
**Actor/es:** Cliente (ACT-01), Chofer (ACT-02)  
**Subsistema:** SS-04 Seguimiento en Tiempo Real  
**Calificación:** Importante  
**Descripción:** El chofer asignado, o el cliente dueño mientras el pedido está en camino, pide la ruta por calles desde la última posición del chofer hasta la dirección de entrega, para dibujarla en el mapa.

---


**Código:** CU-080 | **Caso de Uso:** Consultar el Pool de Pedidos Disponibles  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Crítico  
**Descripción:** El chofer consulta los pedidos pendientes que todavía no tienen repartidor, dentro de su distribuidora, para tomar trabajo por su cuenta cuando el despacho automático no lo alcanzó. Si no puede recibir pedidos por su carga de camión, la lista viene vacía con el aviso.

---


**Código:** CU-081 | **Caso de Uso:** Consultar los Pedidos Asignados al Chofer  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Crítico  
**Descripción:** El chofer consulta los pedidos que tiene asignados, y el administrador usa la misma consulta para auditar la carga de trabajo de un repartidor. Es la vista operativa de la jornada del chofer.

---


**Código:** CU-338 | **Caso de Uso:** Retomar el Pedido en Curso  
**Actor/es:** Chofer (ACT-02)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** Al abrir la aplicación, el chofer recupera el pedido que tiene en curso —el que lleva en camino o, si no, el aceptado más antiguo— para retomarlo donde lo dejó. Si no tiene ninguno, recupera el pedido entregado hoy en efectivo cuyo cobro sigue pendiente.

---


**Código:** CU-339 | **Caso de Uso:** Modificar un Pedido Pendiente (Administrador)  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El administrador cambia un pedido pendiente que todavía no tiene chofer: la dirección, la franja o la fecha, el medio de pago, las notas o los renglones. Los precios y los recargos los vuelve a calcular el sistema y el stock se ajusta.

---


**Código:** CU-341 | **Caso de Uso:** Modificar un Pedido Pendiente (Cliente)  
**Actor/es:** Cliente (ACT-01)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** El cliente cambia su pedido mientras todavía está pendiente y ningún repartidor lo tomó: los renglones, la dirección, la franja o la fecha, el medio de pago (menos MercadoPago) o las notas. Antes de guardar, ve cómo quedaría el total con la cotización (CU-302); el sistema recalcula precios y recargos y ajusta el stock.

---


**Código:** CU-082 | **Caso de Uso:** Crear un Usuario Base  
**Actor/es:** Ninguno directo: es un caso incluido; lo inician CU-002, CU-031, CU-086 y CU-087; actores secundarios: Firebase (ACT-07)  
**Subsistema:** SS-01 Autenticación y Usuarios  
**Calificación:** Importante  
**Descripción:** Es el comportamiento común de todas las altas de usuario: el sistema decide si quien lo pide puede crear ese rol, controla que el correo y el teléfono estén libres, crea la cuenta de acceso y guarda el usuario con el perfil que corresponde a su rol. No lo inicia un actor por sí solo: lo incluyen los casos que dan de alta usuarios (CU-002, CU-031, CU-086 y CU-087).

---


**Código:** CU-083 | **Caso de Uso:** Consultar los Usuarios  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-01 Autenticación y Usuarios  
**Calificación:** Importante  
**Descripción:** El administrador consulta los usuarios del sistema, con paginación y búsqueda por texto libre sobre correo, nombre y teléfono. Un administrador de empresa ve solo a su personal y a los clientes que le compraron.

---


**Código:** CU-272 | **Caso de Uso:** Buscar un Usuario  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-01 Autenticación y Usuarios  
**Calificación:** Importante  
**Descripción:** El administrador busca un usuario puntual por su correo o por su teléfono. Es la base de las pantallas de gestión de cuentas.

---


**Código:** CU-085 | **Caso de Uso:** Dar de Baja un Usuario  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05); actores secundarios: Firebase (ACT-07)  
**Subsistema:** SS-01 Autenticación y Usuarios  
**Calificación:** Importante  
**Descripción:** El administrador da de baja la cuenta de un usuario. La baja es lógica: el usuario, su perfil y sus direcciones dejan de aparecer pero se conservan para el historial y la auditoría, y el acceso queda deshabilitado. Los vehículos no se dan de baja: la flota es de la distribuidora. Un chofer con pedidos en curso o con una carga de camión abierta no puede darse de baja. La cuenta de un cliente la da de baja solo el Administrador General.

---


**Código:** CU-086 | **Caso de Uso:** Registrar un Administrador  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-16 Administración de Cuentas y Roles  
**Calificación:** Importante  
**Descripción:** Un administrador da de alta a otro administrador. Un administrador de empresa solo puede crear administradores de su distribuidora; el Administrador General, en cualquier distribuidora, y también otros administradores generales. La creación de la cuenta la resuelve CU-082, que este caso incluye.

---


**Código:** CU-087 | **Caso de Uso:** Crear el Primer Administrador General  
**Actor/es:** Operador Técnico (ACT-10)  
**Subsistema:** SS-16 Administración de Cuentas y Roles  
**Calificación:** Importante  
**Descripción:** En la puesta en marcha, el Operador Técnico —la persona con acceso al servidor— crea la primera cuenta de Administrador General ejecutando una orden en el servidor. No existe una operación pública para esto. La creación de la cuenta la resuelve CU-082, que este caso incluye.

---


**Código:** CU-088 | **Caso de Uso:** Consultar los Administradores  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-16 Administración de Cuentas y Roles  
**Calificación:** Secundario  
**Descripción:** El administrador consulta las cuentas administrativas de su distribuidora, o busca una puntual por identificador o correo. El Administrador General, sin distribuidora elegida, ve las de todas.

---


**Código:** CU-345 | **Caso de Uso:** Modificar un Administrador  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-16 Administración de Cuentas y Roles  
**Calificación:** Importante  
**Descripción:** El administrador corrige el nombre o el teléfono de otro administrador. Un administrador de empresa solo modifica a los de su distribuidora, nunca a un Administrador General ni a sí mismo; el Administrador General modifica a cualquiera, eligiendo la distribuidora si es un administrador de empresa, y puede modificar su propio perfil. El correo, el rol, la distribuidora y el bloqueo no se cambian por acá.

---


**Código:** CU-346 | **Caso de Uso:** Dar de Baja un Administrador  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-16 Administración de Cuentas y Roles  
**Calificación:** Importante  
**Descripción:** El administrador da de baja a otro administrador: la cuenta deja de existir para el panel y pierde el acceso, pero se conserva todo lo que hizo. Rigen las mismas reglas que para modificarlo, y además nadie se da de baja a sí mismo, tampoco el Administrador General. No se puede dar de baja al último administrador activo de una distribuidora ni al último Administrador General.

---


**Código:** CU-089 | **Caso de Uso:** Consultar los Roles  
**Actor/es:** Administrador General (ACT-05)  
**Subsistema:** SS-16 Administración de Cuentas y Roles  
**Calificación:** Importante  
**Descripción:** El Administrador General consulta los roles de la plataforma: los lista o consulta uno puntual.

---


**Código:** CU-252 | **Caso de Uso:** Crear un Rol  
**Actor/es:** Administrador General (ACT-05)  
**Subsistema:** SS-16 Administración de Cuentas y Roles  
**Calificación:** Importante  
**Descripción:** El Administrador General da de alta un rol en el catálogo de roles de la plataforma.

---


**Código:** CU-253 | **Caso de Uso:** Modificar un Rol  
**Actor/es:** Administrador General (ACT-05)  
**Subsistema:** SS-16 Administración de Cuentas y Roles  
**Calificación:** Importante  
**Descripción:** El Administrador General modifica un rol del catálogo de roles de la plataforma. Los cuatro roles del sistema no se pueden modificar.

---


**Código:** CU-254 | **Caso de Uso:** Dar de Baja un Rol  
**Actor/es:** Administrador General (ACT-05)  
**Subsistema:** SS-16 Administración de Cuentas y Roles  
**Calificación:** Importante  
**Descripción:** El Administrador General da de baja un rol del catálogo de roles de la plataforma, siempre que no sea uno de los del sistema ni tenga usuarios asignados.

---


**Código:** CU-092 | **Caso de Uso:** Consultar el Listado de Clientes  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-16 Administración de Cuentas y Roles  
**Calificación:** Importante  
**Descripción:** El administrador consulta la cartera de clientes de su distribuidora, con paginación y búsqueda por nombre o correo. Un cliente aparece si le hizo al menos un pedido a esa distribuidora.

---


**Código:** CU-094 | **Caso de Uso:** Modificar la Ubicación del Cliente  
**Actor/es:** Cliente (ACT-01), Administrador (ACT-03)  
**Subsistema:** SS-16 Administración de Cuentas y Roles  
**Calificación:** Secundario  
**Descripción:** El cliente, o el administrador, actualiza la ubicación de referencia guardada en el perfil del cliente.

---


**Código:** CU-095 | **Caso de Uso:** Dar de Baja un Cliente  
**Actor/es:** Administrador General (ACT-05)  
**Subsistema:** SS-16 Administración de Cuentas y Roles  
**Calificación:** Importante  
**Descripción:** El Administrador General da de baja lógica el perfil de un cliente: deja de aparecer en las consultas, pero se conserva con su historial. Un administrador de empresa no puede hacerlo, porque un cliente puede comprarle a varias distribuidoras.

---


**Código:** CU-129 | **Caso de Uso:** Consultar el Detalle del Cliente  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-16 Administración de Cuentas y Roles  
**Calificación:** Importante  
**Descripción:** El administrador abre la ficha de un cliente y ve sus datos, su marca de validación y su última ubicación conocida. Es la lectura puntual que el listado (CU-092) no cubre y de la que dependen la modificación y la baja.

---


**Código:** CU-130 | **Caso de Uso:** Buscar un Cliente por Usuario  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-16 Administración de Cuentas y Roles  
**Calificación:** Importante  
**Descripción:** El administrador ubica la ficha de cliente a partir de la cuenta de usuario, que es el dato con el que llega desde el resto del panel: un pedido, un reclamo o una calificación. Es una extensión de la consulta del detalle del cliente (CU-129).

---


**Código:** CU-131 | **Caso de Uso:** Modificar los Datos del Cliente  
**Actor/es:** Administrador General (ACT-05)  
**Subsistema:** SS-16 Administración de Cuentas y Roles  
**Calificación:** Importante  
**Descripción:** El Administrador General corrige los datos de la cuenta de un cliente: su nombre y su teléfono, o le fija una contraseña nueva. Es la modificación del ABM de clientes, separada de la actualización de ubicación (CU-094) y de la baja (CU-095), que son operaciones distintas sobre el mismo cliente. Un administrador de empresa no puede hacerlo, porque un cliente puede comprarle a varias distribuidoras.

---


**Código:** CU-096 | **Caso de Uso:** Modificar el Perfil del Chofer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador cambia la marca de validación del perfil de un chofer. Es el único dato que la operación acepta: los datos de la persona, la ubicación, el saldo, la disponibilidad y el estado de actividad tienen cada uno su propia operación.

---


**Código:** CU-097 | **Caso de Uso:** Dar de Baja un Chofer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador da de baja a un chofer: su perfil y su cuenta se marcan como borrados y salen de las consultas, pero se conservan con su historial de entregas. Se rechaza mientras tenga pedidos aceptados o en camino; si no los tiene, el chofer sale del despacho y se libera su vehículo en uso.

---


**Código:** CU-109 | **Caso de Uso:** Consultar el Detalle del Chofer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador abre la ficha de un chofer y ve sus datos personales, su vehículo, si está validado, si está activo y su calificación. Es la lectura puntual que el listado (CU-035) no cubre y de la que dependen la modificación y la baja.

---


**Código:** CU-110 | **Caso de Uso:** Buscar un Chofer por Usuario  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador ubica el perfil de chofer a partir de la cuenta de usuario, que es el dato con el que llega desde el resto del panel —un pedido, un reclamo, una calificación—. Es la búsqueda que incluyen las demás operaciones del ABM.

---


**Código:** CU-111 | **Caso de Uso:** Modificar un Vehículo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador corrige los datos del vehículo de un chofer: tipo, patente, marca, modelo, año, color o capacidad de carga. Salió de CU-051, que agrupaba modificar, dar de baja y consultar en un solo caso.

---


**Código:** CU-112 | **Caso de Uso:** Dar de Baja un Vehículo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador da de baja un vehículo de la flota. Salió de CU-051. La baja es lógica: el vehículo deja de aparecer, se conserva para el historial y su patente puede volver a registrarse.

---


**Código:** CU-113 | **Caso de Uso:** Consultar el Detalle del Vehículo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador abre la ficha de un vehículo y ve su tipo, patente, marca, modelo, año, color, capacidad de carga y el chofer al que pertenece. Salió de CU-051.

---


**Código:** CU-114 | **Caso de Uso:** Buscar un Vehículo por Patente  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador ubica un vehículo por su patente, que es el dato con el que se lo nombra en la operación diaria. Es una vía alternativa de búsqueda, independiente del listado (CU-051).

---


**Código:** CU-115 | **Caso de Uso:** Consultar los Vehículos de un Chofer  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** Se listan los vehículos registrados a nombre de un chofer. El administrador lo usa desde la ficha del chofer; el propio chofer, para ver los suyos. Salió de CU-051.

---


**Código:** CU-136 | **Caso de Uso:** Registrar el Seguro del Vehículo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Crítico  
**Descripción:** El administrador carga la compañía, el número de póliza y la fecha de vencimiento del seguro de un vehículo de la flota. Un vehículo sin seguro vigente no puede salir a repartir: el dato es una condición de habilitación, no un adjunto.

---


**Código:** CU-137 | **Caso de Uso:** Registrar la Verificación Técnica Vehicular  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Crítico  
**Descripción:** El administrador carga la fecha hasta la que vale la verificación técnica de un vehículo. Es obligatoria para circular y, en el transporte de gas licuado, es lo que habilita al vehículo a llevar la carga.

---


**Código:** CU-138 | **Caso de Uso:** Registrar la Licencia de Conducir del Chofer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Crítico  
**Descripción:** El administrador carga el número, la categoría y el vencimiento de la licencia de conducir de un chofer. La categoría importa: no es la misma la que habilita una moto que la que habilita un camión de reparto.

---


**Código:** CU-139 | **Caso de Uso:** Consultar los Vencimientos de la Flota  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador ve en una sola pantalla qué seguros, verificaciones técnicas y licencias vencen dentro de una ventana de tiempo, y cuáles ya vencieron. Es la vista de control de la flota, la contracara de CU-134 para los envases.

---


**Código:** CU-140 | **Caso de Uso:** Programar un Mantenimiento de Vehículo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador agenda un service, un cambio de cubiertas o una reparación para un vehículo, con la fecha prevista y el tipo de trabajo. Queda anotado como programado, para que el administrador lo tenga presente al planificar.

---


**Código:** CU-141 | **Caso de Uso:** Registrar un Mantenimiento Realizado  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador cierra un mantenimiento: anota cuándo se hizo, con cuántos kilómetros, cuánto costó y qué se hizo. Es lo que construye el historial del vehículo, del que sale el costo de mantenimiento por unidad y el intervalo real entre servicios.

---


**Código:** CU-142 | **Caso de Uso:** Avisar los Vencimientos Próximos de la Flota  
**Actor/es:** Sistema Automático (ACT-04); actores secundarios: Servicio de correo (ACT-08)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El sistema revisa todos los días qué tareas de mantenimiento de la flota están por vencer o ya vencieron, con la anticipación propia de cada plan, y avisa por correo a los administradores de cada distribuidora. Convierte el tablero de CU-139 en algo que no depende de que alguien se acuerde de mirarlo.

---


**Código:** CU-155 | **Caso de Uso:** Adjuntar un Archivo a una Tarea de Flota  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador sube un archivo —la foto o el PDF de una póliza, una verificación técnica o una licencia— como adjunto de una tarea de mantenimiento de la flota (CU-136 a CU-141).

---


**Código:** CU-156 | **Caso de Uso:** Consultar los Adjuntos de una Tarea de Flota  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** El administrador lista los archivos adjuntos de una tarea de mantenimiento de la flota.

---


**Código:** CU-157 | **Caso de Uso:** Descargar un Adjunto de Flota  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** El administrador descarga un archivo adjunto de una tarea de mantenimiento de la flota.

---


**Código:** CU-158 | **Caso de Uso:** Eliminar un Adjunto de Flota  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** El administrador borra un archivo adjunto de una tarea de mantenimiento de la flota.

---


**Código:** CU-159 | **Caso de Uso:** Almacenar un Archivo  
**Actor/es:** Ninguno directo: es un caso incluido; lo inician CU-155 y CU-174  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** Guarda el contenido de un archivo en el almacenamiento privado del sistema, el único proveedor de archivos. Lo incluyen CU-155 y CU-174.

---


**Código:** CU-160 | **Caso de Uso:** Recuperar un Archivo  
**Actor/es:** Ninguno directo: es un caso incluido; lo inician CU-157 y CU-175  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** Resuelve cómo entregar el contenido de un archivo ya guardado: una dirección firmada, de corta vigencia, con la que el archivo se baja directo del almacenamiento privado. Lo incluyen CU-157 y CU-175.

---


**Código:** CU-161 | **Caso de Uso:** Poner un Vehículo en Uso para un Chofer  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador define qué vehículo de la flota de su distribuidora usa un chofer. La flota es de la distribuidora y cualquier chofer puede usar cualquiera de sus vehículos: el vehículo registrado a nombre del chofer (CU-034) es solo informativo y el que cuenta para el despacho es el que está en uso. La operación cierra la asignación anterior del chofer y la del vehículo, y abre la nueva.

---


**Código:** CU-162 | **Caso de Uso:** Liberar el Vehículo en Uso de un Chofer  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** El administrador deja al chofer sin vehículo en uso. El vehículo queda libre para otro chofer y el período de uso se conserva en el historial.

---


**Código:** CU-163 | **Caso de Uso:** Consultar el Vehículo en Uso de un Chofer  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** Se consulta qué vehículo tiene en uso un chofer. El administrador lo usa desde la ficha del chofer; el propio chofer, para ver el suyo. La respuesta indica además si el vehículo está inhabilitado por documentación vencida.

---


**Código:** CU-164 | **Caso de Uso:** Consultar el Historial de Vehículos de un Chofer  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** El administrador lista los vehículos que un chofer usó, del más reciente al más antiguo, con las fechas de asignación y liberación.

---


**Código:** CU-165 | **Caso de Uso:** Consultar el Historial de Choferes de un Vehículo  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** El administrador lista los choferes que usaron un vehículo, del más reciente al más antiguo. Un vehículo dado de baja conserva su historial.

---


**Código:** CU-195 | **Caso de Uso:** Registrar una Carga de Combustible  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador, o el chofer desde su aplicación con el vehículo que tiene en uso, registra una carga de combustible: fecha y hora, tipo de combustible, litros, precio por litro, importe, kilometraje del tablero, si se llenó el tanque, estación, medio de pago y comprobante. El sistema impide que el kilometraje retroceda, actualiza el del vehículo y marca la carga como anómala si su consumo se aparta del promedio, avisando a los administradores.

---


**Código:** CU-320 | **Caso de Uso:** Modificar una Carga de Combustible  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador corrige los datos de una carga de combustible ya registrada; se revalidan las mismas reglas que al registrarla.

---


**Código:** CU-321 | **Caso de Uso:** Anular una Carga de Combustible  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador anula una carga de combustible. La baja es lógica y recalcula el kilometraje del vehículo si era la última.

---


**Código:** CU-322 | **Caso de Uso:** Consultar las Cargas de Combustible  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** El administrador consulta las cargas de combustible por vehículo, chofer, fechas y anomalía.

---


**Código:** CU-196 | **Caso de Uso:** Consultar el Consumo de Combustible de un Vehículo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador consulta cuánto rinde un vehículo en un período: kilómetros por litro, costo por kilómetro, tramos entre cargas de tanque lleno y cargas anómalas.

---


**Código:** CU-197 | **Caso de Uso:** Registrar la Habilitación para Transportar Mercancías Peligrosas  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Crítico  
**Descripción:** El administrador registra la habilitación del vehículo para transportar mercancías peligrosas, que exige el reparto de gas licuado: número, autoridad que la otorga, inicio de vigencia y vencimiento. Un vehículo con la habilitación vencida queda inhabilitado y no recibe pedidos.

---


**Código:** CU-198 | **Caso de Uso:** Registrar una Multa de Tránsito  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador registra una multa de tránsito de un vehículo: fecha y hora de la infracción, jurisdicción, número de acta, infracción, importe, importe con pago voluntario y vencimiento. El sistema sugiere el chofer que usaba el vehículo en ese momento.

---


**Código:** CU-323 | **Caso de Uso:** Modificar una Multa de Tránsito  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador corrige los datos de una multa o la pasa a apelada. Una multa pagada o anulada no se modifica.

---


**Código:** CU-324 | **Caso de Uso:** Anular una Multa de Tránsito  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador anula una multa con un motivo obligatorio. La baja es lógica: la multa se conserva y el motivo queda guardado.

---


**Código:** CU-325 | **Caso de Uso:** Consultar las Multas de Tránsito  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** El administrador consulta las multas por vehículo, chofer, estado y fechas.

---


**Código:** CU-326 | **Caso de Uso:** Avisar las Multas por Vencer  
**Actor/es:** Sistema Automático (ACT-04); actores secundarios: Servicio de correo (ACT-08)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** Cada día el sistema avisa por correo a los administradores de las multas pendientes que vencen en siete días o menos, o que ya vencieron.

---


**Código:** CU-199 | **Caso de Uso:** Registrar el Pago de una Multa  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** El administrador registra que una multa se pagó: fecha de pago e importe pagado. La multa pasa a pagada, desde pendiente o desde apelada.

---


**Código:** CU-200 | **Caso de Uso:** Imputar una Multa al Chofer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** El administrador imputa una multa al chofer que conducía el vehículo, para que se le descuente en la liquidación. Mientras no exista el módulo de caja queda solo la marca de imputación.

---


**Código:** CU-201 | **Caso de Uso:** Registrar un Siniestro  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador, o el chofer desde su aplicación, registra un siniestro de un vehículo: fecha, lugar, descripción, si hubo heridos o terceros, si hubo derrame de gas, denuncia policial y reclamo al seguro. Si el vehículo no puede circular, queda fuera de servicio.

---


**Código:** CU-327 | **Caso de Uso:** Modificar un Siniestro  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador corrige los datos de un siniestro y lo hace avanzar de estado.

---


**Código:** CU-328 | **Caso de Uso:** Consultar los Siniestros  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** El administrador consulta los siniestros por vehículo, estado y fechas.

---


**Código:** CU-202 | **Caso de Uso:** Cerrar un Siniestro  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** El administrador cierra un siniestro cuando se resolvió: asienta el costo de la reparación, el reintegro del seguro y la franquicia.

---


**Código:** CU-203 | **Caso de Uso:** Consultar el Costo Total de un Vehículo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador consulta cuánto cuesta un vehículo en un período, por rubro —mantenimiento, seguros, combustible, multas y siniestros—, con los kilómetros recorridos, el costo por kilómetro y la evolución mes a mes.

---


**Código:** CU-204 | **Caso de Uso:** Consultar el Tablero de Costos de la Flota  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador consulta el costo de toda la flota en un período, con un renglón por vehículo —rubros, kilómetros y costo por kilómetro— ordenado por costo por kilómetro.

---


**Código:** CU-205 | **Caso de Uso:** Registrar un Neumático  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** El administrador da de alta un neumático de la distribuidora: número de serie, marca, medida y costo. Queda en depósito hasta que se lo monta en un vehículo. Es una funcionalidad opcional del módulo.

---


**Código:** CU-206 | **Caso de Uso:** Registrar un Movimiento de Neumático  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Secundario  
**Descripción:** El administrador registra un movimiento de un neumático: montaje en un vehículo, desmontaje, rotación de posición, recapado o baja, con el kilometraje del vehículo. Es una funcionalidad opcional del módulo.

---


**Código:** CU-247 | **Caso de Uso:** Reactivar un Vehículo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** El administrador devuelve a la flota activa un vehículo que estaba fuera de servicio, por ejemplo por un siniestro, siempre que su documentación bloqueante esté en regla. Si alguna sigue vencida, el sistema lo rechaza y dice cuál.

---


**Código:** CU-100 | **Caso de Uso:** Enviar una Notificación de Prueba  
**Actor/es:** Administrador General (ACT-05); actores secundarios: Firebase (ACT-07)  
**Subsistema:** SS-17 Notificaciones y Mensajería  
**Calificación:** Secundario  
**Descripción:** El Administrador General envía una notificación de prueba a un dispositivo concreto, para verificar de punta a punta el canal de notificaciones.

---


**Código:** CU-101 | **Caso de Uso:** Reenviar la Notificación de Confirmación de Pedido  
**Actor/es:** Administrador General (ACT-05); actores secundarios: Firebase (ACT-07)  
**Subsistema:** SS-17 Notificaciones y Mensajería  
**Calificación:** Secundario  
**Descripción:** El Administrador General vuelve a enviarle a un cliente la notificación de confirmación de un pedido, cuando la original no llegó.

---


**Código:** CU-102 | **Caso de Uso:** Probar el Servicio de Correo  
**Actor/es:** Administrador General (ACT-05); actores secundarios: Servicio de correo (ACT-08)  
**Subsistema:** SS-17 Notificaciones y Mensajería  
**Calificación:** Secundario  
**Descripción:** El Administrador General le pide al sistema que mande un correo de prueba a una dirección, para verificar de punta a punta la configuración del servicio de correo.

---


**Código:** CU-154 | **Caso de Uso:** Consultar el Listado de Franjas Horarias  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-09 Franjas Horarias  
**Calificación:** Importante  
**Descripción:** El administrador consulta el listado completo de franjas horarias de su distribuidora, para elegir la que va a modificar o dar de baja. Es la consulta propia del ABM de franjas; la consulta de disponibilidad de cara al cliente es otra (CU-045).

---


**Código:** CU-104 | **Caso de Uso:** Verificar la Salud del Sistema (vida y disponibilidad)  
**Actor/es:** Plataforma de despliegue (ACT-09)  
**Subsistema:** SS-18 Observabilidad y Operación  
**Calificación:** Importante  
**Descripción:** La plataforma de despliegue —balanceador, orquestador o monitoreo externo— consulta si el sistema está vivo y en condiciones de recibir tráfico, verificando sus dependencias y sus recursos. Con eso decide si le manda tráfico o si reinicia la instancia.

---


**Código:** CU-152 | **Caso de Uso:** Consultar el Registro de Auditoría  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-18 Observabilidad y Operación  
**Calificación:** Importante  
**Descripción:** El administrador consulta qué se hizo en el sistema: quién realizó cada operación que modificó datos, sobre qué, cuándo, desde qué aplicación y con qué resultado. Puede filtrar por persona, tipo de recurso, recurso puntual, período y resultado. También consulta la auditoría de datos: qué registro de qué entidad se dio de alta, se modificó, se dio de baja o se reactivó, quién lo hizo y, campo por campo, qué cambió.

---


**Código:** CU-172 | **Caso de Uso:** Configurar los Parámetros de un Proceso Automático  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-18 Observabilidad y Operación  
**Calificación:** Importante  
**Descripción:** El administrador consulta y modifica los parámetros de cada proceso automático de su distribuidora: el planificador de flota (CU-105), la anticipación de recompra (CU-106), la agrupación por recorrido (CU-107), la recuperación de envases (CU-108) y el despacho express (CU-148 y CU-149). Cada proceso lleva sus propios parámetros —plazos, umbrales, vigencias y hora de ejecución—.

---


**Código:** CU-173 | **Caso de Uso:** Configurar la Frecuencia de las Tareas Programadas  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-18 Observabilidad y Operación  
**Calificación:** Importante  
**Descripción:** El administrador define cada cuánto corre, para su distribuidora, cada tarea programada del sistema: el ciclo de reintentos del despacho, la activación y el vencimiento de reservas, el vencimiento de pedidos de MercadoPago sin pagar y el aviso diario de vencimientos de flota. Sin configuración rigen las frecuencias de siempre.

---


**Código:** CU-105 | **Caso de Uso:** Planificar el Mantenimiento y las Habilitaciones de la Flota  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03), Sistema Automático (ACT-04)  
**Subsistema:** SS-07 Gestión de Choferes y Vehículos  
**Calificación:** Importante  
**Descripción:** A partir del recorrido que el sistema ya registra en cada entrega, un proceso diario estima el consumo de kilómetros de cada vehículo y proyecta cuándo vence cada mantenimiento por kilometraje y cada habilitación por fecha. Con la anticipación configurada, arma las ventanas de taller de menor impacto operativo y se las propone al chofer asignado, de a una por vez; si ninguna prospera, escala al administrador. Un vehículo con una habilitación bloqueante vencida deja de recibir pedidos.

---


**Código:** CU-106 | **Caso de Uso:** Anticipar la Recompra por Consumo Estimado  
**Actor/es:** Cliente (ACT-01), Sistema Automático (ACT-04)  
**Subsistema:** SS-02 Gestión de Pedidos  
**Calificación:** Importante  
**Descripción:** A partir del historial de compras de cada cliente, un proceso diario estima su ritmo de consumo y proyecta cuándo se le agotaría el gas. Con la anticipación configurada, le ofrece reponer con el pedido ya armado y una vigencia limitada. Si el cliente acepta, el pedido se crea y entra al circuito normal de despacho; si la vigencia pasa sin respuesta, la invitación caduca y el sistema respeta un intervalo mínimo antes de volver a ofrecerle.

---


**Código:** CU-107 | **Caso de Uso:** Agrupar Pedidos por Recorrido  
**Actor/es:** Chofer (ACT-02), Sistema Automático (ACT-04)  
**Subsistema:** SS-03 Despacho y Asignación  
**Calificación:** Importante  
**Descripción:** En lugar de asignar cada pedido por separado, un proceso automático agrupa los pedidos programados compatibles —misma zona, franjas cercanas y capacidad de carga del vehículo— en un recorrido ordenado y lo ofrece completo a un chofer por vez. Si ningún chofer lo toma, el lote se deshace y los pedidos vuelven a la asignación individual.

---


**Código:** CU-108 | **Caso de Uso:** Recuperar Envases No Devueltos  
**Actor/es:** Cliente (ACT-01), Administrador (ACT-03), Sistema Automático (ACT-04)  
**Subsistema:** SS-13 Trazabilidad de Envases  
**Calificación:** Importante  
**Descripción:** Sobre el historial de movimientos de envases, un proceso automático detecta los que siguen en poder de un cliente por encima del plazo de tolerancia y abre una gestión escalonada: un recordatorio de devolución, la oferta de devolver el envase en la próxima entrega ya programada y un aviso con el detalle del depósito comprometido. Si al cabo de los plazos el envase sigue sin volver, el caso se escala al administrador, que decide.

---


### SS-21 — Caja, Rendiciones y Cuentas Corrientes


**Código:** CU-225 | **Caso de Uso:** Crear una Caja  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador da de alta una caja de su distribuidora —efectivo, banco o billetera—. Cada caja lleva su saldo, que solo cambia por movimientos del libro. Cada distribuidora tiene una «Caja central» desde el principio.

---


**Código:** CU-264 | **Caso de Uso:** Modificar una Caja  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador edita una caja de su distribuidora —su nombre o su exigencia de sesión— o la desactiva.

---


**Código:** CU-226 | **Caso de Uso:** Abrir la Caja  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador abre la sesión de una caja de efectivo con el monto con que empieza el turno. La sesión es el período entre una apertura y un cierre, y es la unidad del arqueo.

---


**Código:** CU-227 | **Caso de Uso:** Cerrar la Caja con Arqueo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Crítico  
**Descripción:** El administrador cierra la sesión de una caja contando el efectivo que hay y comparándolo con lo que el libro dice que debería haber. La diferencia queda registrada y el saldo se ajusta a lo contado.

---


**Código:** CU-228 | **Caso de Uso:** Registrar una Entrada de Dinero en la Caja  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Crítico  
**Descripción:** El administrador asienta en el libro de una caja una entrada de dinero —un aporte, un cobro, un ingreso que no viene de un pedido— con su categoría, su medio y su motivo; el saldo de la caja sube en el mismo acto. Es uno de los dos únicos caminos manuales por los que cambia un saldo (el otro es la salida, CU-309).

---


**Código:** CU-309 | **Caso de Uso:** Registrar una Salida de Dinero de la Caja  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Crítico  
**Descripción:** El administrador asienta en el libro de una caja una salida de dinero —un gasto de la distribuidora, un retiro, un pago— con su categoría, su medio y su motivo; el saldo de la caja baja en el mismo acto y no puede quedar en negativo si es de efectivo.

---


**Código:** CU-310 | **Caso de Uso:** Transferir Fondos entre Cajas  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador mueve fondos de una caja a otra de su distribuidora: el sistema asienta una salida en la caja de origen y una entrada en la de destino, con la categoría de sistema «transferencia entre cajas», en una sola operación.

---


**Código:** CU-229 | **Caso de Uso:** Anular un Movimiento de Caja  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador corrige un movimiento de caja asentando otro de sentido contrario que lo anula, sin tocar el original. Un movimiento se anula una sola vez.

---


**Código:** CU-340 | **Caso de Uso:** Consultar los Movimientos de Caja  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador consulta el libro de una caja: las entradas y las salidas de dinero de un período, con su tipo, su monto, su motivo, su categoría, su medio y quién las registró.

---


**Código:** CU-230 | **Caso de Uso:** Crear una Categoría de Ingresos y Gastos  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Secundario  
**Descripción:** El administrador da de alta una categoría con que se clasifican los movimientos de caja. Las categorías de sistema vienen cargadas y no se pueden modificar.

---


**Código:** CU-265 | **Caso de Uso:** Modificar una Categoría de Ingresos y Gastos  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Secundario  
**Descripción:** El administrador renombra o desactiva una categoría con que se clasifican los movimientos de caja. Las categorías de sistema no se pueden modificar.

---


**Código:** CU-231 | **Caso de Uso:** Generar la Rendición Diaria del Chofer  
**Actor/es:** Sistema Automático (ACT-04)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** Un proceso temporal abre, al cierre de cada día, la rendición de cada chofer que entregó pedidos cobrados en efectivo y todavía no los rindió. La rendición reúne esos pedidos y los cobros de cuenta corriente hechos en la calle.

---


**Código:** CU-232 | **Caso de Uso:** Declarar el Efectivo Rendido  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Crítico  
**Descripción:** El chofer declara cuánto efectivo entrega y qué gastos pagó con la cobranza, desde su aplicación; el administrador puede hacerlo por él desde el panel. La rendición queda presentada con su diferencia.

---


**Código:** CU-233 | **Caso de Uso:** Aprobar la Rendición del Chofer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Crítico  
**Descripción:** El administrador revisa la rendición presentada por el chofer, resuelve la diferencia y la aprueba: el efectivo entra a la caja que elige. Reabrirla para que se corrija es CU-330.

---


**Código:** CU-330 | **Caso de Uso:** Reabrir la Rendición del Chofer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador reabre una rendición presentada para que el chofer la corrija.

---


**Código:** CU-234 | **Caso de Uso:** Avisar las Rendiciones sin Cerrar  
**Actor/es:** Sistema Automático (ACT-04); actores secundarios: Servicio de correo (ACT-08)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** Un proceso temporal avisa por correo a los administradores de cada distribuidora de las rendiciones de días anteriores que siguen abiertas o presentadas sin aprobar. Cada rendición se marca como avisada para no repetir el mismo correo.

---


**Código:** CU-235 | **Caso de Uso:** Habilitar la Cuenta Corriente de un Cliente  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador abre la cuenta corriente de un cliente en su distribuidora, con la razón social, la condición fiscal, el límite de crédito y el plazo de pago. Modificarla o bloquearla es CU-331.

---


**Código:** CU-331 | **Caso de Uso:** Modificar la Cuenta Corriente de un Cliente  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador cambia los términos o el estado de la cuenta corriente de un cliente: la modifica, la bloquea o la cierra.

---


**Código:** CU-236 | **Caso de Uso:** Vender a Cuenta Corriente  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Crítico  
**Descripción:** El administrador crea desde el panel un pedido pagado a cuenta corriente, después de verificar que el cliente tenga crédito. Cuando el pedido se entrega, el sistema asienta el cargo en la cuenta (CU-332).

---


**Código:** CU-332 | **Caso de Uso:** Asentar el Cargo de una Venta a Cuenta Corriente  
**Actor/es:** Sistema Automático (ACT-04)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Crítico  
**Descripción:** Cuando se entrega un pedido a cuenta corriente, el sistema asienta el cargo de la venta en la cuenta del cliente, con su vencimiento.

---


**Código:** CU-237 | **Caso de Uso:** Registrar un Pago de Cuenta Corriente  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Crítico  
**Descripción:** El administrador registra el cobro de un cliente a cuenta corriente, o el chofer lo registra al cobrarlo en la calle. El pago se aplica a las deudas más antiguas. La corrección del saldo con notas de crédito y de débito es CU-329.

---


**Código:** CU-329 | **Caso de Uso:** Registrar un Ajuste de Cuenta Corriente  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador corrige el saldo de una cuenta corriente con una nota de crédito o de débito.

---


**Código:** CU-238 | **Caso de Uso:** Consultar el Estado de Cuenta de un Cliente  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador consulta el estado de cuenta de un cliente: los cargos, los pagos y los ajustes de un período, con el saldo corrido, el crédito disponible y la antigüedad de su deuda.

---


**Código:** CU-239 | **Caso de Uso:** Consultar la Antigüedad de la Deuda  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Secundario  
**Descripción:** El administrador consulta cuánto se le debe a la distribuidora y desde cuándo, repartido en tramos de antigüedad: de 0 a 30 días, de 31 a 60, de 61 a 90 y más de 90.

---


**Código:** CU-240 | **Caso de Uso:** Crear una Regla de Comisión por Entrega  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador define cuánto gana un chofer por entrega: por unidad, por pedido o como porcentaje del total, para un chofer, un producto o todos, con su vigencia. Cambiarla es CU-333.

---


**Código:** CU-333 | **Caso de Uso:** Modificar una Regla de Comisión por Entrega  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador cambia una regla de comisión.

---


**Código:** CU-241 | **Caso de Uso:** Registrar la Comisión de una Entrega  
**Actor/es:** Sistema Automático (ACT-04)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** Cuando un pedido se entrega, el sistema calcula y asienta la comisión que gana el chofer con la regla vigente en ese momento. Es automático; el proceso de conciliación nocturno genera las que falten.

---


**Código:** CU-242 | **Caso de Uso:** Liquidar las Comisiones de un Chofer  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador reúne las comisiones y las deducciones de un chofer en un período en una liquidación en borrador. Aprobarla es CU-334 y anularla, CU-335.

---


**Código:** CU-334 | **Caso de Uso:** Aprobar una Liquidación de Comisiones  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador aprueba una liquidación en borrador.

---


**Código:** CU-335 | **Caso de Uso:** Anular una Liquidación de Comisiones  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador anula una liquidación y libera sus asientos.

---


**Código:** CU-243 | **Caso de Uso:** Registrar el Pago de una Liquidación  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador paga una liquidación aprobada: el neto sale de la caja que elige y la liquidación queda pagada.

---


**Código:** CU-347 | **Caso de Uso:** Anular el Pago de una Liquidación  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador deshace el pago de una liquidación de comisiones que se pagó por error o por la caja equivocada. El dinero vuelve a entrar a la misma caja de la que salió y la liquidación queda aprobada, lista para pagarse de nuevo o para anularse. Exige el motivo. Es la única forma de corregir un pago.

---


**Código:** CU-244 | **Caso de Uso:** Consultar Mis Comisiones  
**Actor/es:** Chofer (ACT-02)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Secundario  
**Descripción:** El chofer consulta desde su aplicación sus comisiones y sus deducciones de un período, y cuánto tiene sin liquidar.

---


**Código:** CU-245 | **Caso de Uso:** Consultar el Tablero Financiero  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-21 Caja, Rendiciones y Cuentas Corrientes  
**Calificación:** Importante  
**Descripción:** El administrador ve en una sola pantalla el estado del dinero de su distribuidora: el saldo por caja, las rendiciones pendientes, la deuda total y vencida de las cuentas corrientes y las comisiones a liquidar.

---


### SS-19 — Personal y Legajos


**Código:** CU-176 | **Caso de Uso:** Consultar los Puestos de Trabajo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador consulta el catálogo de puestos de trabajo de su distribuidora (chofer, ayudante, depósito, administración, vendedor y los que agregue), cada uno con una categoría que gobierna las reglas que se le aplican al personal que lo ocupa y con la cantidad de empleados activos que lo ocupan.

---


**Código:** CU-255 | **Caso de Uso:** Crear un Puesto de Trabajo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador crea un puesto de trabajo en su distribuidora, con un nombre libre y una categoría que gobierna las reglas que se le aplican al personal que lo ocupa.

---


**Código:** CU-256 | **Caso de Uso:** Modificar un Puesto de Trabajo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador modifica el nombre, la categoría o la marca de activo de un puesto de trabajo de su distribuidora.

---


**Código:** CU-257 | **Caso de Uso:** Dar de Baja un Puesto de Trabajo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador da de baja un puesto de trabajo de su distribuidora, mientras no tenga empleados activos.

---


**Código:** CU-177 | **Caso de Uso:** Registrar el Legajo de un Empleado  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Crítico  
**Descripción:** El administrador da de alta el legajo de una persona que trabaja en su distribuidora, sea chofer, ayudante, personal de depósito, administrativo o vendedor: sus datos personales, su puesto, su fecha de ingreso y su modalidad de contratación. Tenga o no cuenta de acceso al sistema, todo empleado existe como legajo. Es una extensión opcional del alta de un chofer (CU-031).

---


**Código:** CU-178 | **Caso de Uso:** Modificar el Legajo de un Empleado  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador corrige los datos de un legajo —domicilio, teléfono, puesto, modalidad de contratación—. La salida normal de una persona es el egreso (CU-181) y un alta equivocada se elimina con CU-311.

---


**Código:** CU-311 | **Caso de Uso:** Dar de Baja el Legajo de un Empleado  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador da de baja el legajo de un empleado cuando fue un alta equivocada, mientras no tenga cuenta de acceso. La salida normal de una persona es el egreso (CU-181).

---


**Código:** CU-179 | **Caso de Uso:** Consultar el Legajo de un Empleado  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador abre la ficha completa de un empleado: sus datos personales, su puesto, su fecha de ingreso, su estado, si tiene cuenta de acceso y, si es chofer, el vínculo con su ficha de reparto.

---


**Código:** CU-180 | **Caso de Uso:** Consultar el Listado de Empleados  
**Actor/es:** Administrador (ACT-03), Administrador General (ACT-05)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador consulta el listado de empleados de su distribuidora, con filtros por nombre, puesto, categoría, estado, cuenta de acceso y estado de la documentación, y con el peor vencimiento de cada persona.

---


**Código:** CU-181 | **Caso de Uso:** Registrar el Egreso de un Empleado  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Crítico  
**Descripción:** El administrador da de baja a una persona de la distribuidora con su fecha y su motivo (renuncia, despido, fin de contrato, jubilación u otro). Si tenía cuenta de acceso queda bloqueada y, si era chofer, queda deshabilitado y se le libera el vehículo. El reingreso es CU-312.

---


**Código:** CU-312 | **Caso de Uso:** Reingresar a un Empleado  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador reingresa a un empleado egresado: el legajo vuelve a estar activo con una fecha de ingreso nueva y sin datos de egreso.

---


**Código:** CU-182 | **Caso de Uso:** Otorgar una Cuenta de Acceso a un Empleado  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador le da acceso al sistema a un empleado que tiene legajo y no tiene cuenta. El rol de la cuenta lo decide la categoría de su puesto: los choferes entran con el rol chofer y la administración con el rol administrador; el resto del personal no tiene cuenta.

---


**Código:** CU-183 | **Caso de Uso:** Registrar el Curso de Transporte de Mercancías Peligrosas del Empleado  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Crítico  
**Descripción:** El administrador registra el curso de transporte de mercancías peligrosas que habilita a un chofer a llevar gas licuado, con el número de certificado y su fecha de vencimiento. Mientras el curso esté vencido, el chofer no recibe pedidos.

---


**Código:** CU-184 | **Caso de Uso:** Registrar el Examen Psicofísico del Empleado  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Crítico  
**Descripción:** El administrador registra el examen psicofísico de un chofer con su fecha de vencimiento. Mientras esté vencido, el chofer no recibe pedidos.

---


**Código:** CU-185 | **Caso de Uso:** Registrar el Alta en la ART del Empleado  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador registra la cobertura de la aseguradora de riesgos del trabajo de un empleado, con la aseguradora, el número de póliza y la fecha en que vence la cobertura. A diferencia de los documentos del chofer, aplica a todo el personal y no inhabilita para el despacho.

---


**Código:** CU-186 | **Caso de Uso:** Adjuntar un Archivo al Legajo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Secundario  
**Descripción:** El administrador adjunta un archivo al legajo de un empleado —el escaneo del documento, el contrato, un certificado— con una etiqueta que dice qué es.

---


**Código:** CU-187 | **Caso de Uso:** Consultar los Vencimientos del Personal  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador ve qué documentación del personal vence dentro de una ventana de días —licencia de conducir, curso de mercancías peligrosas, examen psicofísico, alta en la ART— y, para cada empleado, qué documentos le faltan y si está inhabilitado para el despacho.

---


**Código:** CU-188 | **Caso de Uso:** Avisar los Vencimientos Próximos del Personal  
**Actor/es:** Sistema Automático (ACT-04); actores secundarios: Servicio de correo (ACT-08)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** Todos los días el sistema revisa qué documentación del personal está por vencer, ya venció o falta cargar, y avisa por correo a los administradores de cada distribuidora. Reutiliza el aviso diario de los vencimientos de la flota.

---


**Código:** CU-189 | **Caso de Uso:** Registrar la Asistencia de un Empleado  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador carga a mano la jornada de un empleado —hora de ingreso y de egreso—. La corrección de una jornada es CU-313 y la consulta de la asistencia, CU-314.

---


**Código:** CU-313 | **Caso de Uso:** Corregir la Asistencia de un Empleado  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador corrige el ingreso o el egreso de una jornada ya cargada y deja una nota que explique el cambio.

---


**Código:** CU-314 | **Caso de Uso:** Consultar la Asistencia de los Empleados  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador consulta las jornadas de un día, de un período o de un empleado, con los presentes y las jornadas sin cerrar.

---


**Código:** CU-190 | **Caso de Uso:** Registrar el Inicio de la Jornada  
**Actor/es:** Chofer (ACT-02)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Secundario  
**Descripción:** El chofer marca desde su aplicación cuándo empieza su jornada de trabajo. El fin de la jornada es CU-315.

---


**Código:** CU-315 | **Caso de Uso:** Registrar el Fin de la Jornada  
**Actor/es:** Chofer (ACT-02)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Secundario  
**Descripción:** El chofer marca desde su aplicación cuándo termina su jornada de trabajo.

---


**Código:** CU-191 | **Caso de Uso:** Registrar una Licencia o Ausencia  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador registra una licencia o ausencia de un empleado —vacaciones, enfermedad, accidente de trabajo, estudio, casamiento, nacimiento, duelo, licencia sin goce, suspensión o ausencia injustificada— con su período. La modificación es CU-316 y la cancelación, CU-317.

---


**Código:** CU-316 | **Caso de Uso:** Modificar una Licencia o Ausencia  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador cambia el tipo, el período o el motivo de una licencia mientras está solicitada.

---


**Código:** CU-317 | **Caso de Uso:** Cancelar una Licencia o Ausencia  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador cancela una licencia mientras no haya terminado.

---


**Código:** CU-192 | **Caso de Uso:** Aprobar una Solicitud de Licencia  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador aprueba una licencia solicitada por un empleado. La consulta de las licencias es CU-319 y el rechazo, CU-318.

---


**Código:** CU-318 | **Caso de Uso:** Rechazar una Solicitud de Licencia  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador rechaza una solicitud de licencia indicando el motivo.

---


**Código:** CU-319 | **Caso de Uso:** Consultar las Licencias  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** El administrador consulta las licencias de su distribuidora por período, estado, tipo o empleado.

---


**Código:** CU-193 | **Caso de Uso:** Consultar el Saldo de Vacaciones de un Empleado  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Secundario  
**Descripción:** El administrador consulta cuántos días de vacaciones le corresponden a un empleado en un año, cuántos tomó y cuántos le quedan.

---


**Código:** CU-194 | **Caso de Uso:** Consultar el Tablero de Personal  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Secundario  
**Descripción:** El administrador ve, en una sola tarjeta de su pantalla de inicio, cuántos empleados activos tiene por puesto, cuántos están presentes hoy, cuántos de licencia y cómo está la documentación del personal.

---


**Código:** CU-246 | **Caso de Uso:** Verificar la Habilitación Laboral del Chofer  
**Actor/es:** Ninguno directo: es un caso incluido; lo inician CU-012, CU-013 y CU-015  
**Subsistema:** SS-19 Personal y Legajos  
**Calificación:** Importante  
**Descripción:** Antes de asignarle o aceptarle un pedido a un chofer, el sistema comprueba que su situación laboral lo habilite: que su legajo esté activo, que no tenga una licencia aprobada que cubra el día de hoy y que no tenga vencida una documentación bloqueante cuyo dueño es su empleado. Lo incluyen CU-012, CU-013 y CU-015.

---


### SS-08 — Gestión de Productos e Inventario (ampliación: stock físico y carga del camión, C-09)

**Código:** CU-207 | **Caso de Uso:** Consultar los Depósitos  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador consulta los depósitos y sucursales de su distribuidora, que son los lugares donde se guarda el stock físico: el listado y el detalle de uno con sus saldos.

---


**Código:** CU-258 | **Caso de Uso:** Registrar un Depósito  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador da de alta un depósito o sucursal de su distribuidora. El primer depósito que se crea queda como predeterminado.

---


**Código:** CU-259 | **Caso de Uso:** Modificar un Depósito  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador modifica los datos de un depósito o sucursal de su distribuidora, o lo desactiva y lo reactiva.

---


**Código:** CU-260 | **Caso de Uso:** Dar de Baja un Depósito  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador da de baja un depósito o sucursal de su distribuidora. La baja es lógica y solo se admite cuando el depósito no tiene saldo y no es el predeterminado.

---


**Código:** CU-273 | **Caso de Uso:** Marcar el Depósito Predeterminado  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador elige cuál de sus depósitos es el predeterminado, el que usan por omisión la entrega de un pedido y el ajuste del catálogo.

---


**Código:** CU-274 | **Caso de Uso:** Registrar el Conteo Inicial de un Depósito  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador carga lo que hay físicamente en un depósito, por tipo de garrafa y condición, una sola vez por depósito.

---


**Código:** CU-208 | **Caso de Uso:** Consultar el Stock por Ubicación  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Crítico  
**Descripción:** El administrador consulta cuántas garrafas llenas, vacías y defectuosas hay en cada depósito y en cada camión.

---


**Código:** CU-279 | **Caso de Uso:** Consultar el Resumen de Stock  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador compara, por tipo de garrafa, lo que hay en los depósitos con lo que hay en los camiones, y ve lo reservado, lo vendible y el mínimo.

---


**Código:** CU-209 | **Caso de Uso:** Consultar los Movimientos de Stock  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador consulta el libro de movimientos de stock con filtros por tipo de garrafa, ubicación, motivo y fechas.

---


**Código:** CU-210 | **Caso de Uso:** Configurar el Stock Mínimo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Secundario  
**Descripción:** El administrador define, para cada depósito y tipo de garrafa, el mínimo de unidades llenas por debajo del cual el sistema avisa (CU-211). Parte de la consulta de los mínimos vigentes (CU-297).

---


**Código:** CU-297 | **Caso de Uso:** Consultar el Stock Mínimo  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Secundario  
**Descripción:** El administrador consulta los mínimos de llenas vigentes por depósito y tipo de garrafa, junto con las llenas que hay hoy y si ya se avisó.

---


**Código:** CU-211 | **Caso de Uso:** Avisar el Stock Bajo  
**Actor/es:** Sistema Automático (ACT-04); actores secundarios: Servicio de correo (ACT-08)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** Cada día a la mañana el sistema revisa los depósitos que bajaron de su mínimo de unidades llenas y avisa por correo a los administradores de la distribuidora, una sola vez hasta que el stock se recupere.

---


**Código:** CU-212 | **Caso de Uso:** Transferir Stock entre Depósitos  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Secundario  
**Descripción:** El administrador traslada unidades de uno o más tipos de garrafa de un depósito a otro, o devuelve a un depósito lo que un camión tiene suelto.

---


**Código:** CU-276 | **Caso de Uso:** Anular una Transferencia de Stock  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Secundario  
**Descripción:** El administrador corrige una transferencia hecha por error con un contraasiento que la deshace.

---


**Código:** CU-213 | **Caso de Uso:** Registrar un Ajuste o una Merma de Stock  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador corrige el stock de un depósito o un camión por un recuento, una merma, una fuga, una rotura, una pérdida o un hallazgo, con una nota obligatoria.

---


**Código:** CU-275 | **Caso de Uso:** Consultar los Ajustes de Stock  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador consulta los ajustes de stock registrados, con filtros por motivo y fechas, y el detalle de uno.

---


**Código:** CU-218 | **Caso de Uso:** Registrar la Carga del Camión  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Crítico  
**Descripción:** El administrador abre la hoja de carga del día de un camión: elige el vehículo, el chofer que lo tiene en uso, el depósito de salida, el ayudante, si lo hay, y por tipo de garrafa las llenas y los vacíos para canje que se cargan. Abrir la carga no mueve stock: la hoja queda «en carga».

---


**Código:** CU-295 | **Caso de Uso:** Corregir los Renglones de una Carga del Camión  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** Mientras la carga está «en carga», el administrador reemplaza sus renglones: las llenas y los vacíos que se cargan por tipo de garrafa. No mueve stock.

---


**Código:** CU-296 | **Caso de Uso:** Reponer una Carga del Camión  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** Con el camión en ruta, el administrador suma llenas del depósito de origen al camión y el sistema las anota en el renglón de reposición del tipo de garrafa.

---


**Código:** CU-289 | **Caso de Uso:** Cancelar una Carga del Camión  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador cancela, con un motivo, una carga que todavía no salió.

---


**Código:** CU-219 | **Caso de Uso:** Registrar la Salida del Camión  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El chofer, desde su aplicación, o el administrador confirman que el camión salió a repartir: las garrafas de la hoja pasan del depósito al camión.

---


**Código:** CU-220 | **Caso de Uso:** Descontar del Stock Físico lo Entregado  
**Actor/es:** Ninguno directo: es un caso incluido; lo inician CU-020, CU-079 y CU-278  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Crítico  
**Descripción:** Cada vez que se confirma la entrega de un pedido, el sistema descuenta las garrafas llenas entregadas del camión del pedido o, si no tiene saldo, del depósito predeterminado, y acredita los envases vacíos recolectados, en una relación de uno a uno. Lo incluyen CU-020, CU-079 y CU-278.

---


**Código:** CU-221 | **Caso de Uso:** Registrar el Regreso del Camión  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El chofer, desde su aplicación, o el administrador declaran lo que el camión trae de vuelta: llenas y vacías por tipo de garrafa.

---


**Código:** CU-222 | **Caso de Uso:** Cerrar la Rendición de Stock del Camión  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Crítico  
**Descripción:** El administrador revisa lo declarado frente a lo esperado, devuelve el stock del camión al depósito y cierra la carga, con una nota si hay diferencia.

---


**Código:** CU-223 | **Caso de Uso:** Consultar la Carga Actual del Camión  
**Actor/es:** Chofer (ACT-02)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Secundario  
**Descripción:** El chofer consulta desde su aplicación su carga abierta, con lo cargado, lo entregado y lo esperado, y si su distribuidora le exige tenerla abierta para recibir pedidos.

---


**Código:** CU-290 | **Caso de Uso:** Consultar las Cargas del Camión  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador lista las cargas de camión de su distribuidora, con filtros por estado, día, rango de días, vehículo y chofer.

---


**Código:** CU-291 | **Caso de Uso:** Consultar una Carga del Camión  
**Actor/es:** Chofer (ACT-02), Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador, o el chofer de la carga, consulta el detalle de una carga: renglones, esperado, diferencias, pedidos entregados, efectivo de la jornada y movimientos.

---


**Código:** CU-224 | **Caso de Uso:** Conciliar el Stock Vendible con el Físico  
**Actor/es:** Administrador (ACT-03), Sistema Automático (ACT-04); actores secundarios: Servicio de correo (ACT-08)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** Cada noche el sistema compara el stock vendible con el físico menos lo reservado y avisa de la diferencia y de las entregas sin descuento; el administrador consulta la conciliación cuando quiere.

---


**Código:** CU-277 | **Caso de Uso:** Registrar un Ajuste de Conciliación del Vendible  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador corrige el stock vendible de un tipo de garrafa hasta que coincida con el físico menos lo reservado, sin tocar el físico.

---


**Código:** CU-278 | **Caso de Uso:** Reaplicar las Entregas sin Movimiento de Stock  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** El administrador vuelve a descontar el stock físico de las entregas que no pudieron hacerlo, una vez corregida la causa.

---


**Código:** CU-248 | **Caso de Uso:** Verificar la Carga de Camión Abierta del Chofer  
**Actor/es:** Ninguno directo: es un caso incluido; lo inician CU-012, CU-013, CU-015 y CU-080  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Importante  
**Descripción:** Antes de ofrecerle, dejarle aceptar o asignarle un pedido a un chofer, y al mostrarle los pedidos disponibles, el sistema controla su carga de camión: con una carga abierta solo recibe pedidos si está en ruta y con el camión de la carga; sin carga, recibe salvo que la distribuidora exija tenerla. Lo incluyen CU-012, CU-013, CU-015 y CU-080.

---


**Código:** CU-249 | **Caso de Uso:** Configurar el Control de Carga de Camión Abierta  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Secundario  
**Descripción:** El administrador define si su distribuidora exige una carga de camión abierta para recibir pedidos. Parte de la consulta del valor vigente (CU-298).

---


**Código:** CU-298 | **Caso de Uso:** Consultar el Control de Carga de Camión Abierta  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Secundario  
**Descripción:** El administrador consulta si su distribuidora exige una carga de camión abierta para recibir pedidos.

---


**Código:** CU-250 | **Caso de Uso:** Aplicar un Movimiento de Stock  
**Actor/es:** Ninguno directo: es un caso incluido; lo inician CU-212, CU-213, CU-217, CU-219, CU-220, CU-222, CU-274, CU-276, CU-280 y CU-296  
**Subsistema:** SS-08 Gestión de Productos e Inventario  
**Calificación:** Crítico  
**Descripción:** Cada vez que el stock físico cambia, el sistema asienta los movimientos con su origen y su destino y mueve los saldos de las ubicaciones, sin dejar ninguno negativo. Lo incluyen todos los casos que mueven stock.

---


### SS-20 — Compras (C-09)

**Código:** CU-214 | **Caso de Uso:** Consultar los Proveedores  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Importante  
**Descripción:** El administrador consulta los proveedores de la distribuidora, principalmente las plantas de llenado a las que se compra gas, con búsqueda por término y filtro por tipo, o abre la ficha de uno.

---


**Código:** CU-261 | **Caso de Uso:** Registrar un Proveedor  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Importante  
**Descripción:** El administrador da de alta a un proveedor de la distribuidora, principalmente una planta de llenado a la que se compra gas.

---


**Código:** CU-262 | **Caso de Uso:** Modificar un Proveedor  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Importante  
**Descripción:** El administrador corrige los datos de un proveedor de la distribuidora o lo activa y desactiva.

---


**Código:** CU-263 | **Caso de Uso:** Dar de Baja un Proveedor  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Importante  
**Descripción:** El administrador da de baja a un proveedor de la distribuidora, que deja de listarse pero conserva su historial.

---


**Código:** CU-286 | **Caso de Uso:** Consultar el Historial de Compras de un Proveedor  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Importante  
**Descripción:** El administrador ve lo que se le compró a un proveedor: cuántas recepciones, cuántas garrafas llenas y qué monto, con el listado de remitos, en un rango de fechas.

---


**Código:** CU-215 | **Caso de Uso:** Emitir una Orden de Compra  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Importante  
**Descripción:** El administrador emite una orden de compra a un proveedor para un depósito destino, con los tipos de garrafa, las cantidades, el costo esperado y los envases vacíos que entrega en canje. La orden nace en borrador.

---


**Código:** CU-287 | **Caso de Uso:** Modificar una Orden de Compra  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Secundario  
**Descripción:** El administrador corrige una orden de compra que todavía está en borrador: el proveedor, el depósito, la fecha esperada, las notas o los renglones.

---


**Código:** CU-288 | **Caso de Uso:** Enviar una Orden de Compra  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Importante  
**Descripción:** El administrador confirma una orden de compra en borrador y la pasa a enviada, con el instante de emisión.

---


**Código:** CU-216 | **Caso de Uso:** Cancelar una Orden de Compra  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Secundario  
**Descripción:** El administrador cancela una orden de compra en borrador o enviada que no va a cumplirse, con el motivo.

---


**Código:** CU-282 | **Caso de Uso:** Cerrar una Orden de Compra con Faltante  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Importante  
**Descripción:** El administrador da por cerrada una orden parcialmente recibida porque lo que falta ya no llega, con el motivo.

---


**Código:** CU-283 | **Caso de Uso:** Consultar las Órdenes de Compra  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Importante  
**Descripción:** El administrador consulta las órdenes de compra por estado, proveedor y fecha, abre una con sus renglones y recepciones, o ve lo que falta recibir.

---


**Código:** CU-217 | **Caso de Uso:** Registrar la Recepción de una Compra  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Crítico  
**Descripción:** El administrador registra el remito de ingreso de una compra, con o sin orden: las garrafas llenas recibidas, los vacíos que se llevó la planta y el costo, y el stock del depósito sube.

---


**Código:** CU-280 | **Caso de Uso:** Anular una Recepción de Compra  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Importante  
**Descripción:** El administrador anula una recepción confirmada, con el motivo: el sistema deshace sus movimientos de stock con un contraasiento, recalcula el costo promedio y devuelve lo recibido a la orden.

---


**Código:** CU-281 | **Caso de Uso:** Marcar el Pago de una Recepción  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Secundario  
**Descripción:** El administrador marca una recepción de compra como pagada o impaga. Es solo una marca: no mueve dinero.

---


**Código:** CU-284 | **Caso de Uso:** Consultar las Recepciones de Compra  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Importante  
**Descripción:** El administrador consulta las recepciones de compra por proveedor, orden, estado de pago, estado y fecha, o abre una con sus renglones.

---


**Código:** CU-285 | **Caso de Uso:** Consultar el Costo Promedio de las Garrafas  
**Actor/es:** Administrador (ACT-03)  
**Subsistema:** SS-20 Compras  
**Calificación:** Importante  
**Descripción:** El administrador consulta el costo promedio ponderado de cada tipo de garrafa, el costo de la última compra y las llenas que hay hoy.

---


## 8. Calificación de los Casos de Uso

| Caso de Uso | Subsistema | Actor Principal | Calificación | Estado |
|-------------|------------|-----------------|:------------:|-------------|
| CU-001 Iniciar Sesión | SS-01 | ACT-01, ACT-02, ACT-03 | Crítico | Implementado |
| CU-002 Registrarse como Cliente | SS-01 | ACT-01 | Crítico | Implementado |
| CU-004 Consultar el Perfil de Usuario | SS-01 | ACT-01, ACT-02 | Importante | Implementado |
| CU-005 Crear un Pedido | SS-02 | ACT-01 | Crítico | Implementado |
| CU-006 Consultar el Detalle de un Pedido | SS-02 | ACT-01, ACT-02, ACT-03 | Crítico | Implementado |
| CU-007 Consultar el Historial de Pedidos | SS-02 | ACT-01 | Importante | Implementado |
| CU-008 Cancelar un Pedido (Cliente) | SS-02 | ACT-01 | Importante | Implementado |
| CU-009 Liberar un Pedido (Chofer) | SS-02 | ACT-02 | Importante | Implementado |
| CU-010 Cancelar un Pedido (Administrador) | SS-02 | ACT-03 | Importante | Implementado |
| CU-011 Consultar Todos los Pedidos | SS-02 | ACT-03 | Importante | Implementado |
| CU-012 Asignar un Chofer Manualmente | SS-03 | ACT-03 | Secundario | Implementado |
| CU-013 Asignar un Pedido Automáticamente por Proximidad | SS-03 | ACT-04 | Crítico | Implementado, con funcionalidad planificada |
| CU-014 Vencer la Oferta y Ofrecer al Siguiente Chofer | SS-03 | ACT-04 | Crítico | Implementado |
| CU-015 Aceptar un Pedido | SS-03 | ACT-02 | Crítico | Implementado |
| CU-016 Rechazar un Pedido Ofrecido | SS-03 | ACT-02 | Importante | Implementado |
| CU-017 Modificar la Ubicación GPS del Chofer | SS-04 | ACT-02 | Crítico | Implementado, con funcionalidad planificada (C-10) |
| CU-018 Marcar un Pedido "En Camino" | SS-04 | ACT-02 | Crítico | Implementado |
| CU-019 Avisar la Llegada al Cliente | SS-04 | ACT-02 | Importante | Implementado |
| CU-020 Confirmar una Entrega Manualmente | SS-04 | ACT-03, ACT-05 | Crítico | Implementado |
| CU-022 Activar la Disponibilidad | SS-04 | ACT-02 | Crítico | Implementado |
| CU-023 Registrar un Reclamo | SS-05 | ACT-01 | Importante | Implementado |
| CU-024 Consultar los Reclamos | SS-05 | ACT-03 | Importante | Implementado |
| CU-025 Resolver un Reclamo | SS-05 | ACT-03 | Importante | Implementado |
| CU-026 Consultar el Tablero General | SS-06 | ACT-03 | Importante | Implementado |
| CU-027 Consultar el Reporte de Ventas por Chofer | SS-06 | ACT-03 | Importante | Implementado |
| CU-028 Consultar el Reporte de Ventas por Producto | SS-06 | ACT-03 | Importante | Implementado |
| CU-029 Consultar el Reporte por Método de Pago | SS-06 | ACT-03 | Secundario | Implementado |
| CU-030 Consultar el Gráfico de Ventas (últimos 7 días) | SS-06 | ACT-03 | Secundario | Implementado |
| CU-031 Registrar un Chofer (Gestión de la Flota) | SS-07 | ACT-03 | Crítico | Implementado |
| CU-032 Validar un Chofer | SS-07 | ACT-03 | Crítico | Implementado |
| CU-033 Activar un Chofer | SS-07 | ACT-03 | Importante | Implementado |
| CU-034 Registrar un Vehículo del Chofer | SS-07 | ACT-03 | Importante | Implementado |
| CU-035 Consultar el Listado de Choferes | SS-07 | ACT-03 | Importante | Implementado |
| CU-036 Crear un Producto (Garrafa) | SS-08 | ACT-03 | Crítico | Implementado |
| CU-037 Modificar el Precio de un Producto | SS-08 | ACT-03 | Crítico | Implementado |
| CU-038 Modificar el Stock de un Producto | SS-08 | ACT-03 | Crítico | Implementado |
| CU-039 Configurar las Promociones por Cantidad | SS-08 | ACT-03 | Importante | Implementado |
| CU-040 Desactivar un Producto | SS-08 | ACT-03 | Importante | Implementado |
| CU-041 Consultar el Catálogo de Productos (Cliente) | SS-08 | ACT-01 | Crítico | Implementado |
| CU-042 Crear una Franja Horaria | SS-09 | ACT-03 | Importante | Implementado |
| CU-043 Modificar una Franja Horaria | SS-09 | ACT-03 | Importante | Implementado |
| CU-044 Seleccionar una Franja Horaria al Crear un Pedido | SS-09 | ACT-01 | Importante | Implementado |
| CU-045 Consultar las Franjas Horarias Disponibles | SS-09 | ACT-01 | Importante | Implementado |
| CU-046 Consultar las Direcciones de Entrega del Cliente | SS-02 | ACT-01 | Importante | Implementado |
| CU-047 Recuperar la Contraseña | SS-01 | ACT-01, ACT-02, ACT-03 | Importante | Implementado |
| CU-048 Procesar el Pago con MercadoPago | SS-14 | ACT-06 | Crítico | Implementado |
| CU-049 Consultar las Ganancias del Chofer | SS-07 | ACT-02, ACT-03 | Importante | Implementado |
| CU-050 Bloquear un Usuario | SS-01 | ACT-03, ACT-05 | Secundario | Implementado |
| CU-051 Consultar el Listado de Vehículos | SS-07 | ACT-03 | Importante | Implementado |
| CU-052 Registrar una Distribuidora | SS-10 | ACT-05 | Crítico | Implementado |
| CU-053 Consultar las Distribuidoras | SS-10 | ACT-05 | Crítico | Implementado |
| CU-054 Modificar los Datos de una Distribuidora | SS-10 | ACT-05 | Crítico | Implementado |
| CU-055 Dar de Baja una Distribuidora | SS-10 | ACT-05 | Importante | Implementado |
| CU-056 Crear un Polígono de Cobertura | SS-11 | ACT-03, ACT-05 | Importante | Implementado |
| CU-057 Consultar los Polígonos de Cobertura | SS-11 | ACT-03, ACT-05 | Secundario | Implementado |
| CU-058 Validar la Cobertura de una Dirección | SS-11 | ACT-01, ACT-03, ACT-05 | Crítico | Implementado |
| CU-059 Dar de Baja un Polígono de Cobertura | SS-11 | ACT-03, ACT-05 | Secundario | Implementado |
| CU-060 Registrar una Incidencia de Entrega | SS-12 | ACT-02, ACT-03, ACT-05 | Crítico | Implementado |
| CU-061 Consultar las Incidencias | SS-12 | ACT-03, ACT-05 | Importante | Implementado |
| CU-062 Consultar las Incidencias de un Pedido | SS-12 | ACT-02, ACT-03, ACT-05 | Secundario | Implementado |
| CU-063 Resolver una Incidencia | SS-12 | ACT-03, ACT-05 | Importante | Implementado |
| CU-064 Calificar un Pedido (cliente↔chofer) | SS-12 | ACT-01, ACT-02 | Crítico | Implementado |
| CU-065 Consultar el Promedio de Calificaciones de un Usuario | SS-12 | ACT-01, ACT-02, ACT-03, ACT-05 | Secundario | Implementado |
| CU-066 Consultar el Historial de Calificaciones Recibidas | SS-12 | ACT-03, ACT-05 | Secundario | Implementado |
| CU-067 Dar de Alta un Envase Físico | SS-13 | ACT-03, ACT-05 | Importante | Implementado |
| CU-068 Asignar los Envases a un Pedido | SS-13 | ACT-02, ACT-03, ACT-05 | Crítico | Implementado |
| CU-069 Consultar el Parque de Envases | SS-13 | ACT-03, ACT-05 | Importante | Implementado |
| CU-070 Registrar un Movimiento de Envase (cambio de estado) | SS-13 | ACT-02, ACT-03, ACT-05 | Crítico | Implementado |
| CU-071 Consultar el Historial de Movimientos de un Envase | SS-13 | ACT-03, ACT-05 | Importante | Implementado |
| CU-072 Crear una Reserva Programada con Seña | SS-15 | ACT-01, ACT-02, ACT-03 | Crítico | Implementado |
| CU-073 Consultar las Reservas y el Estado de la Seña | SS-15 | ACT-03, ACT-05 | Importante | Implementado |
| CU-074 Confirmar la Seña Cobrada en Efectivo | SS-15 | ACT-03, ACT-05 | Crítico | Implementado |
| CU-075 Activar las Reservas Vencidas Automáticamente | SS-15 | ACT-04 | Crítico | Implementado |
| CU-076 Expirar las Reservas sin Seña Pagada | SS-15 | ACT-04 | Importante | Implementado |
| CU-077 Expirar los Pedidos de MercadoPago sin Pagar | SS-15 | ACT-04 | Importante | Implementado |
| CU-078 Consultar el Código de Entrega (QR del chofer) | SS-04 | ACT-02, ACT-03, ACT-05 | Crítico | Implementado |
| CU-079 Confirmar una Entrega Escaneando el QR (cliente) | SS-04 | ACT-01, ACT-03, ACT-05 | Crítico | Implementado |
| CU-080 Consultar el Pool de Pedidos Disponibles | SS-02 | ACT-02, ACT-03, ACT-05 | Crítico | Implementado |
| CU-081 Consultar los Pedidos Asignados al Chofer | SS-02 | ACT-02, ACT-03, ACT-05 | Crítico | Implementado |
| CU-082 Crear un Usuario Base | SS-01 | — | Importante | Implementado |
| CU-083 Consultar los Usuarios | SS-01 | ACT-03 | Importante | Implementado |
| CU-085 Dar de Baja un Usuario | SS-01 | ACT-03, ACT-05 | Importante | Implementado |
| CU-086 Registrar un Administrador | SS-16 | ACT-03, ACT-05 | Importante | Implementado |
| CU-087 Crear el Primer Administrador General | SS-16 | ACT-10 | Importante | Implementado |
| CU-088 Consultar los Administradores | SS-16 | ACT-03 | Secundario | Implementado |
| CU-089 Consultar los Roles | SS-16 | ACT-05 | Importante | Implementado |
| CU-092 Consultar el Listado de Clientes | SS-16 | ACT-03 | Importante | Implementado |
| CU-094 Modificar la Ubicación del Cliente | SS-16 | ACT-01, ACT-03 | Secundario | Implementado |
| CU-095 Dar de Baja un Cliente | SS-16 | ACT-05 | Importante | Implementado |
| CU-096 Modificar el Perfil del Chofer | SS-07 | ACT-03 | Importante | Implementado |
| CU-097 Dar de Baja un Chofer | SS-07 | ACT-03 | Importante | Implementado |
| CU-100 Enviar una Notificación de Prueba | SS-17 | ACT-05 | Secundario | Implementado |
| CU-101 Reenviar la Notificación de Confirmación de Pedido | SS-17 | ACT-05 | Secundario | Implementado |
| CU-102 Probar el Servicio de Correo | SS-17 | ACT-05 | Secundario | Implementado |
| CU-104 Verificar la Salud del Sistema (vida y disponibilidad) | SS-18 | ACT-09 | Importante | Implementado |
| CU-105 Planificar el Mantenimiento y las Habilitaciones de la Flota | SS-07 | ACT-02, ACT-03, ACT-04 | Importante | Planificado (C-14) |
| CU-106 Anticipar la Recompra por Consumo Estimado | SS-02 | ACT-01, ACT-04 | Importante | Planificado (C-16) |
| CU-107 Agrupar Pedidos por Recorrido | SS-03 | ACT-02, ACT-04 | Importante | Planificado (C-19) |
| CU-108 Recuperar Envases No Devueltos | SS-13 | ACT-01, ACT-03, ACT-04 | Importante | Planificado (C-15) |
| CU-109 Consultar el Detalle del Chofer | SS-07 | ACT-03 | Importante | Implementado |
| CU-110 Buscar un Chofer por Usuario | SS-07 | ACT-03 | Importante | Implementado |
| CU-111 Modificar un Vehículo | SS-07 | ACT-03 | Importante | Implementado |
| CU-112 Dar de Baja un Vehículo | SS-07 | ACT-03 | Importante | Implementado |
| CU-113 Consultar el Detalle del Vehículo | SS-07 | ACT-03 | Importante | Implementado |
| CU-114 Buscar un Vehículo por Patente | SS-07 | ACT-03 | Importante | Implementado |
| CU-115 Consultar los Vehículos de un Chofer | SS-07 | ACT-03, ACT-02 | Importante | Implementado |
| CU-116 Registrar una Dirección de Entrega | SS-02 | ACT-01 | Importante | Implementado, con funcionalidad planificada (C-10) |
| CU-117 Consultar Detalle de una Dirección de Entrega | SS-02 | ACT-01 | Importante | Implementado |
| CU-118 Modificar una Dirección de Entrega | SS-02 | ACT-01 | Importante | Implementado, con funcionalidad planificada (C-10) |
| CU-119 Dar de Baja una Dirección de Entrega | SS-02 | ACT-01 | Importante | Implementado |
| CU-120 Marcar una Dirección como Predeterminada | SS-02 | ACT-01 | Importante | Implementado |
| CU-121 Consultar la Dirección Predeterminada | SS-02 | ACT-01 | Importante | Implementado |
| CU-122 Agregar un Ítem al Carrito | SS-02 | ACT-01 | Importante | Implementado |
| CU-123 Modificar la Cantidad de un Ítem del Carrito | SS-02 | ACT-01 | Importante | Implementado |
| CU-124 Quitar un Ítem del Carrito | SS-02 | ACT-01 | Importante | Implementado |
| CU-125 Consultar el Carrito | SS-02 | ACT-01 | Importante | Implementado |
| CU-126 Vaciar el Carrito | SS-02 | ACT-01 | Menor | Implementado |
| CU-127 Cambiar la Dirección de Entrega del Pedido | SS-02 | ACT-01 | Importante | Implementado |
| CU-128 Indicar Quién Recibe el Pedido | SS-02 | ACT-01 | Importante | Implementado |
| CU-129 Consultar el Detalle del Cliente | SS-16 | ACT-03 | Importante | Implementado |
| CU-130 Buscar un Cliente por Usuario | SS-16 | ACT-03 | Importante | Implementado |
| CU-131 Modificar los Datos del Cliente | SS-16 | ACT-05 | Importante | Implementado |
| CU-132 Registrar la Revisión Periódica de un Envase | SS-13 | ACT-03 | Crítico | Implementado |
| CU-133 Consultar la Vigencia de un Envase | SS-13 | ACT-03 | Importante | Implementado |
| CU-134 Consultar los Envases Próximos a Vencer | SS-13 | ACT-03 | Importante | Implementado |
| CU-135 Bloquear el Despacho de un Envase Vencido | SS-13 | ACT-04 | Crítico | Implementado |
| CU-136 Registrar el Seguro del Vehículo | SS-07 | ACT-03 | Crítico | Implementado |
| CU-137 Registrar la Verificación Técnica Vehicular | SS-07 | ACT-03 | Crítico | Implementado |
| CU-138 Registrar la Licencia de Conducir del Chofer | SS-07 | ACT-03 | Crítico | Implementado |
| CU-139 Consultar los Vencimientos de la Flota | SS-07 | ACT-03 | Importante | Implementado |
| CU-140 Programar un Mantenimiento de Vehículo | SS-07 | ACT-03 | Importante | Implementado |
| CU-141 Registrar un Mantenimiento Realizado | SS-07 | ACT-03 | Importante | Implementado |
| CU-142 Avisar los Vencimientos Próximos de la Flota | SS-07 | ACT-04 | Importante | Implementado |
| CU-143 Declarar el Consumo Promedio al Registrarse | SS-02 | ACT-01 | Importante | Implementado |
| CU-144 Modificar el Consumo Promedio Declarado | SS-02 | ACT-01 | Importante | Implementado |
| CU-145 Configurar los Días de Aviso Previo a la Recompra | SS-02 | ACT-01 | Menor | Planificado (C-13) |
| CU-146 Consultar la Fecha Estimada de Recompra | SS-02 | ACT-03 | Importante | Planificado (C-13) |
| CU-147 Realizar una Compra Express | SS-02 | ACT-01 | Crítico | Implementado |
| CU-148 Elegir la Modalidad de Entrega del Pedido | SS-02 | ACT-01 | Importante | Implementado |
| CU-149 Despachar un Pedido Express a un Chofer en Moto | SS-03 | ACT-04 | Crítico | Implementado |
| CU-150 Programar la Vigencia de un Polígono de Cobertura | SS-11 | ACT-03, ACT-05 | Importante | Implementado |
| CU-151 Desactivar los Polígonos de Cobertura Vencidos | SS-11 | ACT-04 | Importante | Implementado |
| CU-152 Consultar el Registro de Auditoría | SS-18 | ACT-03, ACT-05 | Importante | Implementado |
| CU-154 Consultar el Listado de Franjas Horarias | SS-09 | ACT-03, ACT-05 | Importante | Implementado |
| CU-155 Adjuntar un Archivo a una Tarea de Flota | SS-07 | ACT-03 | Importante | Implementado |
| CU-156 Consultar los Adjuntos de una Tarea de Flota | SS-07 | ACT-03 | Secundario | Implementado |
| CU-157 Descargar un Adjunto de Flota | SS-07 | ACT-03 | Secundario | Implementado |
| CU-158 Eliminar un Adjunto de Flota | SS-07 | ACT-03 | Secundario | Implementado |
| CU-159 Almacenar un Archivo | SS-07 | — | Importante | Implementado |
| CU-160 Recuperar un Archivo | SS-07 | — | Secundario | Implementado |
| CU-161 Poner un Vehículo en Uso para un Chofer | SS-07 | ACT-03, ACT-05 | Importante | Implementado |
| CU-162 Liberar el Vehículo en Uso de un Chofer | SS-07 | ACT-03, ACT-05 | Secundario | Implementado |
| CU-163 Consultar el Vehículo en Uso de un Chofer | SS-07 | ACT-03, ACT-05, ACT-02 | Secundario | Implementado |
| CU-164 Consultar el Historial de Vehículos de un Chofer | SS-07 | ACT-03, ACT-05 | Secundario | Implementado |
| CU-165 Consultar el Historial de Choferes de un Vehículo | SS-07 | ACT-03, ACT-05 | Secundario | Implementado |
| CU-166 Tomar un Reclamo Pendiente | SS-05 | ACT-03, ACT-05 | Importante | Implementado |
| CU-167 Reabrir un Reclamo | SS-05 | ACT-03, ACT-05 | Importante | Implementado |
| CU-168 Reintegrar el Pago de un Pedido | SS-14 | ACT-04, ACT-03 | Importante | Implementado |
| CU-169 Registrar el Cambio de Estado de un Pedido | SS-02 | — | Importante | Implementado |
| CU-170 Consultar el Historial de Estados de un Pedido | SS-02 | ACT-01, ACT-02, ACT-03, ACT-05 | Secundario | Implementado |
| CU-171 Configurar los Parámetros de Despacho de la Distribuidora | SS-03 | ACT-03, ACT-05 | Crítico | Implementado |
| CU-172 Configurar los Parámetros de un Proceso Automático | SS-18 | ACT-03, ACT-05 | Importante | Implementado |
| CU-173 Configurar la Frecuencia de las Tareas Programadas | SS-18 | ACT-03, ACT-05 | Importante | Implementado |
| CU-174 Adjuntar la Fotografía de un Reclamo | SS-05 | ACT-01, ACT-03, ACT-05 | Importante | Implementado |
| CU-175 Consultar la Fotografía de un Reclamo | SS-05 | ACT-01, ACT-03, ACT-05 | Secundario | Implementado |
| CU-176 Consultar los Puestos de Trabajo | SS-19 | ACT-03 | Importante | Implementado |
| CU-177 Registrar el Legajo de un Empleado | SS-19 | ACT-03 | Crítico | Implementado |
| CU-178 Modificar el Legajo de un Empleado | SS-19 | ACT-03 | Importante | Implementado |
| CU-179 Consultar el Legajo de un Empleado | SS-19 | ACT-03, ACT-05 | Importante | Implementado |
| CU-180 Consultar el Listado de Empleados | SS-19 | ACT-03, ACT-05 | Importante | Implementado, con funcionalidad planificada |
| CU-181 Registrar el Egreso de un Empleado | SS-19 | ACT-03 | Crítico | Implementado, con funcionalidad planificada |
| CU-182 Otorgar una Cuenta de Acceso a un Empleado | SS-19 | ACT-03 | Importante | Implementado |
| CU-183 Registrar el Curso de Transporte de Mercancías Peligrosas del Empleado | SS-19 | ACT-03 | Crítico | Implementado |
| CU-184 Registrar el Examen Psicofísico del Empleado | SS-19 | ACT-03 | Crítico | Implementado |
| CU-185 Registrar el Alta en la ART del Empleado | SS-19 | ACT-03 | Importante | Implementado |
| CU-186 Adjuntar un Archivo al Legajo | SS-19 | ACT-03 | Secundario | Implementado |
| CU-187 Consultar los Vencimientos del Personal | SS-19 | ACT-03 | Importante | Implementado |
| CU-188 Avisar los Vencimientos Próximos del Personal | SS-19 | ACT-04 | Importante | Implementado |
| CU-189 Registrar la Asistencia de un Empleado | SS-19 | ACT-03 | Importante | Implementado |
| CU-190 Registrar el Inicio de la Jornada | SS-19 | ACT-02 | Secundario | Implementado |
| CU-191 Registrar una Licencia o Ausencia | SS-19 | ACT-03 | Importante | Implementado |
| CU-192 Aprobar una Solicitud de Licencia | SS-19 | ACT-03 | Importante | Implementado |
| CU-193 Consultar el Saldo de Vacaciones de un Empleado | SS-19 | ACT-03 | Secundario | Implementado |
| CU-194 Consultar el Tablero de Personal | SS-19 | ACT-03 | Secundario | Implementado |
| CU-195 Registrar una Carga de Combustible | SS-07 | ACT-03, ACT-02 | Importante | Implementado |
| CU-196 Consultar el Consumo de Combustible de un Vehículo | SS-07 | ACT-03 | Importante | Implementado |
| CU-197 Registrar la Habilitación para Transportar Mercancías Peligrosas | SS-07 | ACT-03 | Crítico | Implementado |
| CU-198 Registrar una Multa de Tránsito | SS-07 | ACT-03 | Importante | Implementado |
| CU-199 Registrar el Pago de una Multa | SS-07 | ACT-03 | Secundario | Implementado |
| CU-200 Imputar una Multa al Chofer | SS-07 | ACT-03 | Secundario | Implementado |
| CU-201 Registrar un Siniestro | SS-07 | ACT-03, ACT-02 | Importante | Implementado |
| CU-202 Cerrar un Siniestro | SS-07 | ACT-03 | Secundario | Implementado |
| CU-203 Consultar el Costo Total de un Vehículo | SS-07 | ACT-03 | Importante | Implementado |
| CU-204 Consultar el Tablero de Costos de la Flota | SS-07 | ACT-03 | Importante | Implementado |
| CU-205 Registrar un Neumático | SS-07 | ACT-03 | Secundario | Implementado |
| CU-206 Registrar un Movimiento de Neumático | SS-07 | ACT-03 | Secundario | Implementado |
| CU-207 Consultar los Depósitos | SS-08 | ACT-03 | Importante | Implementado |
| CU-208 Consultar el Stock por Ubicación | SS-08 | ACT-03 | Crítico | Implementado |
| CU-209 Consultar los Movimientos de Stock | SS-08 | ACT-03 | Importante | Implementado |
| CU-210 Configurar el Stock Mínimo | SS-08 | ACT-03 | Secundario | Implementado |
| CU-211 Avisar el Stock Bajo | SS-08 | ACT-04 | Importante | Implementado |
| CU-212 Transferir Stock entre Depósitos | SS-08 | ACT-03 | Secundario | Implementado |
| CU-213 Registrar un Ajuste o una Merma de Stock | SS-08 | ACT-03 | Importante | Implementado |
| CU-214 Consultar los Proveedores | SS-20 | ACT-03 | Importante | Implementado |
| CU-215 Emitir una Orden de Compra | SS-20 | ACT-03 | Importante | Implementado |
| CU-216 Cancelar una Orden de Compra | SS-20 | ACT-03 | Secundario | Implementado |
| CU-217 Registrar la Recepción de una Compra | SS-20 | ACT-03 | Crítico | Implementado |
| CU-218 Registrar la Carga del Camión | SS-08 | ACT-03 | Crítico | Implementado |
| CU-219 Registrar la Salida del Camión | SS-08 | ACT-02, ACT-03 | Importante | Implementado |
| CU-220 Descontar del Stock Físico lo Entregado | SS-08 | — | Crítico | Implementado |
| CU-221 Registrar el Regreso del Camión | SS-08 | ACT-02, ACT-03 | Importante | Implementado |
| CU-222 Cerrar la Rendición de Stock del Camión | SS-08 | ACT-03 | Crítico | Implementado |
| CU-223 Consultar la Carga Actual del Camión | SS-08 | ACT-02 | Secundario | Implementado |
| CU-224 Conciliar el Stock Vendible con el Físico | SS-08 | ACT-03, ACT-04 | Importante | Implementado |
| CU-225 Crear una Caja | SS-21 | ACT-03 | Importante | Implementado |
| CU-226 Abrir la Caja | SS-21 | ACT-03 | Importante | Implementado |
| CU-227 Cerrar la Caja con Arqueo | SS-21 | ACT-03 | Crítico | Implementado |
| CU-228 Registrar una Entrada de Dinero en la Caja | SS-21 | ACT-03 | Crítico | Implementado |
| CU-229 Anular un Movimiento de Caja | SS-21 | ACT-03 | Importante | Implementado |
| CU-230 Crear una Categoría de Ingresos y Gastos | SS-21 | ACT-03 | Secundario | Implementado |
| CU-231 Generar la Rendición Diaria del Chofer | SS-21 | ACT-04 | Importante | Implementado |
| CU-232 Declarar el Efectivo Rendido | SS-21 | ACT-02, ACT-03 | Crítico | Implementado |
| CU-233 Aprobar la Rendición del Chofer | SS-21 | ACT-03 | Crítico | Implementado |
| CU-234 Avisar las Rendiciones sin Cerrar | SS-21 | ACT-04 | Importante | Implementado |
| CU-235 Habilitar la Cuenta Corriente de un Cliente | SS-21 | ACT-03 | Importante | Implementado |
| CU-236 Vender a Cuenta Corriente | SS-21 | ACT-03 | Crítico | Implementado |
| CU-237 Registrar un Pago de Cuenta Corriente | SS-21 | ACT-03, ACT-02 | Crítico | Implementado |
| CU-238 Consultar el Estado de Cuenta de un Cliente | SS-21 | ACT-03 | Importante | Implementado |
| CU-239 Consultar la Antigüedad de la Deuda | SS-21 | ACT-03 | Secundario | Implementado |
| CU-240 Crear una Regla de Comisión por Entrega | SS-21 | ACT-03 | Importante | Implementado |
| CU-241 Registrar la Comisión de una Entrega | SS-21 | ACT-04 | Importante | Implementado |
| CU-242 Liquidar las Comisiones de un Chofer | SS-21 | ACT-03 | Importante | Implementado |
| CU-243 Registrar el Pago de una Liquidación | SS-21 | ACT-03 | Importante | Implementado |
| CU-244 Consultar Mis Comisiones | SS-21 | ACT-02 | Secundario | Implementado |
| CU-245 Consultar el Tablero Financiero | SS-21 | ACT-03 | Importante | Implementado |
| CU-246 Verificar la Habilitación Laboral del Chofer | SS-19 | — | Importante | Implementado |
| CU-247 Reactivar un Vehículo | SS-07 | ACT-03 | Importante | Implementado |
| CU-248 Verificar la Carga de Camión Abierta del Chofer | SS-08 | — | Importante | Implementado |
| CU-249 Configurar el Control de Carga de Camión Abierta | SS-08 | ACT-03 | Secundario | Implementado |
| CU-250 Aplicar un Movimiento de Stock | SS-08 | — | Crítico | Implementado |
| CU-251 Modificar el Perfil de Usuario | SS-01 | ACT-01, ACT-02 | Importante | Implementado |
| CU-252 Crear un Rol | SS-16 | ACT-05 | Importante | Implementado |
| CU-253 Modificar un Rol | SS-16 | ACT-05 | Importante | Implementado |
| CU-254 Dar de Baja un Rol | SS-16 | ACT-05 | Importante | Implementado |
| CU-255 Crear un Puesto de Trabajo | SS-19 | ACT-03 | Importante | Implementado |
| CU-256 Modificar un Puesto de Trabajo | SS-19 | ACT-03 | Importante | Implementado |
| CU-257 Dar de Baja un Puesto de Trabajo | SS-19 | ACT-03 | Importante | Implementado |
| CU-258 Registrar un Depósito | SS-08 | ACT-03 | Importante | Implementado |
| CU-259 Modificar un Depósito | SS-08 | ACT-03 | Importante | Implementado |
| CU-260 Dar de Baja un Depósito | SS-08 | ACT-03 | Importante | Implementado |
| CU-261 Registrar un Proveedor | SS-20 | ACT-03 | Importante | Implementado |
| CU-262 Modificar un Proveedor | SS-20 | ACT-03 | Importante | Implementado |
| CU-263 Dar de Baja un Proveedor | SS-20 | ACT-03 | Importante | Implementado |
| CU-264 Modificar una Caja | SS-21 | ACT-03 | Importante | Implementado |
| CU-265 Modificar una Categoría de Ingresos y Gastos | SS-21 | ACT-03 | Secundario | Implementado |
| CU-266 Desactivar la Disponibilidad | SS-04 | ACT-02 | Crítico | Implementado |
| CU-267 Desactivar un Chofer | SS-07 | ACT-03 | Importante | Implementado |
| CU-268 Reactivar un Producto | SS-08 | ACT-03 | Importante | Implementado |
| CU-269 Consultar los Productos Inactivos | SS-08 | ACT-03 | Importante | Implementado |
| CU-270 Desbloquear un Usuario | SS-01 | ACT-03, ACT-05 | Secundario | Implementado |
| CU-271 Invalidar un Chofer | SS-07 | ACT-03 | Crítico | Implementado |
| CU-272 Buscar un Usuario | SS-01 | ACT-03 | Importante | Implementado |
| CU-273 Marcar el Depósito Predeterminado | SS-08 | ACT-03 | Importante | Implementado |
| CU-274 Registrar el Conteo Inicial de un Depósito | SS-08 | ACT-03 | Importante | Implementado |
| CU-275 Consultar los Ajustes de Stock | SS-08 | ACT-03 | Importante | Implementado |
| CU-276 Anular una Transferencia de Stock | SS-08 | ACT-03 | Secundario | Implementado |
| CU-277 Registrar un Ajuste de Conciliación del Vendible | SS-08 | ACT-03 | Importante | Implementado |
| CU-278 Reaplicar las Entregas sin Movimiento de Stock | SS-08 | ACT-03 | Importante | Implementado |
| CU-279 Consultar el Resumen de Stock | SS-08 | ACT-03 | Importante | Implementado |
| CU-280 Anular una Recepción de Compra | SS-20 | ACT-03 | Importante | Implementado |
| CU-281 Marcar el Pago de una Recepción | SS-20 | ACT-03 | Secundario | Implementado |
| CU-282 Cerrar una Orden de Compra con Faltante | SS-20 | ACT-03 | Importante | Implementado |
| CU-283 Consultar las Órdenes de Compra | SS-20 | ACT-03 | Importante | Implementado |
| CU-284 Consultar las Recepciones de Compra | SS-20 | ACT-03 | Importante | Implementado |
| CU-285 Consultar el Costo Promedio de las Garrafas | SS-20 | ACT-03 | Importante | Implementado |
| CU-286 Consultar el Historial de Compras de un Proveedor | SS-20 | ACT-03 | Importante | Implementado |
| CU-287 Modificar una Orden de Compra | SS-20 | ACT-03 | Secundario | Implementado |
| CU-288 Enviar una Orden de Compra | SS-20 | ACT-03 | Importante | Implementado |
| CU-289 Cancelar una Carga del Camión | SS-08 | ACT-03 | Importante | Implementado |
| CU-290 Consultar las Cargas del Camión | SS-08 | ACT-03 | Importante | Implementado |
| CU-291 Consultar una Carga del Camión | SS-08 | ACT-02, ACT-03 | Importante | Implementado |
| CU-292 Confirmar el Cobro en Efectivo | SS-14 | ACT-02 | Crítico | Implementado |
| CU-293 Informar el Cobro Impago | SS-14 | ACT-02 | Importante | Implementado |
| CU-294 Resolver un Cobro Impago | SS-14 | ACT-03, ACT-05 | Importante | Implementado |
| CU-295 Corregir los Renglones de una Carga del Camión | SS-08 | ACT-03 | Importante | Implementado |
| CU-296 Reponer una Carga del Camión | SS-08 | ACT-03 | Importante | Implementado |
| CU-297 Consultar el Stock Mínimo | SS-08 | ACT-03 | Secundario | Implementado |
| CU-298 Consultar el Control de Carga de Camión Abierta | SS-08 | ACT-03 | Secundario | Implementado |
| CU-299 Registrar el Cobro en Efectivo como Administrador | SS-14 | ACT-03, ACT-05 | Importante | Implementado |
| CU-300 Registrar el Cobro Impago como Administrador | SS-14 | ACT-03, ACT-05 | Importante | Implementado |
| CU-301 Confirmar una Transferencia | SS-14 | ACT-03, ACT-05 | Importante | Implementado |
| CU-302 Cotizar un Pedido | SS-02 | ACT-01, ACT-03, ACT-05 | Importante | Implementado |
| CU-303 Consultar la Ruta de un Pedido | SS-04 | ACT-01, ACT-02 | Importante | Implementado |
| CU-304 Consultar los Cobros Pendientes | SS-06 | ACT-03, ACT-05 | Secundario | Implementado |
| CU-305 Modificar un Polígono de Cobertura | SS-11 | ACT-03, ACT-05 | Importante | Implementado |
| CU-306 Consultar un Polígono de Cobertura | SS-11 | ACT-03, ACT-05 | Secundario | Implementado |
| CU-307 Activar un Polígono de Cobertura | SS-11 | ACT-03, ACT-05 | Importante | Implementado |
| CU-308 Desactivar un Polígono de Cobertura | SS-11 | ACT-03, ACT-05 | Importante | Implementado |
| CU-309 Registrar una Salida de Dinero de la Caja | SS-21 | ACT-03 | Crítico | Implementado |
| CU-310 Transferir Fondos entre Cajas | SS-21 | ACT-03 | Importante | Implementado |
| CU-311 Dar de Baja el Legajo de un Empleado | SS-19 | ACT-03 | Importante | Implementado |
| CU-312 Reingresar a un Empleado | SS-19 | ACT-03 | Importante | Implementado |
| CU-313 Corregir la Asistencia de un Empleado | SS-19 | ACT-03 | Importante | Implementado |
| CU-314 Consultar la Asistencia de los Empleados | SS-19 | ACT-03 | Importante | Implementado |
| CU-315 Registrar el Fin de la Jornada | SS-19 | ACT-02 | Secundario | Implementado |
| CU-316 Modificar una Licencia o Ausencia | SS-19 | ACT-03 | Importante | Implementado |
| CU-317 Cancelar una Licencia o Ausencia | SS-19 | ACT-03 | Importante | Implementado |
| CU-318 Rechazar una Solicitud de Licencia | SS-19 | ACT-03 | Importante | Implementado |
| CU-319 Consultar las Licencias | SS-19 | ACT-03 | Importante | Implementado |
| CU-320 Modificar una Carga de Combustible | SS-07 | ACT-03 | Importante | Implementado |
| CU-321 Anular una Carga de Combustible | SS-07 | ACT-03 | Importante | Implementado |
| CU-322 Consultar las Cargas de Combustible | SS-07 | ACT-03 | Secundario | Implementado |
| CU-323 Modificar una Multa de Tránsito | SS-07 | ACT-03 | Importante | Implementado |
| CU-324 Anular una Multa de Tránsito | SS-07 | ACT-03 | Importante | Implementado |
| CU-325 Consultar las Multas de Tránsito | SS-07 | ACT-03 | Secundario | Implementado |
| CU-326 Avisar las Multas por Vencer | SS-07 | ACT-04 | Importante | Implementado |
| CU-327 Modificar un Siniestro | SS-07 | ACT-03 | Importante | Implementado |
| CU-328 Consultar los Siniestros | SS-07 | ACT-03 | Secundario | Implementado |
| CU-329 Registrar un Ajuste de Cuenta Corriente | SS-21 | ACT-03 | Importante | Implementado |
| CU-330 Reabrir la Rendición del Chofer | SS-21 | ACT-03 | Importante | Implementado |
| CU-331 Modificar la Cuenta Corriente de un Cliente | SS-21 | ACT-03 | Importante | Implementado |
| CU-332 Asentar el Cargo de una Venta a Cuenta Corriente | SS-21 | ACT-04 | Crítico | Implementado |
| CU-333 Modificar una Regla de Comisión por Entrega | SS-21 | ACT-03 | Importante | Implementado |
| CU-334 Aprobar una Liquidación de Comisiones | SS-21 | ACT-03 | Importante | Implementado |
| CU-335 Anular una Liquidación de Comisiones | SS-21 | ACT-03 | Importante | Implementado |
| CU-336 Cambiar el Correo del Usuario | SS-01 | ACT-01, ACT-02, ACT-03 | Importante | Implementado |
| CU-337 Ajustar el Saldo del Chofer | SS-07 | ACT-03 | Importante | Implementado |
| CU-338 Retomar el Pedido en Curso | SS-02 | ACT-02 | Importante | Implementado |
| CU-339 Modificar un Pedido Pendiente (Administrador) | SS-02 | ACT-03, ACT-05 | Importante | Implementado |
| CU-340 Consultar los Movimientos de Caja | SS-21 | ACT-03, ACT-05 | Importante | Implementado |
| CU-341 Modificar un Pedido Pendiente (Cliente) | SS-02 | ACT-01 | Importante | Implementado |
| CU-342 Activar una Franja Horaria | SS-09 | ACT-03 | Importante | Implementado |
| CU-343 Desactivar una Franja Horaria | SS-09 | ACT-03 | Importante | Implementado |
| CU-344 Consultar el Catálogo de Productos (Administrador) | SS-08 | ACT-03 | Importante | Implementado |
| CU-345 Modificar un Administrador | SS-16 | ACT-03, ACT-05 | Importante | Implementado |
| CU-346 Dar de Baja un Administrador | SS-16 | ACT-03, ACT-05 | Importante | Implementado |
| CU-347 Anular el Pago de una Liquidación | SS-21 | ACT-03 | Importante | Implementado |
| CU-348 Consultar el Reintegro de un Pedido | SS-14 | ACT-01 | Secundario | Implementado |

### Resumen de Calificación

| Calificación | Cantidad | CU |
|:------------:|:--------:|-----|
| **Crítico** | 63 | CU-001, CU-002, CU-005, CU-006, CU-013, CU-014, CU-015, CU-017, CU-018, CU-020, CU-022, CU-031, CU-032, CU-036, CU-037, CU-038, CU-041, CU-048, CU-052, CU-053, CU-054, CU-058, CU-060, CU-064, CU-068, CU-070, CU-072, CU-074, CU-075, CU-078, CU-079, CU-080, CU-081, CU-132, CU-135, CU-136, CU-137, CU-138, CU-147, CU-149, CU-171, CU-177, CU-181, CU-183, CU-184, CU-197, CU-208, CU-217, CU-218, CU-220, CU-222, CU-227, CU-228, CU-232, CU-233, CU-236, CU-237, CU-250, CU-266, CU-271, CU-292, CU-309, CU-332 |
| **Importante** | 218 | CU-004, CU-007, CU-008, CU-009, CU-010, CU-011, CU-016, CU-019, CU-023, CU-024, CU-025, CU-026, CU-027, CU-028, CU-033, CU-034, CU-035, CU-039, CU-040, CU-042, CU-043, CU-044, CU-045, CU-046, CU-047, CU-049, CU-051, CU-055, CU-056, CU-061, CU-063, CU-067, CU-069, CU-071, CU-073, CU-076, CU-077, CU-082, CU-083, CU-085, CU-086, CU-087, CU-089, CU-092, CU-095, CU-096, CU-097, CU-104, CU-105, CU-106, CU-107, CU-108, CU-109, CU-110, CU-111, CU-112, CU-113, CU-114, CU-115, CU-116, CU-117, CU-118, CU-119, CU-120, CU-121, CU-122, CU-123, CU-124, CU-125, CU-127, CU-128, CU-129, CU-130, CU-131, CU-133, CU-134, CU-139, CU-140, CU-141, CU-142, CU-143, CU-144, CU-146, CU-148, CU-150, CU-151, CU-152, CU-154, CU-155, CU-159, CU-161, CU-166, CU-167, CU-168, CU-169, CU-172, CU-173, CU-174, CU-176, CU-178, CU-179, CU-180, CU-182, CU-185, CU-187, CU-188, CU-189, CU-191, CU-192, CU-195, CU-196, CU-198, CU-201, CU-203, CU-204, CU-207, CU-209, CU-211, CU-213, CU-214, CU-215, CU-219, CU-221, CU-224, CU-225, CU-226, CU-229, CU-231, CU-234, CU-235, CU-238, CU-240, CU-241, CU-242, CU-243, CU-245, CU-246, CU-247, CU-248, CU-251, CU-252, CU-253, CU-254, CU-255, CU-256, CU-257, CU-258, CU-259, CU-260, CU-261, CU-262, CU-263, CU-264, CU-267, CU-268, CU-269, CU-272, CU-273, CU-274, CU-275, CU-277, CU-278, CU-279, CU-280, CU-282, CU-283, CU-284, CU-285, CU-286, CU-288, CU-289, CU-290, CU-291, CU-293, CU-294, CU-295, CU-296, CU-299, CU-300, CU-301, CU-302, CU-303, CU-305, CU-307, CU-308, CU-310, CU-311, CU-312, CU-313, CU-314, CU-316, CU-317, CU-318, CU-319, CU-320, CU-321, CU-323, CU-324, CU-326, CU-327, CU-329, CU-330, CU-331, CU-333, CU-334, CU-335, CU-336, CU-337, CU-338, CU-339, CU-340, CU-341, CU-342, CU-343, CU-344, CU-345, CU-346, CU-347 |
| **Secundario** | 55 | CU-012, CU-029, CU-030, CU-050, CU-057, CU-059, CU-062, CU-065, CU-066, CU-088, CU-094, CU-100, CU-101, CU-102, CU-156, CU-157, CU-158, CU-160, CU-162, CU-163, CU-164, CU-165, CU-170, CU-175, CU-186, CU-190, CU-193, CU-194, CU-199, CU-200, CU-202, CU-205, CU-206, CU-210, CU-212, CU-216, CU-223, CU-230, CU-239, CU-244, CU-249, CU-265, CU-270, CU-276, CU-281, CU-287, CU-297, CU-298, CU-304, CU-306, CU-315, CU-322, CU-325, CU-328, CU-348 |
| **Menor** | 2 | CU-126, CU-145 |
| **Total** | **338** | CU-001 a CU-348, sin CU-003, CU-021, CU-084, CU-090, CU-091, CU-093, CU-098, CU-099, CU-103 ni CU-153 |

### Casos de uso retirados

Los 10 casos de la tabla se retiraron del catálogo porque no son procesos de negocio elementales (un actor, un lugar, un momento, un resultado con valor propio que deja el sistema en un estado estable). Sus números quedan reservados y no se reutilizan.

| Código | Caso de uso | Retirado el | Motivo | Qué lo reemplaza |
|---|---|---|---|---|
| CU-003 | Registrar un Chofer (Gestión de Usuarios) | 15/10/2026 | Duplicaba CU-031: era la misma operación vista desde el subsistema de usuarios. | CU-031 Registrar un Chofer (Gestión de la Flota) |
| CU-021 | Recibir Notificaciones en Tiempo Real | 14/10/2026 | Es un requisito del sistema: el cliente recibe sin consultar cada cambio de su pedido y la posición del chofer. | Documento 1, NFR-02 (Rendimiento) |
| CU-084 | Verificar la Existencia de un Usuario (pre-registro) | 15/10/2026 | Es una validación del formulario de registro, no un proceso con valor propio para el actor. | CU-002 Registrarse como Cliente |
| CU-090 | Sembrar los Roles Iniciales | 15/10/2026 | Es una preparación del entorno al desplegar el sistema, no un objetivo de un usuario. | Documento 3, despliegue (arranque del sistema) |
| CU-091 | Validar Vigencia del Token de Sesión | 14/10/2026 | Es un mecanismo de autenticación que se ejecuta en cada solicitud, no un caso de uso. | Documento 1, NFR-01 (Seguridad) |
| CU-093 | Validar o Invalidar Cliente | 26/09/2026 | Los clientes se registran y compran sin aprobación previa: la marca no condicionaba ningún pedido y solo sumaba trabajo al administrador. | Sin reemplazo (los choferes siguen validándose en CU-032) |
| CU-098 | Registrar el Token de Notificaciones del Dispositivo | 15/10/2026 | Es un mecanismo del canal de avisos: la aplicación lo hace sola al iniciar sesión, sin que el usuario lo pida. | Documento 1, NFR-02 (Rendimiento) y Documento 3, diseño de notificaciones |
| CU-099 | Consultar los Tokens de un Usuario | 15/10/2026 | Es una herramienta de diagnóstico técnico del canal de avisos, no un proceso de negocio. | CU-100 Enviar una Notificación de Prueba y Documento 3 |
| CU-103 | Dar de Baja una Franja Horaria | 16/10/2026 | Duplicaba CU-343: ambos desactivan la franja (baja lógica), uno con el verbo «dar de baja» y el otro con «desactivar». | CU-343 Desactivar una Franja Horaria |
| CU-153 | Registrar Toda Operación de Escritura | 15/10/2026 | Es un requisito transversal: el sistema deja constancia de cada escritura sin que ningún actor lo pida. | Documento 1, NFR-10 (Trazabilidad y auditoría); la consulta sigue en CU-152 |

Los recuentos salen del catálogo de arriba y se verifican contra él: entre CU-001 y CU-348 hay 348 números, 338 de casos del catálogo y 10 retirados.
Los casos CU-001 a CU-051 provienen del relevamiento inicial. Los casos CU-052 a CU-104 se
incorporaron al contrastar la documentación contra el sistema construido: son
comportamientos que el sistema ya ejecuta y que el relevamiento no había registrado. Los casos CU-105 a CU-108 son los cuatro módulos inteligentes planificados (M2 a M5). Los casos CU-109 a CU-175 se incorporaron después: desglosan en casos propios las operaciones de los ABM de choferes, vehículos, clientes, direcciones y franjas horarias, y suman la funcionalidad construida y planificada del carrito, el pedido en curso, la vigencia de los envases, la flota, el consumo declarado, la compra express, los reintegros, el registro de auditoría y la configuración de los procesos automáticos. Los casos CU-251 a CU-272 parten en un caso de uso por operación los casos que agrupaban varias operaciones de un ABM (perfil, roles, puestos de trabajo, depósitos, proveedores, cajas, categorías, disponibilidad, estado y validación del chofer, productos inactivos, bloqueo y búsqueda de usuarios): el caso original conserva su número y nombra la primera operación, y la modificación y la baja incluyen a la consulta de la que parten.

---
