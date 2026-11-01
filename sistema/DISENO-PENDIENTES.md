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
| Aviso de pago rechazado o cancelado | Cuando la pasarela informa un pago rechazado o cancelado, el sistema lo registra y deja el pedido a la espera, pero no le avisa al Cliente ni libera el stock hasta que vence el plazo de pago. El aviso de pago aprobado sí está construido. | CU-048 | — | Importante |
| Estado de la documentación en el listado de empleados | El listado acepta el filtro por estado de la documentación y lo ignora: no calcula el peor vencimiento de cada persona. La ficha de documentación (CU-187) sí lo calcula. | CU-180 | — | Menor |
| Choferes por terminar su entrega en la asignación automática | La asignación automática (M1) descarta a los choferes con un pedido en curso; todavía no admite como candidatos a los que están por terminar su entrega, de modo que un chofer que entrega la última garrafa no recibe el pedido siguiente hasta quedar libre. | CU-013 | — | Importante |
| Egreso del chofer con una rendición pendiente | El egreso rechaza al chofer con pedidos en curso o con una carga de camión abierta, pero todavía no al que tiene una rendición sin aprobar: el módulo de rendiciones no registró su regla en `EmployeeRulesRegistry`. | CU-181 | — | Importante |
| Egreso de caja de lo que se paga fuera del libro | Las cargas de combustible, las multas imputadas y los pagos de compras no generan movimientos de caja ni asientos de deducción: el módulo de caja existe, pero esos casos no lo usan. El cobro que un administrador registra sobre un pedido en efectivo (`register-cash`, `resolve-unpaid`) sí entra a una caja de efectivo. | — | — | Importante |
| Marcas y rendición en la App Chofer | La API tiene la marca de inicio y de fin de la jornada, la rendición propia y las comisiones del chofer, pero la aplicación todavía no tiene las pantallas. | CU-190, CU-315, CU-232, CU-244 | — | Importante |

### 2 Parametrización pendiente

| Pendiente | Descripción | CU | Iteración | Prioridad |
|-----|-------------|----|:---------:|-----------|
| Parámetros de los módulos inteligentes | La configuración por distribuidora está construida para el despacho (CU-171), las tareas programadas (CU-173), los cuatro módulos inteligentes y la compra express (CU-172), pero los módulos M2 a M5 todavía no existen: sus parámetros se guardan y se validan, y ningún proceso los lee. | CU-172 | C-14, C-15, C-16, C-19 | Importante |

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

| Grupo | Casos de uso | Iteración | Modelo de datos construido |
|-------|--------------|:---------:|----------------------------|
| Consumo declarado y recompra | CU-145, CU-146 | C-13 | Días de aviso y próxima recompra estimada en `customer`. El consumo declarado (CU-143 y CU-144) está construido. |
| Módulos inteligentes | CU-106 (M3), CU-108 (M5), CU-107 (M4), CU-105 (M2) | C-16, C-15, C-19, C-14 | M2: `maintenance_window_proposal` y `vehicle_usage_log`. M3: `repurchase_invitation`. M4: `route_batch`, `route_batch_stop` y `route_batch_offer`. M5: `cylinder_recovery_case` y `cylinder_recovery_notice`. Los parámetros de los cuatro, en `module_config`. M1, el despacho, está construido (CU-013, CU-014). |

**Ampliaciones planificadas de casos ya construidos.** CU-116 y CU-118 (C-10) están implementados con una parte pendiente: la dirección resuelta contra el servicio de mapas. El modelo ya existe —piso, departamento, punto en PostGIS, identificador del lugar y precisión en `user_address`— y falta la consulta al servicio de mapas que lo complete. Lo mismo vale para el tiempo estimado de llegada de CU-017 (C-10). Son casos «Implementado, con funcionalidad planificada (C-10)» y no se cuentan entre los no construidos.

**Cambios de modelo planificados.** Los casos de uso planificados necesitan, además, estos cambios,
que no se tocan en la base hasta su iteración y figuran en el modelo propuesto
(`modelos/base-de-datos/SPLG-base-de-datos-propuesta.sql`): la columna `cylinder_recovery_notice.order_id`, para
atar la oferta de retiro a la entrega programada (C-15), y la columna `cylinder.decommissioned_at`, porque
el ciclo del envase no tiene un estado de baja (C-15). Cada iteración trae además sus índices en su propia migración.

**Construido el 17/10/2026.** Las iteraciones C-07, C-08, C-11, C-12, C-17, C-18 y C-20, y los casos CU-127, CU-128, CU-143 y CU-144 de C-10 y C-13,
dejaron de ser alcance pendiente: su especificación está en la tabla de implementación (§4.25) con las rutas y los códigos reales.
El reconocimiento de una moto no necesitó la columna `car.vehicle_type` prevista: se resuelve con el texto libre `car.type_car`, que contiene «moto».

---
