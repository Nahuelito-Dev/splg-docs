# Plan de Pruebas de Aceptación

**Proyecto:** SPLG — Sistema de Pedidos y Logística de Garrafas de Gas
**Metodología:** Proceso Unificado (PU)
**Iteración:** T-01 — Transición
**Versión:** 1.0
**Fecha:** 02/11/2026
**Titular de la prueba:** Nahuel Wagner

---

## 1. Propósito

Este documento define cómo se comprobará, con usuarios reales de la distribuidora, que el sistema SPLG hace lo que los casos de uso prometen. Es el artefacto «Plan de Pruebas de Aceptación» de la iteración T-01 (Documento 0.1, «Artefactos Nuevos») y la base para decidir si el sistema puede entregarse.

La prueba de aceptación no busca errores de programación, que se verifican antes con las pruebas del propio desarrollo. Busca responder una pregunta distinta: **¿una persona de la distribuidora puede hacer su trabajo con el sistema, y el sistema responde como el caso de uso lo describe?** Por eso cada caso está escrito desde la vista de quien usa el sistema —qué hace, qué ve— y su resultado esperado sale de la ficha expandida del caso de uso (Casos-de-Uso, §5) y de su estado «Implementado».

## 2. Alcance

### 2.1 Qué se prueba

- Los **21 casos de uso esenciales** de los Documentos 1, 2 y 3: CU-001, CU-002, CU-005, CU-008, CU-022, CU-013, CU-014, CU-015, CU-017, CU-078, CU-079, CU-292, CU-301, CU-048, CU-023, CU-025, CU-105, CU-106, CU-107, CU-108 y CU-152. Cada uno con su escenario principal y con el alternativo o de excepción más importante de su ficha (sección 5).
- Seis **flujos críticos de punta a punta** que atraviesan varios casos de uso y comprueban que trabajen bien juntos (sección 6): compra con efectivo, compra con MercadoPago, despacho automático y entrega con código, cobro y rendición del chofer, caja del día y procesos automáticos.

### 2.2 Qué no se prueba

| Fuera de esta prueba | Motivo |
|---|---|
| El tiempo estimado de llegada que acompaña la posición del chofer (CU-017) | Figura como funcionalidad planificada en la ficha del caso. |
| La aceptación de la invitación de recompra en la aplicación del cliente (CU-106), el lote ofrecido en la aplicación del chofer (CU-107) y las pantallas de las aplicaciones para los envases (CU-108) | Están en curso: de estos tres casos se prueban el proceso automático y el panel de administración. |
| Los casos de uso retirados del alcance (ganancias y comisiones del chofer) | El chofer cobra un sueldo mensual. |
| Las pruebas de carga, el despliegue en producción, la capacitación y los manuales | Son otras metas de la iteración T-01 con su propio artefacto. |
| Los casos de uso no esenciales que no intervienen en los flujos críticos | Se cubren con las pruebas del desarrollo. |

## 3. Responsables, usuarios de prueba y entorno

### 3.1 Responsables

| Rol | Responsable | Tarea |
|---|---|---|
| Titular del plan | Nahuel Wagner | Prepara los datos, conduce la prueba, registra los resultados y los defectos, y decide la aceptación con el distribuidor. |
| Administrador del distribuidor | Persona designada por el distribuidor | Ejecuta los casos del panel de administración y valida que puede operar sin asistencia técnica. |
| Choferes de prueba | Al menos 2 choferes reales (CHO-1 y CHO-2) | Ejecutan los casos de la aplicación del chofer. |
| Clientes de prueba | Al menos 5 clientes reales (CLI-1 a CLI-5) | Ejecutan los casos de la aplicación del cliente. |

### 3.2 Entorno y dispositivos

- **Entorno:** el servidor de producción del distribuidor, con la pasarela de MercadoPago configurada. Si el servidor todavía no está disponible, un entorno de ensayo idéntico en configuración. Las tarjetas de prueba solo sirven en el entorno de pruebas de la pasarela. En producción, el caso de pago aprobado (PA-48 y FC-02) se ejecuta con un medio de pago real por un importe mínimo que luego se reintegra, y el caso de pago rechazado (PA-49) no se ejecuta: va solo en el entorno de pruebas.
- **Dispositivos:** un teléfono por usuario de prueba, con la aplicación correspondiente instalada, GPS activo y permisos de ubicación y notificaciones concedidos; para los choferes, un teléfono real, no un simulador. El administrador usa el panel desde un navegador de escritorio.
- **Conectividad:** los dispositivos con datos móviles o Wi-Fi. Los casos que prueban un corte de conexión indican el momento exacto en que se interrumpe.
- **Reloj:** los procesos programados (rendición de las 23:30, avisos de las 08:00, reservas, ofertas) se observan en el horario real; la fecha y la hora de cada observación se anotan en la columna de resultados.

### 3.3 Datos de prueba

| Código | Qué es |
|---|---|
| CLI-1 a CLI-5 | Clientes reales con sesión iniciada y al menos una dirección de entrega dentro de la zona de cobertura. CLI-2 tiene además una dirección fuera de zona. |
| CLI-N | La persona nueva que se registra en PA-05. Su cuenta se da de baja al terminar la prueba y, mientras existe, no tiene pedidos. |
| CLI-R | Cliente dedicado a la prueba de recompra (PA-60): tiene el mínimo de pedidos entregados, la última entrega hace tiempo y ningún pedido activo. No se usa en otros casos. |
| CLI-X | Cuenta auxiliar de cliente de prueba, que el administrador bloquea solo para su caso. |
| CHO-1, CHO-2 | Choferes reales, habilitados y validados, con vehículo en uso, licencia y documentación vigentes. |
| CHO-X | Cuenta auxiliar de chofer de prueba, sin validar o sin vehículo en uso según el caso. |
| ADM | Administrador de la distribuidora. |
| PRD-10 | Garrafa de 10 kg con stock suficiente; el stock se anota antes de cada caso que lo modifica. |
| PRD-B | Producto con un stock conocido y bajo (dos unidades), para probar la falta de stock. |
| FJ-1 / FJ-2 | Una franja horaria con cupo y otra con el cupo agotado para la fecha de la prueba. |
| VEH-M | Vehículo de prueba con una tarea de mantenimiento próxima a vencer. |
| VEH-H | Vehículo en uso de CHO-2 al que el administrador le carga, solo para PA-59, una habilitación bloqueante (por ejemplo el seguro) con el vencimiento ya cumplido; al terminar se renueva. |
| PED-A, PED-B | Los dos pedidos en efectivo que CHO-2 entrega en PA-76. |

Los datos auxiliares que se modifiquen para un caso (documentación vencida, bloqueos, pedidos de prueba) se restituyen al terminar y se cierran por el circuito normal del sistema (cancelar, dar de baja), sin borrar registros.

## 4. Criterios generales de aceptación

Son los de la Fase de Transición del Documento 0.1 (iteración T-01). Al finalizar la iteración el sistema debe cumplir:

- [ ] El sistema está desplegado y funcionando en el servidor de producción del cliente.
- [ ] Al menos 2 choferes han sido capacitados y pueden operar el sistema de forma autónoma.
- [ ] El administrador del distribuidor puede gestionar el sistema sin asistencia técnica.
- [ ] Se completaron al menos 5 pedidos reales de prueba de extremo a extremo en producción.
- [ ] Los 3 manuales de usuario (cliente, chofer, administrador) están redactados y entregados.
- [ ] Los defectos críticos detectados en las pruebas beta están corregidos y verificados.
- [ ] La documentación PU completa (Doc 0 a Doc 3) está entregada a la cátedra.

Este plan aporta la evidencia de cuatro de ellos: los pedidos de extremo a extremo (flujos FC-01 y FC-02: el flujo principal de FC-01 se ejecuta tres veces, con CLI-1, CLI-2 y CLI-3, y con CHO-1, CHO-2 y CHO-1; el de FC-02, dos veces, con CLI-4 y CLI-5 y con CHO-2 y CHO-1; son los cinco pedidos reales de extremo a extremo, con los cinco clientes y los dos choferes), la autonomía de los choferes (casos de CHO-1 y CHO-2), la del administrador (casos de ADM) y la corrección de los defectos críticos (sección 8). Los demás se verifican con sus propios artefactos.

## 5. Casos de prueba por caso de uso esencial

La última columna se completa en la prueba real con uno de estos resultados: **Aprobado**, **Aprobado con observaciones** o **Rechazado** (con el número de defecto), junto con la fecha y quien lo ejecutó. Los casos de cada tabla se ejecutan en el orden en que figuran.

