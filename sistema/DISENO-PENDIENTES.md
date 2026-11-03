# Pendientes de implementación

Documentación técnica del diseño del sistema. No forma parte del Documento 3 de la cátedra, que lleva sólo lo que pide su plantilla.

## Trabajo futuro

Lo que falta construir. Cada
fila indica el caso de uso al que corresponde y la iteración del plan de construcción
(Documento 0, §4) en que se resuelve. Todo caso de uso pendiente está especificado con sus cinco
artefactos —caso de uso de alto nivel, expandido, diagrama de secuencia del sistema, diagrama de
interacción de diseño y, cuando modifica datos, contrato de operación— y figura como
«Planificado» en el catálogo. Una fila con iteración «—» es una mejora de un caso ya construido que quedó diferida: no tiene iteración asignada.

### 1 Funcionalidad ausente

| Pendiente | Descripción | CU | Iteración | Prioridad |
|-----|-------------|----|:---------:|-----------|
| Liberar el stock de un pago rechazado | Cuando Mercado Pago informa un pago rechazado o cancelado, el sistema lo registra con su motivo, le avisa al Cliente (`order:payment-rejected`) y le permite reintentar el pago mientras el pedido siga vivo; el stock queda reservado hasta que vence el plazo de pago. | CU-048 | — | Menor |

### 2 Parametrización pendiente

Sin pendientes. Los parámetros por distribuidora del despacho (CU-171), las tareas programadas (CU-173), los cuatro módulos inteligentes y la compra express (CU-172) están construidos y los leen sus procesos; M3, M4 y M5 vienen apagados por omisión hasta que el administrador los enciende.

### 3 Integridad y consistencia del modelo

| Pendiente | Descripción | Prioridad |
|-----|-------------|-----------|
| Columna `isActive` en desuso en `delivery` | La habilitación administrativa (`isEnabled`) y la presencia en línea (`isAvailable`) ya son columnas separadas; ningún camino del código lee ni escribe `isActive`, que queda en su valor por omisión (`true`) desde el alta. La columna vieja sigue declarada en la entidad y en la base porque no se migró su baja. Es una deuda de limpieza de esquema, no una colisión funcional, y no corresponde a ningún caso de uso. | Menor |

### 4 Observaciones de seguridad

Sin pendientes. Las dos operaciones que figuraban en esta sección —la consulta de un usuario por
correo y la prueba del servicio de correo— exigen autenticación y rol.

---

### 5 Alcance especificado y no construido

Los casos de uso de esta tabla están documentados con sus cinco artefactos y el sistema no los realiza todavía: son los casos enteramente planificados (estado «Planificado» en el catálogo), cada uno con su iteración.
No son omisiones del relevamiento: son alcance que se especificó para que la construcción
posterior tenga contra qué hacerse. Las ampliaciones de casos ya construidos se listan después, y las mejoras diferidas sin iteración están en §10.1. El modelo de datos de cada grupo, salvo el que se aclara, **ya está construido**.
Lo que falta son los servicios, las operaciones de la API y las pantallas que usen esas tablas.

No quedan casos de uso enteramente planificados: los módulos inteligentes M2 a M5 (CU-105 a CU-108) y la recompra del cliente (CU-145 y CU-146) están construidos, en el sistema y en las aplicaciones. M3, M4 y M5 están apagados por omisión y en prueba en vivo.

**Ampliaciones planificadas de casos ya construidos.** CU-116 y CU-118 (C-10) están implementados con una parte pendiente: la dirección resuelta contra el servicio de mapas. El modelo ya existe —piso, departamento, punto en PostGIS, identificador del lugar y precisión en `user_address`— y falta la consulta al servicio de mapas que lo complete. Lo mismo vale para el tiempo estimado de llegada de CU-017 (C-10). Son casos «Implementado, con funcionalidad planificada (C-10)» y no se cuentan entre los no construidos.

**Construido el 17/10/2026.** Las iteraciones C-07, C-08, C-11, C-12, C-17, C-18 y C-20, y los casos CU-127, CU-128, CU-143 y CU-144 de C-10 y C-13,
dejaron de ser alcance pendiente: su especificación está en la tabla de implementación (§4.25) con las rutas y los códigos reales.
El reconocimiento de una moto no necesitó la columna `car.vehicle_type` prevista: se resuelve con el texto libre `car.type_car`, que contiene «moto».

---