### 5.1 CU-001 — Iniciar Sesión

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-01 | CU-001<br>*Principal* | Cliente, Chofer, Administrador | Los tres usuarios están registrados y no están bloqueados. | 1) Abrir la aplicación del cliente, ingresar correo y contraseña correctos y confirmar.<br>2) Repetir en la aplicación del chofer con CHO-1.<br>3) Repetir en el panel de administración con ADM. | CLI-1, CHO-1, ADM | En cada aplicación el usuario queda operando con las funciones de su rol. Cada ingreso se completa en pocos segundos (cota de 3 segundos para la verificación de identidad). El panel mantiene la sesión abierta durante una hora. |  |
| PA-02 | CU-001<br>*Excepción: credenciales incorrectas* | Cliente | El usuario está registrado. | 1) Ingresar un correo existente con una contraseña equivocada.<br>2) Ingresar un correo que no existe. | CLI-1 con contraseña errónea; correo inexistente | La aplicación informa el error y no abre la sesión en ninguno de los dos casos. |  |
| PA-03 | CU-001<br>*Excepción: rol que no corresponde* | Cliente | CLI-1 está registrado como cliente. | 1) Intentar ingresar con CLI-1 en la aplicación del chofer.<br>2) Intentar ingresar con CLI-1 en el panel de administración. | CLI-1 | La aplicación del chofer no abre la sesión. El panel informa «No tenés permisos de administrador». |  |
| PA-04 | CU-001<br>*Excepción: cuenta bloqueada* | Cliente | La cuenta de prueba CLI-X fue bloqueada por el administrador. | 1) Ingresar con CLI-X en la aplicación del cliente. | CLI-X (cuenta auxiliar de prueba, bloqueada para este caso) | El sistema deniega el ingreso e informa «La cuenta está bloqueada. Comuníquese con la distribuidora.» |  |

### 5.2 CU-002 — Registrarse como Cliente

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-05 | CU-002<br>*Principal* | Cliente (persona nueva) | La persona tiene conexión a internet y no tiene cuenta con ese correo ni con ese teléfono. | 1) Elegir «Registrarse» en la aplicación del cliente.<br>2) Completar nombre completo, correo, teléfono en formato internacional y una contraseña de al menos seis caracteres.<br>3) Confirmar el registro.<br>4) Revisar la bandeja de correo.<br>5) Iniciar sesión con los datos recién cargados. | Datos de una persona nueva (CLI-N); la cuenta se da de baja al terminar la prueba | El sistema informa que la cuenta fue creada, con rol de cliente, y no abre la sesión. Llega el correo de bienvenida. El inicio de sesión posterior funciona (la respuesta del registro se da en menos de 5 segundos). |  |
| PA-06 | CU-002<br>*Excepción: correo o teléfono ya registrados* | Cliente (persona nueva) | Existe una cuenta con ese correo o con ese teléfono. | 1) Intentar registrarse con el correo de CLI-1.<br>2) Intentar registrarse con el teléfono de CLI-1 y un correo nuevo. | CLI-1 (correo y teléfono existentes) | El sistema informa «Email o teléfono ya en uso» e invita a iniciar sesión. La cuenta existente no se modifica y no se crea ninguna cuenta nueva. |  |
| PA-07 | CU-002<br>*Excepción: datos inválidos* | Cliente (persona nueva) | Ninguna. | 1) Intentar registrarse con una contraseña de cinco caracteres.<br>2) Intentar registrarse con un correo sin formato de correo.<br>3) Intentar registrarse con un teléfono sin formato internacional. | Datos inválidos de una persona de prueba | El registro se rechaza en cada caso e indica el campo con el problema. No queda ninguna cuenta a medias. |  |

### 5.3 CU-005 — Crear un Pedido

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-08 | CU-005<br>*Principal: pago en efectivo* | Cliente | CLI-1 inició sesión, tiene una dirección dentro de la zona de cobertura y existe stock del producto. | 1) Consultar el catálogo y sumar al carrito dos unidades de PRD-10.<br>2) Elegir la dirección de entrega.<br>3) Elegir pago en efectivo y revisar el resumen.<br>4) Confirmar el pedido.<br>5) Abrir el seguimiento del pedido. | CLI-1, PRD-10 x 2, pago en efectivo | El resumen muestra ítems, descuentos, subtotal y total, sin recargo por el medio de pago. Al confirmar, el pedido queda pendiente, el carrito queda vacío, el stock de PRD-10 baja en dos unidades y el pedido se ofrece a un chofer. El cliente recibe el aviso de que el pedido fue creado (el alta se resuelve en menos de 5 segundos). |  |
| PA-09 | CU-005<br>*Alternativo: pago con MercadoPago* | Cliente | Ídem anterior. | 1) Armar el carrito con una unidad de PRD-10.<br>2) Elegir MercadoPago como medio de pago y revisar el resumen.<br>3) Confirmar el pedido. | CLI-1, PRD-10 x 1, MercadoPago | El total incluye un recargo del 10 % respecto del pago en efectivo. El pedido queda creado con un enlace para completar el cobro y no se ofrece a ningún chofer hasta que el pago se confirme. |  |
| PA-10 | CU-005<br>*Excepción: stock insuficiente* | Cliente | El producto PRD-B tiene un stock conocido de dos unidades. | 1) Sumar tres unidades de PRD-B al carrito.<br>2) Confirmar el pedido. | CLI-1, PRD-B x 3 (stock 2) | El sistema informa «Stock insuficiente para» ese producto. El pedido no se crea y el stock no cambia. |  |
| PA-11 | CU-005<br>*Excepción: dirección fuera de cobertura* | Cliente | La distribuidora tiene zonas de cobertura definidas. CLI-2 tiene una dirección fuera de todas ellas. | 1) Armar un pedido con PRD-10 y elegir la dirección fuera de zona.<br>2) Confirmar el pedido. | CLI-2 con dirección fuera de zona | El sistema rechaza el pedido antes de tocar el stock, que no cambia. No queda ningún pedido nuevo. |  |
| PA-12 | CU-005<br>*Alternativo: entrega agendada en una franja* | Cliente | FJ-1 es una franja activa con cupo para una fecha futura. | 1) Armar un pedido con PRD-10.<br>2) Elegir fecha futura y la franja FJ-1.<br>3) Confirmar el pedido. | CLI-3, PRD-10 x 1, FJ-1 | El pedido se crea con la fecha y la franja elegidas y el cupo de la franja disminuye en uno. |  |
| PA-13 | CU-005<br>*Excepción: franja sin cupo o fecha pasada* | Cliente | FJ-2 es una franja activa con el cupo agotado para la fecha elegida. | 1) Armar un pedido con PRD-10 y elegir la franja FJ-2 para esa fecha.<br>2) Confirmar.<br>3) Repetir con una fecha anterior a hoy. | CLI-3, PRD-10 x 1, FJ-2 | En el primer caso el sistema rechaza el pedido por falta de cupo. En el segundo informa que la fecha agendada no puede ser pasada. En ambos el stock no cambia. |  |
| PA-14 | CU-005<br>*Alternativo: pedido telefónico cargado por el administrador* | Administrador | ADM inició sesión en el panel. CLI-4 tiene una dirección registrada. | 1) Crear un pedido nuevo desde el panel indicando a nombre de qué cliente es.<br>2) Agregar PRD-10 x 1 y elegir la dirección de CLI-4.<br>3) Elegir pago en efectivo y confirmar. | ADM, CLI-4, PRD-10 x 1 | El pedido queda pendiente a nombre de CLI-4 y se ofrece a un chofer. |  |

### 5.4 CU-008 — Cancelar un Pedido (Cliente)

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-15 | CU-008<br>*Principal* | Cliente | CLI-1 tiene un pedido propio pendiente o aceptado (no en camino). Se anota el stock de PRD-10 antes de cancelar. | 1) Abrir el detalle del pedido y elegir cancelarlo.<br>2) Escribir el motivo de la cancelación.<br>3) Confirmar. | CLI-1, pedido pendiente de PRD-10 x 2 | El pedido pasa a cancelado con su motivo. El stock de PRD-10 recupera las dos unidades. El cliente recibe el aviso y el panel muestra el cambio. Si había chofer asignado, su aplicación le avisa que ya no hace falta ir. |  |
| PA-16 | CU-008<br>*Excepción: motivo faltante* | Cliente | Ídem anterior, con otro pedido pendiente. | 1) Elegir cancelar el pedido y confirmar sin escribir el motivo.<br>2) Repetir escribiendo solo espacios. | CLI-1 | La aplicación pide el motivo y el sistema rechaza la cancelación. El pedido sigue pendiente y el stock no cambia. |  |
| PA-17 | CU-008<br>*Excepción: pedido en camino o ya finalizado* | Cliente | CLI-1 tiene un pedido en camino y otro entregado. | 1) Intentar cancelar el pedido en camino.<br>2) Intentar cancelar el pedido entregado. | CLI-1 | Para el pedido en camino el sistema informa «El pedido ya está en camino. Contacte al soporte.». Para el entregado informa «No se puede cancelar un pedido finalizado». Ninguno cambia de estado. |  |

### 5.5 CU-022 — Activar la Disponibilidad

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-18 | CU-022<br>*Principal* | Chofer | CHO-1 está habilitado y validado, tiene un vehículo en uso y GPS activo. | 1) Abrir la aplicación del chofer y encender la disponibilidad desde la pantalla principal.<br>2) Esperar a que la aplicación informe la primera posición. | CHO-1 | La aplicación muestra al chofer como disponible. Empieza a recibir ofertas recién cuando la aplicación informa su primera posición. La activación responde en alrededor de 1 segundo. |  |
| PA-19 | CU-022<br>*Excepción: chofer sin validar o deshabilitado* | Chofer | La cuenta auxiliar CHO-X está sin validar (o deshabilitada) por el administrador. | 1) Ingresar con CHO-X en la aplicación del chofer.<br>2) Intentar encender la disponibilidad. | CHO-X (cuenta auxiliar de chofer sin validar) | El sistema deniega la operación y la disponibilidad no cambia. Mientras tanto, CHO-X no recibe ofertas. |  |
| PA-20 | CU-266 — Desactivar la Disponibilidad<br>*Complementario: apagar la disponibilidad* | Chofer | CHO-1 está disponible. | 1) Apagar la disponibilidad desde la pantalla principal.<br>2) Crear un pedido nuevo con CLI-1 cerca de CHO-1. | CHO-1, CLI-1 | La aplicación muestra al chofer como no disponible y CHO-1 no recibe la oferta del pedido nuevo. |  |

### 5.6 CU-013 — Asignar un Pedido Automáticamente por Proximidad

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-21 | CU-013<br>*Principal* | Sistema Automático (observan CLI-1 y CHO-1 / CHO-2) | CHO-1 y CHO-2 están disponibles, en línea y con su posición informada; CHO-1 está más cerca del domicilio que CHO-2. | 1) Crear un pedido en efectivo con CLI-1.<br>2) Observar la aplicación de ambos choferes. | CLI-1, CHO-1 (más cercano), CHO-2 | Solo CHO-1 recibe la oferta, con el detalle del pedido y la hora en que pierde vigencia (30 segundos por omisión), y una notificación en el dispositivo. CHO-2 no recibe nada. El pedido sigue pendiente. |  |
| PA-22 | CU-013<br>*Excepción: sin choferes elegibles* | Sistema Automático (observa ADM) | Ningún chofer está disponible y en línea. | 1) Poner a todos los choferes fuera de línea.<br>2) Crear un pedido en efectivo con CLI-1.<br>3) Observar el panel de administración. | CLI-1, ADM | No se emite ninguna oferta. El pedido queda pendiente y el administrador recibe un aviso de que no hay choferes elegibles en el radio. El aviso se emite una sola vez. |  |
| PA-23 | CU-013<br>*Excepción: chofer con documentación vencida* | Sistema Automático | La licencia de CHO-1 o la documentación de su vehículo tiene el vencimiento cumplido (el administrador modifica la fecha para este caso y la restituye al finalizar). CHO-2 está habilitado y más lejos. | 1) Crear un pedido en efectivo con CLI-1. | CLI-1, CHO-1 con documentación vencida, CHO-2 | CHO-1 queda descartado aunque esté más cerca y la oferta va a CHO-2. |  |

### 5.7 CU-014 — Vencer la Oferta y Ofrecer al Siguiente Chofer

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-24 | CU-014<br>*Principal: la oferta vence* | Sistema Automático | CHO-1 y CHO-2 están disponibles; CHO-1 está más cerca. | 1) Crear un pedido en efectivo con CLI-1.<br>2) Dejar vencer la oferta en CHO-1 sin responder (más de 30 segundos).<br>3) Observar la aplicación de CHO-2. | CLI-1, CHO-1, CHO-2 | Pasada la ventana de aceptación, la oferta de CHO-1 se da por vencida y, en el siguiente ciclo de revisión (cada 15 segundos), CHO-2 recibe la oferta. El pedido sigue pendiente. CHO-1 no vuelve a recibir ese pedido. |  |
| PA-25 | CU-014<br>*Alternativo: pedido pendiente sin oferta* | Sistema Automático | No hay choferes disponibles. Hay un pedido pendiente con más de un minuto de antigüedad. | 1) Crear un pedido en efectivo con CLI-1 sin choferes disponibles.<br>2) Esperar más de un minuto.<br>3) Poner a CHO-1 disponible y en línea. | CLI-1, CHO-1 | Sin intervención de nadie, el pedido pendiente vuelve a entrar al circuito y CHO-1 recibe la oferta. |  |
| PA-26 | CU-014<br>*Excepción: el pedido fue aceptado o cancelado mientras corría la oferta* | Sistema Automático | Hay una oferta vigente a CHO-1. | 1) Cancelar el pedido desde la aplicación del cliente antes de que la oferta venza.<br>2) Esperar a que pase el ciclo de revisión. | CLI-1, CHO-1, CHO-2 | El pedido cancelado no se ofrece a CHO-2. No aparece ninguna oferta nueva. |  |

### 5.8 CU-015 — Aceptar un Pedido

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-27 | CU-015<br>*Principal* | Chofer | CHO-1 tiene una oferta vigente de un pedido en efectivo de CLI-1. CHO-1 está habilitado, validado y con vehículo en uso. | 1) En la aplicación del chofer, abrir la oferta y elegir «Aceptar».<br>2) En la aplicación del cliente, revisar el seguimiento del pedido. | CLI-1, CHO-1 | El pedido pasa a aceptado y queda asignado a CHO-1 con un código de entrega de seis dígitos. El cliente recibe el aviso con el nombre y el teléfono del chofer. Cualquier oferta abierta a otro chofer se retira y esos choferes reciben el aviso de que ya no está vigente. |  |
| PA-28 | CU-015<br>*Excepción: el pedido ya fue tomado por otro chofer* | Chofer, Administrador | CHO-2 recibió la oferta de un pedido y la mantiene abierta en pantalla, sin responder. Antes de que venza, el administrador asigna el pedido a CHO-1 desde el panel. | 1) CHO-2 recibe la oferta y la deja abierta.<br>2) El administrador asigna el pedido a CHO-1 desde el panel.<br>3) En la aplicación de CHO-2, que sigue con la oferta en pantalla, elegir «Aceptar». | CHO-1, CHO-2, ADM | El sistema rechaza la aceptación e informa que el pedido no está asignado a su usuario. CHO-1 conserva el pedido. |  |
| PA-29 | CU-015<br>*Excepción: chofer sin vehículo en uso* | Chofer | La cuenta auxiliar CHO-X está disponible, en línea y es la más cercana, pero no tiene vehículo en uso. CHO-2 está disponible y más lejos. | 1) CLI-1 confirma un pedido en efectivo.<br>2) Observar las aplicaciones de CHO-X y de CHO-2. | CHO-X, CHO-2, CLI-1 | CHO-X no recibe la oferta, por lo que no puede aceptar el pedido. La oferta va a CHO-2 y el pedido sigue pendiente hasta que alguien lo acepte. |  |
| PA-30 | CU-015<br>*Excepción: chofer sin carga de camión abierta* | Chofer | La distribuidora tiene activada la exigencia de carga de camión abierta (el administrador la activa en la configuración para este caso y la restituye al terminar). CHO-1 no tiene carga abierta y es el más cercano; CHO-2 tiene su carga abierta. | 1) CLI-1 confirma un pedido en efectivo.<br>2) Observar las aplicaciones de CHO-1 y de CHO-2. | CHO-1 sin carga abierta, CHO-2 con carga abierta, CLI-1 | CHO-1 no recibe la oferta porque no puede recibir pedidos sin una carga de camión abierta. La oferta va a CHO-2. |  |

### 5.9 CU-017 — Modificar la Ubicación GPS del Chofer

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-31 | CU-017<br>*Principal: pedido en curso* | Chofer | El pedido de CLI-1 está en camino con CHO-1. El dispositivo tiene GPS y permisos de ubicación. | 1) CHO-1 se desplaza al menos diez metros con la aplicación abierta.<br>2) En la aplicación del cliente, mirar el mapa de seguimiento.<br>3) En el panel de administración, mirar el seguimiento del pedido. | CLI-1, CHO-1 con dispositivo en movimiento | El mapa del cliente y el del panel muestran la posición actualizada de CHO-1 a medida que se mueve. (El tiempo estimado de llegada está planificado y no forma parte de esta prueba.) |  |
| PA-32 | CU-017<br>*Alternativo: sin pedido en curso* | Chofer | CHO-1 está disponible y no tiene pedido en curso. | 1) CHO-1 se desplaza con la aplicación abierta.<br>2) Crear un pedido de CLI-1 cerca de la nueva posición. | CLI-1, CHO-1 | La posición no se muestra a ningún cliente, pero el despacho encuentra a CHO-1 en su nueva ubicación y le ofrece el pedido. |  |
| PA-33 | CU-017<br>*Excepción: se corta la conexión* | Chofer | CHO-1 tiene la aplicación abierta y en movimiento. | 1) Desactivar la conexión de datos del dispositivo unos segundos.<br>2) Volver a activarla y seguir en movimiento. | CHO-1 | La aplicación reintenta la conexión por sí sola y las posiciones vuelven a registrarse sin necesidad de reiniciarla. |  |

### 5.10 CU-078 — Consultar el Código de Entrega (QR del chofer)

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-34 | CU-078<br>*Principal* | Chofer | CHO-1 aceptó el pedido de CLI-1 y lo marcó como en camino. | 1) Abrir el detalle del pedido en la aplicación del chofer y pedir el QR de entrega. | CHO-1, CLI-1 | La aplicación muestra el código como QR y, debajo, el mismo número de seis dígitos, grande y agrupado de a tres (por ejemplo «482 913»). Consultarlo no cambia el pedido. |  |
| PA-35 | CU-078<br>*Alternativo: generar un código nuevo* | Chofer | El pedido está en camino con CHO-1. | 1) Elegir «Generar código nuevo» y confirmar.<br>2) Intentar confirmar la entrega desde la aplicación del cliente con el código anterior. | CHO-1, CLI-1 | La aplicación del chofer muestra el código nuevo al instante. Con el código anterior, el sistema informa «Código de entrega inválido»: dejó de valer. |  |
| PA-36 | CU-078<br>*Excepción: pedido sin aceptar o ajeno* | Chofer / Cliente | Hay un pedido pendiente que CHO-1 todavía no aceptó. | 1) Con CHO-1, intentar pedir el QR de un pedido que todavía no aceptó.<br>2) Con CLI-1, buscar en su aplicación el código de entrega de su pedido. | CHO-1, CLI-1 | El pedido sin aceptar informa que todavía no tiene código de entrega (debe estar aceptado). El cliente no puede conocer el código por el sistema: solo lo ve escaneando el QR del chofer. |  |

### 5.11 CU-079 — Confirmar una Entrega Escaneando el QR (cliente)

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-37 | CU-079<br>*Principal: escaneo del QR* | Cliente | El pedido de CLI-1 está en camino y CHO-1 está en el domicilio mostrando el QR. | 1) CHO-1 elige «Llegué» y muestra el QR.<br>2) CLI-1 escanea el QR con su aplicación. | CLI-1, CHO-1 | El pedido pasa a entregado. Si el pago era en efectivo, el pago sigue pendiente. El cliente y el panel reciben el nuevo estado, el chofer deja de aparecer en el seguimiento en vivo y los envases del pedido figuran con el cliente (la confirmación responde en menos de 3 segundos). |  |
| PA-38 | CU-079<br>*Alternativo: código escrito a mano* | Cliente | Ídem, pero el dispositivo del cliente no puede escanear. | 1) CHO-1 dicta los seis dígitos.<br>2) CLI-1 los escribe con el teclado numérico y confirma. | CLI-2, CHO-1 | El pedido pasa a entregado, igual que con el escaneo. |  |
| PA-39 | CU-079<br>*Excepción: código incorrecto y bloqueo* | Cliente | El pedido está en camino y tiene código. | 1) Ingresar un código incorrecto una vez.<br>2) Ingresar cuatro códigos incorrectos más hasta llegar a cinco.<br>3) Ingresar entonces el código correcto.<br>4) CHO-1 genera un código nuevo e CLI-3 lo ingresa. | CLI-3, CHO-1 | Cada código incorrecto informa «Código de entrega inválido» y suma un intento (el aviso de código mal leído, si el código no tiene seis dígitos, es distinto). Al quinto, el pedido queda bloqueado: aun con el código correcto el sistema informa «Demasiados intentos: pedile al chofer un código nuevo». Con el código nuevo la entrega se confirma. |  |
| PA-40 | CU-079<br>*Alternativo: confirmación asistida por el administrador* | Administrador | El pedido está en camino y el cliente no puede confirmar. | 1) El chofer muestra el código de entrega al administrador.<br>2) En el panel, el administrador ingresa el código y un motivo de al menos 10 caracteres, y confirma la entrega.<br>3) Repetir con el código correcto y un motivo de tres caracteres en otro pedido en camino. | ADM, CHO-1, pedidos en camino de CLI-4 | Con código y motivo válidos el pedido pasa a entregado y el motivo queda en el historial del pedido y en la auditoría. Con el motivo corto el sistema rechaza la operación y el pedido sigue en camino. |  |
| PA-41 | CU-079<br>*Excepción: pedido que no está en camino* | Cliente | CLI-1 tiene un pedido aceptado que todavía no está en camino. | 1) Intentar confirmar la entrega con un código cualquiera. | CLI-1 | El sistema informa «El pedido no está en camino, no se puede confirmar la entrega» y no cambia el estado. |  |

### 5.12 CU-292 — Confirmar el Cobro en Efectivo

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-42 | CU-292<br>*Principal* | Chofer | El pedido en efectivo de CLI-1 está entregado y el cobro figura pendiente. CHO-1 es el chofer asignado. | 1) CHO-1 cobra el efectivo al cliente.<br>2) En su aplicación, abre el pedido y elige «Pago recibido». | CHO-1, CLI-1 | El pago del pedido pasa a pagado y queda registrado el momento y el chofer que lo confirmó. El pedido sigue entregado. |  |
| PA-43 | CU-292<br>*Alternativo: confirmación repetida* | Chofer | El cobro del pedido de PA-42 ya fue confirmado. | 1) CHO-1 vuelve a abrir el pedido y elige otra vez «Pago recibido». | CHO-1, CLI-1 | No hay error: el sistema muestra el pedido tal cual, con el pago pagado y el momento y el chofer de la primera confirmación, sin cambios. |  |
| PA-44 | CU-292<br>*Excepción: pedido no entregado o no pagado en efectivo* | Chofer | CHO-1 tiene un pedido en camino y otro entregado pagado por MercadoPago. | 1) Intentar confirmar el cobro del pedido en camino.<br>2) Intentar confirmarlo en el pedido de MercadoPago. | CHO-1 | El sistema rechaza ambas operaciones y no cambia el estado de los pagos. |  |

### 5.13 CU-301 — Confirmar una Transferencia

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-45 | CU-301<br>*Principal: transferencia recibida* | Administrador | Existe un pedido de CLI-3 pagado por transferencia, con el pago pendiente. | 1) Abrir el pedido en el panel y elegir confirmar la transferencia.<br>2) Escribir un motivo de entre 10 y 500 caracteres y confirmar. | ADM, CLI-3 | El pago pasa a pagado y queda registrado quién lo resolvió, cuándo y con qué motivo. El historial del pedido muestra la nota con el motivo y la venta pasa a sumar en los reportes. |  |
| PA-46 | CU-301<br>*Alternativo: transferencia no recibida* | Administrador | Existe un pedido entregado de CLI-4 pagado por transferencia, con el pago pendiente. | 1) Elegir «marcar como no recibida» con un motivo válido y confirmar. | ADM, CLI-4 | El pago pasa a fallido, con el motivo en el historial. La venta no suma. |  |
| PA-47 | CU-301<br>*Excepción: motivo inválido o pedido no entregado* | Administrador | Existe un pedido de transferencia todavía no entregado. | 1) Intentar confirmar con un motivo de cinco caracteres.<br>2) Intentar marcarlo como no recibido con un motivo válido. | ADM, pedido de transferencia sin entregar | El primer intento se rechaza por motivo inválido. El segundo se rechaza porque el pedido no fue entregado. El pago sigue pendiente. |  |

### 5.14 CU-048 — Procesar el Pago con MercadoPago

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-48 | CU-048<br>*Principal: pago aprobado* | MercadoPago (observa el cliente) | El pedido de CLI-1 está pagado con MercadoPago y el cobro figura pendiente. La cuenta de MercadoPago usada es la de prueba o la del distribuidor, según el entorno. | 1) Abrir el enlace de cobro y completar el pago (en el entorno de pruebas de la pasarela, con una tarjeta de prueba aprobada; en producción, con un medio de pago real de bajo monto, que luego se reintegra).<br>2) Esperar el aviso en la aplicación del cliente.<br>3) Observar la aplicación de los choferes. | CLI-1; medio de pago de prueba o de bajo monto según el entorno | El pedido figura como pagado y el cliente recibe el aviso de que su pago fue aprobado, una sola vez. Recién entonces el pedido se ofrece a un chofer. El pago queda registrado con el estado aprobado. |  |
| PA-49 | CU-048<br>*Alternativo: pago rechazado o abandonado* | MercadoPago (observa el cliente) | Solo en el entorno de pruebas de la pasarela: en producción este caso no se ejecuta con medios de pago reales. Hay otro pedido de CLI-2 con cobro pendiente. | 1) Intentar pagar con una tarjeta de prueba rechazada, o cerrar la pantalla de cobro sin pagar.<br>2) Observar el estado del pedido y la aplicación de los choferes. | CLI-2, tarjeta de prueba rechazada | El pedido no figura como pagado y no se ofrece a ningún chofer. El enlace de cobro sigue disponible para reintentar. |  |
| PA-50 | CU-048<br>*Alternativo: el pago queda registrado una sola vez* | Administrador (verifica en el panel) | El pedido de PA-48 ya tiene su pago aprobado y fue ofrecido a un chofer. La pasarela puede avisar más de una vez el mismo pago; la ficha garantiza que los avisos repetidos no producen efectos nuevos. | 1) En el panel, abrir el pedido y revisar el estado del pago y el historial.<br>2) En la aplicación del cliente, revisar los avisos recibidos.<br>3) En la aplicación de los choferes, revisar las ofertas de ese pedido. | ADM, pedido de CLI-1 ya pagado | El pedido figura pagado una sola vez, con un único identificador de pago. El cliente recibió un solo aviso de pago aprobado y existe una sola oferta abierta del pedido a los choferes. |  |

### 5.15 CU-023 — Registrar un Reclamo

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-51 | CU-023<br>*Principal* | Cliente | CLI-1 tiene un pedido propio que aún no fue entregado (pendiente, aceptado o en camino), por ejemplo uno creado para este caso. | 1) Abrir el historial de pedidos y elegir el pedido.<br>2) Elegir registrar un reclamo, escribir el motivo y una descripción.<br>3) Adjuntar una foto y confirmar el envío. | CLI-1, una foto de prueba | El reclamo queda registrado como pendiente, asociado al pedido y a la distribuidora del pedido. El administrador lo encuentra en el listado de reclamos del panel. |  |
| PA-52 | CU-023<br>*Alternativo: reclamo cargado por el administrador* | Administrador | El pedido pertenece a CLI-2 y a la distribuidora de ADM. | 1) En el panel, registrar un reclamo a nombre de CLI-2 sobre ese pedido. | ADM, CLI-2 | El reclamo queda pendiente a nombre del cliente indicado. |  |
| PA-53 | CU-023<br>*Excepción: pedido que no es del cliente indicado* | Administrador | El pedido pertenece a CLI-2. | 1) En el panel, registrar un reclamo sobre ese pedido a nombre de CLI-3. | ADM, CLI-2, CLI-3 | El sistema informa «Esta orden no pertenece al cliente indicado» y no crea el reclamo. |  |

### 5.16 CU-025 — Resolver un Reclamo

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-54 | CU-025<br>*Principal* | Administrador | Existe un reclamo pendiente o en proceso de la distribuidora de ADM. | 1) Abrir el detalle del reclamo y leer el motivo, la descripción y la foto.<br>2) Elegir el estado «resuelto», escribir la nota de resolución y confirmar. | ADM, reclamo de CLI-1 | El reclamo queda resuelto con su nota de resolución visible en el panel. |  |
| PA-55 | CU-025<br>*Alternativo: rechazar el reclamo* | Administrador | Existe otro reclamo pendiente. | 1) Elegir el estado «rechazado», escribir la nota y confirmar. | ADM, reclamo de CLI-2 | El reclamo queda rechazado con su nota. |  |
| PA-56 | CU-025<br>*Excepción: sin nota o ya cerrado* | Administrador | Existe un reclamo pendiente y otro ya resuelto. | 1) Intentar resolver el reclamo pendiente sin escribir la nota.<br>2) Intentar cambiar el estado del reclamo ya resuelto. | ADM | La resolución sin nota se rechaza por dato obligatorio. El cambio sobre el reclamo ya resuelto se rechaza con el detalle de la transición inválida y la nota anterior no se pisa. |  |

### 5.17 CU-105 — Planificar el Mantenimiento y las Habilitaciones de la Flota

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-57 | CU-105<br>*Principal: negociación de la ventana de taller* | Sistema Automático; Chofer; Administrador | Un vehículo con chofer asignado tiene una tarea de mantenimiento o una habilitación que vence dentro de la ventana de anticipación configurada. | 1) Esperar la corrida diaria del proceso (o a la hora configurada).<br>2) El chofer recibe la propuesta de ventana de taller por notificación y por correo y la acepta.<br>3) El administrador revisa la tarea pendiente en el panel y confirma la ventana. | VEH-M (vehículo de prueba con tarea próxima a vencer), CHO-1, ADM | El chofer recibe una sola propuesta con su vigencia. Al aceptarla, la tarea queda pendiente de confirmación del administrador y, cuando éste confirma, queda programada y la agenda del vehículo se bloquea para esa fecha. |  |
| PA-58 | CU-105<br>*Alternativo: el chofer rechaza o no responde* | Sistema Automático; Chofer; Administrador | Igual que el caso principal. | 1) El chofer rechaza la propuesta, o la deja vencer.<br>2) Repetir hasta agotar las alternativas. | VEH-M, CHO-1, ADM | El sistema ofrece la ventana siguiente. Agotadas las alternativas, el caso se escala al administrador con el cuadro de ventanas evaluadas y el motivo de descarte de cada una; el sistema no contrata nada por su cuenta. |  |
| PA-59 | CU-105<br>*Excepción: habilitación bloqueante vencida* | Sistema Automático | VEH-H, el vehículo en uso de CHO-2, tiene una habilitación bloqueante con el vencimiento cumplido (por ejemplo, el seguro del vehículo: el administrador carga una fecha pasada para este caso). | 1) Esperar la corrida del proceso.<br>2) Crear un pedido en efectivo con CLI-1 cerca de CHO-2.<br>3) Para dejar todo como estaba, el administrador carga en el panel el nuevo vencimiento de la habilitación de VEH-H y verifica que el vehículo vuelve a figurar en servicio.<br>4) Crear otro pedido en efectivo con CLI-1 cerca de CHO-2. | CHO-2, VEH-H, CLI-1, ADM | El vehículo queda fuera de servicio y CHO-2 no recibe la oferta del primer pedido. Con la habilitación renovada, el vehículo vuelve a servicio y CHO-2 recibe la oferta del segundo pedido. |  |

### 5.18 CU-106 — Anticipar la Recompra por Consumo Estimado

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-60 | CU-106<br>*Principal: invitación a reponer* | Sistema Automático (se verifica desde el panel) | El proceso de recompra está habilitado en los parámetros de la distribuidora (viene apagado). CLI-R, cliente dedicado a este caso, tiene el mínimo configurado de pedidos entregados, la última entrega hace tiempo, ningún pedido activo ni invitación reciente, y su fecha estimada de agotamiento cae dentro de la ventana de anticipación. | 1) Esperar la corrida diaria del proceso.<br>2) En el panel de administración, consultar las invitaciones de recompra emitidas. | CLI-R | Existe una invitación vigente para CLI-R, con el pedido armado según su historial, su última dirección y su vencimiento. El cliente tiene como máximo una invitación vigente y el sistema no crea ningún pedido hasta que él acepte. |  |
| PA-61 | CU-106<br>*Excepción: cliente que no corresponde invitar* | Sistema Automático (se verifica desde el panel) | El proceso de recompra está habilitado en los parámetros de la distribuidora. CLI-1 tiene un pedido activo sin entregar; CLI-N (la cuenta nueva de PA-05) no tiene pedidos entregados. | 1) Esperar la corrida del proceso.<br>2) Consultar las invitaciones en el panel. | CLI-1, CLI-N | Ni CLI-1 ni CLI-N reciben invitación. |  |

### 5.19 CU-107 — Agrupar Pedidos por Recorrido

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-62 | CU-107<br>*Principal: lote ofrecido a un chofer* | Sistema Automático (se verifica desde el panel) | El proceso de agrupación está habilitado en los parámetros de la distribuidora (viene apagado). No hay choferes disponibles al crear los pedidos; hay al menos dos pedidos programados con franja futura, sin chofer, cercanos entre sí y con franjas compatibles. | 1) Con los choferes fuera de línea, crear dos pedidos programados cercanos entre sí en la misma franja (CLI-1 y CLI-3).<br>2) Poner a CHO-1 disponible y en línea, con capacidad de carga.<br>3) Esperar la corrida del proceso.<br>4) En el panel, consultar los lotes armados. | CLI-1, CLI-3, FJ-1, CHO-1 | El panel muestra un lote con las dos paradas ordenadas, el peso total y el chofer al que se ofreció. Ninguna parada queda fuera de la franja que eligió el cliente. |  |
| PA-63 | CU-107<br>*Alternativo: sin pedidos para agrupar* | Sistema Automático (se verifica desde el panel) | El proceso de agrupación está habilitado. Hay un solo pedido programado. | 1) Esperar la corrida del proceso. | CLI-1 | No se arma ningún lote y el pedido sigue su circuito individual. |  |

### 5.20 CU-108 — Recuperar Envases No Devueltos

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-64 | CU-108<br>*Principal* | Sistema Automático; Administrador (se verifica desde el panel) | El proceso de recuperación de envases está habilitado en los parámetros de la distribuidora (viene apagado). Existe un envase en poder de CLI-2 con una antigüedad mayor al plazo de tolerancia de devolución. | 1) Esperar la corrida del proceso.<br>2) En el panel, consultar los casos de recupero de envases. | CLI-2, envase retenido | Se abre un caso de recupero para el envase de CLI-2 con el importe del depósito comprometido y se envía el recordatorio de devolución. Ningún depósito se cobra por cuenta del sistema. |  |
| PA-65 | CU-108<br>*Alternativo: el envase vuelve durante la gestión* | Sistema Automático; Administrador | Existe un caso de recupero abierto (PA-64). | 1) En el panel, registrar la devolución del envase.<br>2) Esperar la corrida siguiente.<br>3) En el panel, consultar el caso de recupero. | CLI-2, envase retenido | El caso se cierra y no se ejecutan los escalones pendientes. |  |

### 5.21 CU-152 — Consultar el Registro de Auditoría

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-66 | CU-152<br>*Principal* | Administrador | Se hicieron operaciones recientes en el sistema (por ejemplo, las de los demás casos de esta prueba). | 1) Abrir la auditoría en el panel.<br>2) Filtrar por persona, por período y por resultado.<br>3) Abrir un asiento puntual. | ADM | Se listan los asientos que coinciden, del más reciente al más antiguo, con el total. Cada asiento muestra quién lo originó y con qué rol, qué operación fue, sobre qué recurso, cuándo y con qué resultado, sin credenciales. El sistema no ofrece modificar ni borrar asientos. |  |
| PA-67 | CU-152<br>*Alternativo: auditoría de datos* | Administrador | Existe un cambio reciente sobre un registro (por ejemplo, la cancelación de un pedido). | 1) Abrir la auditoría de datos y filtrar por la entidad y el período.<br>2) Abrir el detalle de un cambio. | ADM | El detalle muestra el tipo de acción, quién hizo el cambio y, por cada campo modificado, el valor anterior y el nuevo. |  |
| PA-68 | CU-152<br>*Excepción: la auditoría no se puede modificar* | Administrador | Ninguna. | 1) Abrir un asiento de la bitácora y un asiento de la auditoría de datos y buscar una opción para editarlos o borrarlos. | ADM | El panel no ofrece ninguna opción para modificar ni borrar asientos, para ningún rol. |  |
| PA-69 | CU-152<br>*Alternativo: sin coincidencias* | Administrador | Ninguna. | 1) Filtrar por un período anterior al inicio del sistema o por una persona sin operaciones. | ADM | El sistema muestra una lista vacía con total cero, sin error. |  |

## 6. Flujos críticos de punta a punta

Los flujos comprueban que los casos de uso funcionen encadenados, como los vive la distribuidora. Un flujo se aprueba solo si todos sus pasos se cumplen en una misma corrida.

### 6.1 FC-01 — Compra con efectivo, de punta a punta

Recorre el circuito completo del pedido pagado en efectivo, desde el catálogo hasta el cobro.

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-70 | FC-01<br>*Principal* | Cliente, Chofer | CLI-1, CHO-1 y CHO-2 con sesión iniciada; CHO-1 y CHO-2 disponibles y en línea; stock de PRD-10 anotado. | 1) CLI-1 arma un carrito con PRD-10 x 2, elige su dirección y el pago en efectivo, y confirma.<br>2) CHO-1 recibe la oferta y la acepta.<br>3) CHO-1 marca el pedido «En camino» y se desplaza hacia el domicilio.<br>4) CHO-1 elige «Llegué» y muestra el QR; CLI-1 lo escanea.<br>5) CHO-1 elige «Pago recibido».<br>6) El administrador revisa el pedido en el panel. | CLI-1, CHO-1, CHO-2, PRD-10 x 2 | Cada estado (pendiente, aceptado, en camino, entregado) se refleja en la aplicación del cliente y en el panel. El stock de PRD-10 bajó en dos unidades y no se restituye. Al final el pedido figura entregado y el pago como pagado, con el chofer que confirmó el cobro. El historial del pedido muestra todos los cambios de estado. *(CU involucrados: CU-005, CU-013, CU-015, CU-018, CU-017, CU-078, CU-079, CU-292.)* |  |
| PA-71 | FC-01<br>*Alternativo: el primer chofer rechaza* | Cliente, Chofer | Ídem anterior; CHO-1 más cerca que CHO-2. | 1) CLI-1 confirma un pedido en efectivo.<br>2) CHO-1 rechaza la oferta.<br>3) CHO-2 recibe la oferta y la acepta.<br>4) Completar la entrega y el cobro como en el flujo principal. | CLI-1, CHO-1, CHO-2 | La oferta pasa de inmediato a CHO-2 sin esperar el vencimiento y CHO-1 no vuelve a recibir ese pedido. El resto del circuito se completa igual que en el principal. *(CU involucrados: CU-005, CU-013, CU-016, CU-015, CU-079, CU-292.)* |  |

### 6.2 FC-02 — Compra con MercadoPago, de punta a punta

Recorre el circuito del pedido pagado en línea, incluida la espera del cobro.

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-72 | FC-02<br>*Principal* | Cliente, MercadoPago, Chofer | CLI-1 y CHO-1 con sesión iniciada; CHO-1 disponible. Pasarela de prueba o del distribuidor habilitada. | 1) CLI-1 arma un carrito con PRD-10 x 1, elige MercadoPago y confirma.<br>2) Antes de pagar, observar que CHO-1 no recibe ninguna oferta.<br>3) CLI-1 completa el pago (tarjeta de prueba aprobada en el entorno de pruebas de la pasarela; medio real de bajo monto, luego reintegrado, en producción).<br>4) CHO-1 recibe la oferta, la acepta y completa la entrega con el QR.<br>5) El administrador revisa el pedido y su pago en el panel. | CLI-1, CHO-1, PRD-10 x 1, medio de pago según el entorno | El total incluye el recargo del 10 % del pago en línea. Hasta el cobro no hay oferta. Con el pago aprobado, el cliente recibe el aviso y recién entonces el pedido se ofrece. Al terminar, el pedido figura entregado y pagado, sin que el chofer deba confirmar cobro alguno. *(CU involucrados: CU-005, CU-048, CU-013, CU-015, CU-018, CU-078, CU-079.)* |  |
| PA-73 | FC-02<br>*Excepción: el cobro nunca se completa* | Cliente, Sistema Automático | CLI-2 creó un pedido con MercadoPago y no pagó. Se anota el stock de PRD-10. | 1) Esperar el plazo de espera del cobro (60 minutos por omisión) y la corrida del proceso, que se ejecuta cada media hora.<br>2) Revisar el estado del pedido y el stock. | CLI-2, PRD-10 x 1 | El pedido queda cancelado de forma definitiva, con su motivo, y el stock de PRD-10 recupera la unidad apartada. *(CU involucrados: CU-005, CU-077.)* |  |

### 6.3 FC-03 — Despacho automático y entrega con código

Verifica la oferta secuencial a un chofer por vez y el mecanismo antifraude de la entrega.

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-74 | FC-03<br>*Principal* | Cliente, Chofer, Sistema Automático | CHO-1 y CHO-2 disponibles y en línea; CHO-1 más cerca. | 1) CLI-1 confirma un pedido en efectivo.<br>2) CHO-1 deja vencer la oferta.<br>3) CHO-2 recibe la oferta y la acepta.<br>4) El pedido pasa a en camino; CHO-2 pide el QR.<br>5) CLI-1 ingresa cinco códigos incorrectos y luego el correcto.<br>6) CHO-2 genera un código nuevo y CLI-1 lo ingresa. | CLI-1, CHO-1, CHO-2 | La oferta se ofrece a un solo chofer por vez. Al vencer la de CHO-1, pasa a CHO-2. El quinto intento fallido bloquea la confirmación, incluso con el código correcto. Con el código nuevo la entrega queda confirmada y el pedido figura entregado. *(CU involucrados: CU-013, CU-014, CU-015, CU-018, CU-078, CU-079.)* |  |
| PA-75 | FC-03<br>*Alternativo: nadie acepta* | Sistema Automático, Administrador | Hay choferes disponibles, pero ninguno acepta. | 1) CLI-3 confirma un pedido en efectivo.<br>2) CHO-1 y CHO-2 rechazan su oferta.<br>3) El administrador asigna el pedido manualmente a CHO-1 desde el panel.<br>4) CHO-1 marca el pedido «En camino» y muestra el QR.<br>5) CLI-3 lo escanea. | CLI-3, CHO-1, CHO-2, ADM | El administrador recibe el aviso de que no quedan choferes elegibles. El pedido asignado manualmente genera su código de entrega y la entrega se completa con normalidad con el QR. *(CU involucrados: CU-016, CU-012, CU-018, CU-078, CU-079.)* |  |

### 6.4 FC-04 — Cobro y rendición del chofer

Verifica que el dinero cobrado en la calle llegue a la caja de la distribuidora.

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-76 | FC-04<br>*Principal* | Chofer, Administrador, Sistema Automático | Se elige un chofer (CHO-2) y un día limpio, en el que ese chofer no entregó otros pedidos en efectivo. Si no es posible, el efectivo esperado se calcula con todos los pedidos en efectivo que entregó ese día, que se listan antes de empezar. Hay una caja activa con sesión abierta y no hay seña en los pedidos. | 1) CHO-2 entrega dos pedidos en efectivo (PED-A y PED-B) con el QR. En PED-A confirma «Pago recibido»; en PED-B no lo confirma, de modo que su cobro queda pendiente de confirmar.<br>2) Esperar la corrida nocturna (23:30) que arma la rendición.<br>3) A la mañana siguiente, CHO-2 abre «Mi rendición» y revisa los pedidos y el efectivo esperado.<br>4) CHO-2 declara el efectivo que entrega y un gasto de combustible con su comprobante.<br>5) El administrador abre «Rendiciones», revisa la rendición presentada, elige la caja destino y la aprueba. | CHO-2, ADM, caja de prueba, PED-A y PED-B de CLI-1 y CLI-2 | Existe una rendición abierta con los dos pedidos (cuentan los cobros pagados y los pendientes de confirmar). El efectivo esperado es la suma de los totales menos la seña ya paga de cada pedido; sin seña, la suma de los dos totales. Al presentarla, la rendición muestra el esperado, la diferencia (lo declarado más los gastos, menos lo esperado) y los gastos. Al aprobarla, el efectivo declarado entra a la caja destino y el saldo aumenta en ese monto. *(CU involucrados: CU-292, CU-231, CU-232, CU-233.)* |  |
| PA-77 | FC-04<br>*Alternativo: faltante de efectivo* | Chofer, Administrador | Rendición presentada con un faltante respecto del esperado. | 1) El administrador intenta aprobarla sin indicar cómo se resuelve la diferencia.<br>2) Elegir que la absorbe la distribuidora y aprobar. | CHO-2, ADM | Sin resolución indicada, el sistema rechaza la aprobación. Con la diferencia absorbida por la distribuidora, la rendición queda aprobada y la diferencia resuelta. *(CU involucrados: CU-232, CU-233.)* |  |
| PA-78 | FC-04<br>*Excepción: caja sin sesión abierta* | Administrador | La caja destino está cerrada. | 1) Intentar aprobar una rendición con efectivo mayor que cero hacia esa caja. | ADM | El sistema rechaza la aprobación y la rendición sigue presentada. Al abrir la caja y reintentar, se aprueba. *(CU involucrados: CU-233.)* |  |
| PA-79 | FC-04<br>*Alternativo: rendición sin cerrar* | Sistema Automático, Administrador | Existe una rendición de un día anterior sin aprobar. | 1) Esperar el aviso de las 08:00. | ADM | El administrador recibe un correo con la lista de rendiciones atrasadas. Cada rendición se avisa una vez. *(CU involucrados: CU-234.)* |  |

### 6.5 FC-05 — Caja del día

Verifica la apertura, los movimientos y el cierre con arqueo de una caja.

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-80 | FC-05<br>*Principal* | Administrador | ADM con sesión iniciada en el panel. Existe una caja activa que exige sesión y no tiene una abierta. | 1) Abrir la caja con el monto contado en el cierre anterior.<br>2) Registrar una entrada de dinero con categoría, medio y motivo.<br>3) Registrar una salida de dinero con categoría, medio y motivo.<br>4) Cerrar la caja contando el efectivo y verificando el esperado. | ADM, caja de prueba, importes de prueba | La caja admite movimientos solo con la sesión abierta. Cada movimiento actualiza el saldo en el acto. Al cerrar, el sistema muestra el monto esperado y, si el contado coincide, la sesión queda cerrada sin diferencia. *(CU involucrados: CU-226, CU-228, CU-309, CU-227.)* |  |
| PA-81 | FC-05<br>*Alternativo: arqueo con diferencia* | Administrador | Caja con la sesión abierta y movimientos. | 1) Cerrar la caja informando un monto contado menor que el esperado.<br>2) Repetir en otra sesión con un monto mayor. | ADM, caja de prueba | El sistema registra un movimiento de ajuste («faltante de caja» o «sobrante de caja») y el saldo queda igual a lo contado. La sesión queda cerrada con el esperado, el contado y la diferencia. *(CU involucrados: CU-227, CU-228, CU-309.)* |  |
| PA-82 | FC-05<br>*Excepción: movimientos inválidos* | Administrador | Caja cerrada o con sesión abierta. | 1) Intentar registrar una entrada con la caja sin sesión abierta.<br>2) Con la sesión abierta, intentar registrar una entrada de monto cero.<br>3) Intentar cerrar con un monto contado negativo. | ADM, caja de prueba | El sistema rechaza cada operación y el saldo no cambia. *(CU involucrados: CU-228, CU-227.)* |  |

### 6.6 FC-06 — Procesos automáticos implementados

Verifica los procesos que el sistema ejecuta por sí mismo, además de los de los casos esenciales.

| ID | CU y escenario | Actor | Precondiciones | Pasos | Datos de prueba | Resultado esperado | Resultado / Fecha / Observaciones |
|---|---|---|---|---|---|---|---|
| PA-83 | FC-06<br>*Reservas con seña* | Cliente, Sistema Automático | CLI-1 creó una reserva para el día de la prueba con la seña cobrada, y otra reserva con la seña sin pagar creada hace más del plazo (48 horas por omisión). | 1) Esperar la corrida de activación (cada cinco minutos).<br>2) Esperar la corrida de vencimiento (cada hora).<br>3) Revisar el estado de las dos reservas y el stock. | CLI-1, PRD-10 | La reserva con la seña cobrada y el día llegado pasa a pendiente y se ofrece al chofer más cercano. La reserva con la seña impaga vencida queda cancelada y su stock se restituye. *(CU involucrados: CU-072, CU-075, CU-076.)* |  |
| PA-84 | FC-06<br>*Aviso de stock bajo* | Sistema Automático, Administrador | Un depósito tiene un stock mínimo configurado y sus unidades llenas están por debajo. | 1) Esperar el aviso de las 08:00. | ADM, depósito de prueba | El administrador recibe un correo con el depósito y el tipo de garrafa bajo el mínimo, una sola vez. *(CU involucrados: CU-211.)* |  |

Los procesos automáticos de los casos CU-105, CU-106, CU-107 y CU-108 se prueban en la sección 5; las partes de esos procesos que corresponden a las aplicaciones del cliente y del chofer están en curso y quedan fuera de esta prueba.

## 7. Trazabilidad

### 7.1 Caso de uso → casos de prueba

| CU | Caso de uso | Casos de prueba propios | Casos de prueba en flujos críticos |
|---|---|---|---|
| CU-001 | Iniciar Sesión | PA-01, PA-02, PA-03, PA-04 | — |
| CU-002 | Registrarse como Cliente | PA-05, PA-06, PA-07 | — |
| CU-005 | Crear un Pedido | PA-08, PA-09, PA-10, PA-11, PA-12, PA-13, PA-14 | PA-70, PA-71, PA-72, PA-73 |
| CU-008 | Cancelar un Pedido (Cliente) | PA-15, PA-16, PA-17 | — |
| CU-022 | Activar la Disponibilidad | PA-18, PA-19 | — |
| CU-013 | Asignar un Pedido Automáticamente por Proximidad | PA-21, PA-22, PA-23 | PA-70, PA-71, PA-72, PA-74 |
| CU-014 | Vencer la Oferta y Ofrecer al Siguiente Chofer | PA-24, PA-25, PA-26 | PA-74 |
| CU-015 | Aceptar un Pedido | PA-27, PA-28, PA-29, PA-30 | PA-70, PA-71, PA-72, PA-74 |
| CU-017 | Modificar la Ubicación GPS del Chofer | PA-31, PA-32, PA-33 | PA-70 |
| CU-078 | Consultar el Código de Entrega (QR del chofer) | PA-34, PA-35, PA-36 | PA-70, PA-72, PA-74, PA-75 |
| CU-079 | Confirmar una Entrega Escaneando el QR (cliente) | PA-37, PA-38, PA-39, PA-40, PA-41 | PA-70, PA-71, PA-72, PA-74, PA-75 |
| CU-292 | Confirmar el Cobro en Efectivo | PA-42, PA-43, PA-44 | PA-70, PA-71, PA-76 |
| CU-301 | Confirmar una Transferencia | PA-45, PA-46, PA-47 | — |
| CU-048 | Procesar el Pago con MercadoPago | PA-48, PA-49, PA-50 | PA-72 |
| CU-023 | Registrar un Reclamo | PA-51, PA-52, PA-53 | — |
| CU-025 | Resolver un Reclamo | PA-54, PA-55, PA-56 | — |
| CU-105 | Planificar el Mantenimiento y las Habilitaciones de la Flota | PA-57, PA-58, PA-59 | — |
| CU-106 | Anticipar la Recompra por Consumo Estimado | PA-60, PA-61 | — |
| CU-107 | Agrupar Pedidos por Recorrido | PA-62, PA-63 | — |
| CU-108 | Recuperar Envases No Devueltos | PA-64, PA-65 | — |
| CU-152 | Consultar el Registro de Auditoría | PA-66, PA-67, PA-68, PA-69 | — |

Otros casos de uso, no esenciales, que intervienen en los casos de prueba (CU-266 tiene el suyo, PA-20, en la sección 5.5; los demás figuran en los flujos de la sección 6):

| CU | Casos de prueba |
|---|---|
| CU-012 | PA-75 |
| CU-016 | PA-71, PA-75 |
| CU-018 | PA-70, PA-72, PA-74, PA-75 |
| CU-072 | PA-83 |
| CU-075 | PA-83 |
| CU-076 | PA-83 |
| CU-077 | PA-73 |
| CU-211 | PA-84 |
| CU-226 | PA-80 |
| CU-227 | PA-80, PA-81, PA-82 |
| CU-228 | PA-80, PA-81, PA-82 |
| CU-231 | PA-76 |
| CU-232 | PA-76, PA-77 |
| CU-233 | PA-76, PA-77, PA-78 |
| CU-234 | PA-79 |
| CU-266 | PA-20 |
| CU-309 | PA-80, PA-81 |

### 7.2 Flujo crítico → casos de prueba

| Flujo crítico | Casos de prueba |
|---|---|
| FC-01 — Compra con efectivo, de punta a punta | PA-70, PA-71 |
| FC-02 — Compra con MercadoPago, de punta a punta | PA-72, PA-73 |
| FC-03 — Despacho automático y entrega con código | PA-74, PA-75 |
| FC-04 — Cobro y rendición del chofer | PA-76, PA-77, PA-78, PA-79 |
| FC-05 — Caja del día | PA-80, PA-81, PA-82 |
| FC-06 — Procesos automáticos implementados | PA-83, PA-84 |

**Resumen:** 84 casos de prueba: 68 corresponden a los 21 casos de uso esenciales, 1 (PA-20) a CU-266 y 15 a los flujos críticos.

## 8. Criterios de salida

### 8.1 Severidad de los defectos

| Severidad | Definición | Ejemplo |
|---|---|---|
| Crítica | Impide completar un flujo crítico o compromete el dinero, el stock o los datos de las personas. | El pedido pagado no se ofrece a ningún chofer; el cobro queda mal registrado. |
| Alta | Un caso de uso esencial no se puede completar, pero existe un camino alternativo. | La cancelación no restituye el stock del producto, pero el administrador lo corrige a mano. |
| Media | El caso se completa, pero con un comportamiento distinto del esperado o con un mensaje equivocado. | Un mensaje de error no coincide con el de la ficha. |
| Baja | Defecto estético o de redacción que no afecta el resultado. | Un texto mal alineado en una pantalla. |

### 8.2 Condiciones para dar por aprobada la prueba

El sistema se acepta para la entrega cuando se cumplen todas estas condiciones:

1. Se ejecutaron todos los casos de prueba de las secciones 5 y 6, con al menos 2 choferes y 5 clientes reales.
2. **El 100 % de los casos de los flujos críticos (sección 6) está aprobado.**
3. Al menos el **95 % de los casos de la sección 5 está aprobado** (con o sin observaciones) y ningún caso de prueba de un caso de uso crítico del catálogo queda rechazado.
4. No hay defectos de severidad **crítica** ni **alta** abiertos; los detectados están corregidos y verificados volviendo a ejecutar el caso que los reveló.
5. Los defectos de severidad **media** abiertos tienen una corrección acordada con fecha; los de severidad **baja** quedan registrados para una versión posterior.
6. Se completaron al menos 5 pedidos reales de extremo a extremo (criterio de la fase), con las repeticiones de FC-01 y FC-02 indicadas en la sección 4.

### 8.3 Qué bloquea la entrega

- Cualquier defecto de severidad crítica o alta sin corregir.
- Un caso de los flujos críticos rechazado.
- Un caso de prueba sin ejecutar por falta de entorno, de datos o de usuarios, salvo que el titular lo declare fuera de alcance por escrito.
- La imposibilidad de que un chofer o el administrador completen su tarea sin asistencia técnica.

### 8.4 Reglas de repetición

Un caso rechazado se vuelve a ejecutar completo después de la corrección. Si la corrección toca un caso de uso que participa de un flujo crítico, se repite también el flujo entero.

## 9. Registro de defectos

Se completa durante la prueba, un renglón por defecto. El número se cita en la columna de resultados del caso rechazado.

| N.º | Fecha | Caso de prueba | Descripción de lo observado | Severidad | Reportó | Estado (abierto / corregido / verificado) | Fecha de verificación |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |

## 10. Resumen de la ejecución

Se completa al cerrar la prueba.

| Concepto | Valor |
|---|---|
| Casos ejecutados / total | / 84 |
| Casos aprobados (con o sin observaciones) | |
| Casos rechazados | |
| Defectos críticos / altos / medios / bajos | |
| Pedidos reales de extremo a extremo completados | |
| Decisión (aceptado / aceptado con condiciones / no aceptado) | |
| Firma del titular y del distribuidor | |
