# Revisión adversarial de notación UML y estructura documental

Alcance: diagnóstico de los archivos `diagramas/uml/*.puml` y de `1-Requisitos.md`, `2-Analisis.md`, `3-Diseño.md`, contrastados contra UML 2.5 y contra las plantillas originales `.catedra-ref/1-Requisitos.txt`, `.catedra-ref/2.-Análisis.txt` y `.catedra-ref/3.-Diseño.txt`. No se modificó ningún `.puml` ni documento de tesis; este archivo es sólo diagnóstico.

## 1. Resumen ejecutivo

1. **Crítico:** `CU_Sistema_Diagrama-De-Contexto.puml` no es un diagrama de contexto UML y tampoco es un diagrama de casos de uso UML correcto: el título dice "Diagrama de Casos de Uso del Sistema" (`diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml:2`), pero dibuja los 18 subsistemas como elipses `usecase` dentro del sistema (`diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml:34` a `diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml:52`). Un subsistema no es un caso de uso.
2. **Crítico:** `Sistema Automático` sigue modelado como actor, aunque `1-Requisitos.md` lo define como procesos que el backend ejecuta por iniciativa propia (`1-Requisitos.md:352`) y aclara que el backend los dispara por sí mismo (`1-Requisitos.md:359` a `1-Requisitos.md:362`). En UML, un actor debe ser externo al sistema sujeto; si es cron interno, no corresponde como actor.
3. **Importante:** los diagramas de nivel sistema todavía tienen flechas donde, si se interpretan como asociaciones UML, deberían ser líneas sin punta: `CU_Sistema_Diagrama-Completo.puml` usa asociaciones actor-CU dirigidas desde `diagramas/uml/CU_Sistema_Diagrama-Completo.puml:279` hasta `diagramas/uml/CU_Sistema_Diagrama-Completo.puml:501`; `CU_Sistema_Diagrama-De-Contexto.puml` usa flechas actor-subsistema desde `diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml:55` hasta `diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml:114`; `CU_Sistema_Actores.puml` usa flechas actor-canal en `diagramas/uml/CU_Sistema_Actores.puml:42` a `diagramas/uml/CU_Sistema_Actores.puml:46`.
4. **Importante:** `CU_Sistema_Despliegue.puml` usa nodos (`node`) pero no declara artefactos (`artifact`); en su lugar coloca `component` dentro de nodos (`diagramas/uml/CU_Sistema_Despliegue.puml:31` a `diagramas/uml/CU_Sistema_Despliegue.puml:50`) y mezcla flujo CI/CD con despliegue runtime (`diagramas/uml/CU_Sistema_Despliegue.puml:66` a `diagramas/uml/CU_Sistema_Despliegue.puml:73`).
5. **Importante:** `3-Diseño.md` sigue sin reproducir literalmente los tres bloques que pide la plantilla por CU Real: `<Interface Gráfica para el caso de uso>`, `Operaciones` con firma y `Diagrama de Clase` (`.catedra-ref/3.-Diseño.txt:8` a `.catedra-ref/3.-Diseño.txt:96`). Hay interfaces gráficas sólo para algunos CU (`3-Diseño.md:229`, `3-Diseño.md:319`, `3-Diseño.md:427`, `3-Diseño.md:619`, `3-Diseño.md:693`, `3-Diseño.md:764`, `3-Diseño.md:889`, `3-Diseño.md:1016`) y el diagrama de clases está global (`3-Diseño.md:7817` a `3-Diseño.md:7827`), no por CU.
6. **Importante:** `1-Requisitos.md` no tiene secciones separadas llamadas `Fronteras del Sistema` ni `Casos de Usos de Alto Nivel`, aunque la plantilla las pide (`.catedra-ref/1-Requisitos.txt:30` a `.catedra-ref/1-Requisitos.txt:37`). Los CU de alto nivel están en otros archivos (`Casos-de-Uso.md:252`, `0-Plan_Del_Proyecto.md:210`).
7. **Importante:** las 5 relaciones `«extend»` de `1-Requisitos.md` §7.7 ya están resueltas, pero queda una relación `«include»` declarada y no dibujada en ningún `.puml`: `CU-005 Crear Pedido -> CU-013 Despacho Automático`, declarada en `1-Requisitos.md:6369`; una búsqueda real sobre `diagramas/uml/*.puml` no encontró `U005 ..> U013 : <<include>>`.
8. **Menor / resuelto:** las asociaciones actor-CU en los 18 diagramas de subsistema `CU_SS-*.puml` ya están como líneas sin punta, por ejemplo `A01 -[#1F6F8B]- U001` en `diagramas/uml/CU_SS-01_Autenticacion-Y-Usuarios.puml:57` y `A04 -[#8A6D1F]- U104` en `diagramas/uml/CU_SS-18_Observabilidad-Y-Operacion.puml:49`.
9. **Menor / resuelto:** el modelo conceptual ya no usa flechas de navegabilidad: está en Mermaid `classDiagram` (`2-Analisis.md:196` a `2-Analisis.md:197`) y sus asociaciones son `--`, composición `*--` o generalización `<|--` (`2-Analisis.md:307` a `2-Analisis.md:343`). El diagrama de clases de diseño ya es un diagrama real `classDiagram` (`3-Diseño.md:7817` a `3-Diseño.md:7827`).
10. **Menor / sin brecha:** `2-Analisis.md` sí cumple el formato de conceptos idóneos pedido por la plantilla: tiene `Símbolo / Intención / Extensión` en la tabla (`2-Analisis.md:43` a `2-Analisis.md:50`), conforme a `.catedra-ref/2.-Análisis.txt:20` a `.catedra-ref/2.-Análisis.txt:28`.

## 2. Ya resuelto por el usuario

Estos puntos fueron re-verificados leyendo los archivos actuales y no se reportan como hallazgos abiertos:

| Punto verificado | Evidencia leída | Dictamen |
|---|---|---|
| Las 5 relaciones `«extend»` de `1-Requisitos.md` §7.7 están dibujadas. | La tabla declara 5 `extend` en `1-Requisitos.md:6379` a `1-Requisitos.md:6385`. Están en `CU_SS-03` (`diagramas/uml/CU_SS-03_Despacho-Y-Asignacion.puml:66` a `diagramas/uml/CU_SS-03_Despacho-Y-Asignacion.puml:68`), `CU_SS-02` (`diagramas/uml/CU_SS-02_Gestion-De-Pedidos.puml:139` a `diagramas/uml/CU_SS-02_Gestion-De-Pedidos.puml:145`), `CU_SS-04` (`diagramas/uml/CU_SS-04_Seguimiento-En-Tiempo-Real.puml:72` a `diagramas/uml/CU_SS-04_Seguimiento-En-Tiempo-Real.puml:74`) y `CU_SS-05` (`diagramas/uml/CU_SS-05_Reclamos.puml:52` a `diagramas/uml/CU_SS-05_Reclamos.puml:54`). | Resuelto: la flecha va de la extensión al caso base y el punto de extensión está documentado con nota. |
| Los 5 casos de uso factorizados existen como elipses estereotipadas. | `Reservar Stock` y `Recargo por Transferencia` están en `diagramas/uml/CU_SS-02_Gestion-De-Pedidos.puml:75` a `diagramas/uml/CU_SS-02_Gestion-De-Pedidos.puml:76`; `Notificar Cliente` está en `diagramas/uml/CU_SS-03_Despacho-Y-Asignacion.puml:49` y `diagramas/uml/CU_SS-04_Seguimiento-En-Tiempo-Real.puml:51`; `Adjuntar Foto` está en `diagramas/uml/CU_SS-05_Reclamos.puml:44`. | Resuelto para los factorizados leídos: aparecen como `usecase ... <<factorizado>>`. |
| Las asociaciones actor-CU en los 18 `CU_SS-*.puml` no tienen punta. | Ejemplos extremos: `CU_SS-01` usa `A01 -[#1F6F8B]- U001` en `diagramas/uml/CU_SS-01_Autenticacion-Y-Usuarios.puml:57`; `CU_SS-18` usa `A04 -[#8A6D1F]- U104` en `diagramas/uml/CU_SS-18_Observabilidad-Y-Operacion.puml:49`. La misma forma sin `->` fue verificada en todos los `CU_SS-*.puml`. | Resuelto: no queda el hallazgo anterior de flechas en diagramas de subsistema. |
| El modelo conceptual no usa flechas de navegabilidad. | El modelo empieza como Mermaid `classDiagram` en `2-Analisis.md:196` a `2-Analisis.md:197`; las relaciones del modelo son generalización `<|--`, asociación `--` y composición `*--` en `2-Analisis.md:307` a `2-Analisis.md:343`. | Resuelto: no hay navegabilidad `-->` en el modelo conceptual. |
| El diagrama de clases de diseño ya no es arte ASCII. | `3-Diseño.md` declara `## 5. Diagrama de Clases de Diseño` en `3-Diseño.md:7817` y abre un bloque Mermaid `classDiagram` en `3-Diseño.md:7826` a `3-Diseño.md:7827`. | Resuelto: existe un diagrama de clases real. |

## 3. FRENTE A - PlantUML / UML 2.5

### 3.1 Crítico - `CU_Sistema_Diagrama-De-Contexto.puml` no es un diagrama de contexto formal

**Archivo:** `diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml`

**Qué hay:** el archivo se titula `Diagrama de Casos de Uso del Sistema — SPLG` (`diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml:2`). Dentro del límite `rectangle "Sistema de Pedidos y Logística de Garrafas de Gas (SPLG)"` (`diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml:34`) dibuja `SS-01` a `SS-18` como `usecase` (`diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml:35` a `diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml:52`). Luego conecta actores con esos supuestos casos de uso mediante flechas dirigidas (`diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml:55` a `diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml:114`).

**Dictamen UML:** por contenido actual, no es un diagrama de contexto UML: muestra estructura interna de subsistemas y no sólo frontera externa del sistema con actores/sistemas externos. Tampoco es un diagrama de casos de uso válido, porque las elipses no representan objetivos funcionales de actores sino subsistemas. En UML, un subsistema debe representarse como paquete/componente/clasificador estereotipado, no como elipse de caso de uso.

**Cómo debería llamarse:**

- Si se quiere conservar su intención actual, debería llamarse `Vista de interacción actor-subsistema` o `Mapa actor-subsistema`, dejando claro que es una vista informal o estructural.
- Si debe ser formal UML, conviene dividirlo: `CU_Sistema_Diagrama-De-Casos-De-Uso.puml` para casos de uso reales y `CU_Sistema_Subsistemas.puml` para paquetes/componentes `«subsystem»`.
- Si realmente debe ser un `Diagrama de Contexto`, debería mostrar el sujeto SPLG como caja única y sólo actores/sistemas externos alrededor; no debería listar los 18 subsistemas internos.

**Qué cambiar puntualmente en `generar-uml.py`:**

| Línea | Qué genera hoy | Cambio recomendado |
|---|---|---|
| `generar-uml.py:178` | `title Diagrama de Casos de Uso del Sistema — SPLG` para el archivo llamado `CU_Sistema_Diagrama-De-Contexto`. | Cambiar el título según el objetivo real. Para contexto: `title Diagrama de Contexto — SPLG`. Para vista de subsistemas: `title Vista de Subsistemas — SPLG`. |
| `generar-uml.py:182` a `generar-uml.py:186` | Abre el rectángulo del sistema y emite cada subsistema con `usecase "... SS-xx ..."` | Si el archivo queda como contexto, no generar los subsistemas internos. Si queda como vista de subsistemas, reemplazar `usecase` por `component "... " as SS01 <<subsystem>>` o `package "... " as SS01 <<subsystem>>`. |
| `generar-uml.py:194` | Emite `Axx -[#color]-> SSxx`. | Si se mantiene como asociación informativa, quitar la punta: `Axx -[#color]- SSxx`. Si se corrige a contexto formal, eliminar esas conexiones a subsistemas internos y conectar actores sólo con el sistema como caja negra o con sistemas externos. |

### 3.2 Importante - Diagramas de nivel sistema con flechas en asociaciones

**Regla UML:** en diagramas de casos de uso, la comunicación actor-caso de uso es una asociación, y la notación estándar es una línea sólida sin flecha. La flecha sugiere dirección/navegabilidad, que no forma parte de la semántica de la asociación actor-CU.

| Archivo | Qué hay | Dictamen y corrección |
|---|---|---|
| `diagramas/uml/CU_Sistema_Diagrama-Completo.puml` | Asociaciones actor-CU con flecha desde `diagramas/uml/CU_Sistema_Diagrama-Completo.puml:279` hasta `diagramas/uml/CU_Sistema_Diagrama-Completo.puml:501`, por ejemplo `A01SS01 -[#1F6F8B]-> U001` en `diagramas/uml/CU_Sistema_Diagrama-Completo.puml:279`. | Sí corresponde corregirlas: reemplazar `->` por línea sin punta. El generador está en `generar-uml.py:231`, donde arma `flechas.append(f'A{k}{...} -[{COLOR_ACT[k]}]-> {eid(c)}')`; debería emitir `-[color]-`. |
| `diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml` | Flechas actor-subsistema desde `diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml:55` hasta `diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml:114`. | No son actor-CU reales porque los destinos son subsistemas mal dibujados como `usecase`. Si el diagrama queda como vista informal actor-subsistema, quitar puntas en `generar-uml.py:194`; si se vuelve contexto formal, sacar esas relaciones internas. |
| `diagramas/uml/CU_Sistema_Actores.puml` | Flechas actor-canal en `diagramas/uml/CU_Sistema_Actores.puml:42` a `diagramas/uml/CU_Sistema_Actores.puml:46` y flechas canal-backend en `diagramas/uml/CU_Sistema_Actores.puml:48` a `diagramas/uml/CU_Sistema_Actores.puml:51`. | No son asociaciones actor-CU porque los destinos son apps/procesos/backend, no casos de uso. Si se presenta como vista UML formal, renombrarlo como vista de canales o convertirlo a componente/comunicación. Si se mantiene como asociación simple actor-canal, quitar puntas en `generar-uml.py:171`; las flechas app-backend de `generar-uml.py:172` pertenecen a una vista arquitectónica, no a CU. |

### 3.3 Crítico - `Sistema Automático` como actor no es ortodoxo si representa procesos internos

**Qué hay:** `1-Requisitos.md` define `ACT-04 | Sistema Automático | Automático` como "Procesos que el backend ejecuta por iniciativa propia" (`1-Requisitos.md:352`). Debajo afirma que no tiene interfaz, que el backend lo dispara por sí mismo y que es actor principal de casos automáticos (`1-Requisitos.md:359` a `1-Requisitos.md:362`). El actor aparece, por ejemplo, en `diagramas/uml/CU_Sistema_Actores.puml:31`, `diagramas/uml/CU_Sistema_Diagrama-De-Contexto.puml:31` y `diagramas/uml/CU_Sistema_Diagrama-Completo.puml:274`.

**Dictamen UML:** si esos procesos son parte del backend, `Sistema Automático` no es actor UML. Un actor es externo al sistema sujeto. Un cron interno, un job interno o un scheduler dentro del backend pertenece al sistema, por lo que no debería aparecer como actor.

**Salida ortodoxa:**

- Si el disparador se quiere mantener como externo, cambiar el actor a algo como `«system» Tiempo` o `«system» Scheduler externo`, explicitando que está fuera de SPLG y que sólo dispara eventos temporales.
- Si el scheduler corre dentro del backend SPLG, sacar `Sistema Automático` de los diagramas de casos de uso. En los CU automáticos, documentar el disparo como "Evento disparador: vencimiento de timer / job programado" y modelar el detalle interno en diseño con secuencia, actividad o componentes internos.

### 3.4 Importante - `CU_Sistema_Despliegue.puml` mezcla despliegue UML con componentes y pipeline

**Archivo:** `diagramas/uml/CU_Sistema_Despliegue.puml`

**Qué hay:** el archivo usa `node` para `Máquina de desarrollo`, `GitHub` y `Producción` (`diagramas/uml/CU_Sistema_Despliegue.puml:31`, `diagramas/uml/CU_Sistema_Despliegue.puml:40`, `diagramas/uml/CU_Sistema_Despliegue.puml:47`). Dentro de esos nodos coloca `component` para backend, frontend, apps, repositorios y workflows (`diagramas/uml/CU_Sistema_Despliegue.puml:32` a `diagramas/uml/CU_Sistema_Despliegue.puml:35`, `diagramas/uml/CU_Sistema_Despliegue.puml:41` a `diagramas/uml/CU_Sistema_Despliegue.puml:44`, `diagramas/uml/CU_Sistema_Despliegue.puml:48` a `diagramas/uml/CU_Sistema_Despliegue.puml:50`). No aparece ninguna declaración `artifact` en el archivo. Además, las líneas `DEV --> REPO`, `REPO --> CI`, `DEP --> REN`, `DEP --> NET` y `DEP --> SL` (`diagramas/uml/CU_Sistema_Despliegue.puml:66` a `diagramas/uml/CU_Sistema_Despliegue.puml:72`) describen flujo de entrega/CI-CD, no una topología runtime.

**Dictamen UML:** usa parte de la notación de despliegue porque hay `node`, pero está incompleto formalmente: faltan artefactos desplegados y se mezclan componentes lógicos con workflow de entrega. En UML 2.5, el diagrama de despliegue debería mostrar nodos, artefactos desplegados y caminos de comunicación/deployment entre nodos.

**Qué debería haber:** por ejemplo, `node "Render"` con `artifact "backend build / container"`; `node "PostgreSQL/PostGIS"` y `node "Redis"` como nodos/servicios de ejecución; `node "Netlify"` con `artifact "admin build"` y `artifact "docs build"`. Las relaciones runtime deberían ser caminos de comunicación entre nodos/artefactos. El flujo GitHub Actions conviene separarlo a un diagrama de pipeline o actividad.

### 3.5 Include/Extend faltantes

**Estado actual:** no quedan `extend` faltantes de la tabla `1-Requisitos.md` §7.7 después de la corrección del usuario. La tabla declara 6 `include` en `1-Requisitos.md:6366` a `1-Requisitos.md:6373` y 5 `extend` en `1-Requisitos.md:6379` a `1-Requisitos.md:6385`. De los `include`, 5 están dibujados y 1 sigue faltando: `CU-005 Crear Pedido -> CU-013 Despacho Automático`, declarada en `1-Requisitos.md:6369` y no encontrada en `diagramas/uml/*.puml`.

| Relación | Tipo | Archivo `.puml` | Sintaxis PlantUML verificada o propuesta |
|---|---|---|---|
| CU-005 Crear Pedido -> Reservar Stock | include | `diagramas/uml/CU_SS-02_Gestion-De-Pedidos.puml` | `U005 ..> F_STOCK : <<include>>` (`diagramas/uml/CU_SS-02_Gestion-De-Pedidos.puml:136`) |
| CU-005 Crear Pedido -> CU-013 Despacho Automático | include | Falta dibujarla; por cruzar `SS-02` y `SS-03`, el lugar más claro es `diagramas/uml/CU_Sistema_Diagrama-Completo.puml` | Propuesta: `U005 ..> U013 : <<include>>` |
| CU-044 Seleccionar Franja Horaria -> CU-045 Consultar Franjas Disponibles | include | `diagramas/uml/CU_SS-09_Franjas-Horarias.puml` | `U044 ..> U045 : <<include>>` (`diagramas/uml/CU_SS-09_Franjas-Horarias.puml:57`) |
| CU-015 Aceptar Pedido -> Notificar Cliente | include | `diagramas/uml/CU_SS-03_Despacho-Y-Asignacion.puml` | `U015 ..> F_AVISO : <<include>>` (`diagramas/uml/CU_SS-03_Despacho-Y-Asignacion.puml:63`) |
| CU-018 Marcar En Camino -> Notificar Cliente | include | `diagramas/uml/CU_SS-04_Seguimiento-En-Tiempo-Real.puml` | `U018 ..> F_AVISO : <<include>>` (`diagramas/uml/CU_SS-04_Seguimiento-En-Tiempo-Real.puml:68`) |
| CU-020 Confirmar Entrega -> Notificar Cliente | include | `diagramas/uml/CU_SS-04_Seguimiento-En-Tiempo-Real.puml` | `U020 ..> F_AVISO : <<include>>` (`diagramas/uml/CU_SS-04_Seguimiento-En-Tiempo-Real.puml:69`) |
| CU-014 Reintentar Asignación (Cron) -> CU-013 Despacho Automático | extend | `diagramas/uml/CU_SS-03_Despacho-Y-Asignacion.puml` | `U014 ..> U013 : <<extend>>` con nota de punto de extensión (`diagramas/uml/CU_SS-03_Despacho-Y-Asignacion.puml:66` a `diagramas/uml/CU_SS-03_Despacho-Y-Asignacion.puml:68`) |
| Aplicar Promoción -> CU-005 Crear Pedido | extend | `diagramas/uml/CU_SS-02_Gestion-De-Pedidos.puml` | `F_PROMO ..> U005 : <<extend>>` con nota de punto de extensión (`diagramas/uml/CU_SS-02_Gestion-De-Pedidos.puml:139` a `diagramas/uml/CU_SS-02_Gestion-De-Pedidos.puml:141`) |
| Recargo por Transferencia -> CU-005 Crear Pedido | extend | `diagramas/uml/CU_SS-02_Gestion-De-Pedidos.puml` | `F_RECAR ..> U005 : <<extend>>` con nota de punto de extensión (`diagramas/uml/CU_SS-02_Gestion-De-Pedidos.puml:143` a `diagramas/uml/CU_SS-02_Gestion-De-Pedidos.puml:145`) |
| CU-019 Avisar Llegada -> CU-018 Marcar En Camino | extend | `diagramas/uml/CU_SS-04_Seguimiento-En-Tiempo-Real.puml` | `U019 ..> U018 : <<extend>>` con nota de punto de extensión (`diagramas/uml/CU_SS-04_Seguimiento-En-Tiempo-Real.puml:72` a `diagramas/uml/CU_SS-04_Seguimiento-En-Tiempo-Real.puml:74`) |
| Adjuntar Foto -> CU-023 Registrar Reclamo | extend | `diagramas/uml/CU_SS-05_Reclamos.puml` | `F_FOTO ..> U023 : <<extend>>` con nota de punto de extensión (`diagramas/uml/CU_SS-05_Reclamos.puml:52` a `diagramas/uml/CU_SS-05_Reclamos.puml:54`) |

**Discrepancia abierta:** la relación `CU-005 Crear Pedido -> CU-013 Despacho Automático` declarada como `include` en `1-Requisitos.md:6369` no aparece en ningún `.puml` al buscar `U005` con `U013` ni por los nombres textuales `Crear Pedido` / `Despacho Automático`. Como cruza `SS-02` y `SS-03`, no se fuerza dentro de un único `CU_SS-*`; debería agregarse en `CU_Sistema_Diagrama-Completo.puml` o en un diagrama específico de relaciones transversales.

## 4. FRENTE B - Brechas estructurales contra plantillas

### 4.1 Importante - `3-Diseño.md` no sigue literalmente los tres bloques exigidos por CU Real

**Plantilla:** `3.-Diseño.txt` pide `Casos de Usos Reales` (`.catedra-ref/3.-Diseño.txt:8`), `<Interface Gráfica para el caso de uso>` (`.catedra-ref/3.-Diseño.txt:9`), `Operaciones` (`.catedra-ref/3.-Diseño.txt:92`), una firma tipo `Operación: buscarHabitacion(tipo,fecha)` (`.catedra-ref/3.-Diseño.txt:93`) y `Diagrama de Clase` (`.catedra-ref/3.-Diseño.txt:96`).

**Qué hay:** `3-Diseño.md` tiene encabezados `#### Interfaz Gráfica` para algunos casos (`3-Diseño.md:229`, `3-Diseño.md:319`, `3-Diseño.md:427`, `3-Diseño.md:619`, `3-Diseño.md:693`, `3-Diseño.md:764`, `3-Diseño.md:889`, `3-Diseño.md:1016`), pero no aparece una sección formal `#### Operaciones` por CU en el barrido de encabezados. El diagrama de clases existe, pero como sección global `## 5. Diagrama de Clases de Diseño` (`3-Diseño.md:7817`) con bloque `classDiagram` (`3-Diseño.md:7826` a `3-Diseño.md:7827`), no como `Diagrama de Clase` por CU Real.

**Dictamen:** el arreglo del diagrama de clases corrige el problema de "arte ASCII", pero no elimina la brecha de estructura contra la plantilla. Si la cátedra corrige literalmente, cada CU Real debería tener su bloque de interfaz, su sección `Operaciones` con firmas y su `Diagrama de Clase` o una referencia explícita al diagrama aplicable.

### 4.2 Importante - `1-Requisitos.md` no tiene `Fronteras del Sistema` ni `Casos de Usos de Alto Nivel` como secciones propias

**Plantilla:** el índice de la plantilla de requisitos pide `Fronteras del Sistema` y `Casos de Usos de Alto Nivel` como secciones separadas (`.catedra-ref/1-Requisitos.txt:30` a `.catedra-ref/1-Requisitos.txt:37`).

**Qué hay:** en `1-Requisitos.md`, los casos de uso expandidos arrancan directamente en `### 7.2 Casos de Uso Expandidos — Críticos` (`1-Requisitos.md:367`) y no aparece una sección separada de alto nivel en el barrido de encabezados. Los CU de alto nivel están en `Casos-de-Uso.md:252` y `0-Plan_Del_Proyecto.md:210`.

**Dictamen:** el contenido existe parcialmente fuera del Doc 1, pero la estructura de `1-Requisitos.md` no replica la plantilla. Para una entrega corregida contra plantilla, conviene agregar en el Doc 1 una sección `Fronteras del Sistema` y una sección `Casos de Usos de Alto Nivel`, aunque esta última remita formalmente a `Casos-de-Uso.md`.

### 4.3 Menor - `2-Analisis.md` cumple `Símbolo / Intención / Extensión`

**Plantilla:** `2.-Análisis.txt` pide los campos `Símbolo`, `Intención` y `Extensión` para conceptos idóneos (`.catedra-ref/2.-Análisis.txt:20` a `.catedra-ref/2.-Análisis.txt:28`).

**Qué hay:** `2-Analisis.md` tiene `### 1.2 Lista de Conceptos Idóneos` (`2-Analisis.md:43`) y una tabla con columnas `Concepto | Símbolo | Intención | Extensión` (`2-Analisis.md:50`).

**Dictamen:** no hay brecha abierta en este punto. La presentación en tabla no es idéntica visualmente a la plantilla, pero conserva los campos pedidos.

## 5. Recomendación de corrección priorizada

1. Corregir `CU_Sistema_Diagrama-De-Contexto.puml` desde `generar-uml.py`: decidir si será contexto real, vista de subsistemas o diagrama de casos de uso. No presentar subsistemas como elipses `usecase`.
2. Decidir la política de `Sistema Automático`: si es interno, sacarlo como actor; si se mantiene, convertirlo en actor externo `«system» Tiempo/Scheduler externo`.
3. Quitar puntas de flecha en asociaciones actor-CU de `CU_Sistema_Diagrama-Completo.puml` y corregir `generar-uml.py:231`. Revisar si `CU_Sistema_Diagrama-De-Contexto.puml` y `CU_Sistema_Actores.puml` se mantienen como vistas informales o se reconvierten a UML formal.
4. Rehacer `CU_Sistema_Despliegue.puml` como despliegue UML: nodos, artefactos desplegados y caminos de comunicación runtime; dejar CI/CD en otro diagrama.
5. Ajustar `3-Diseño.md` a la plantilla literal: `Interfaz Gráfica`, `Operaciones` con firmas y `Diagrama de Clase` por CU Real o referencia explícita por CU.
6. Agregar en `1-Requisitos.md` las secciones `Fronteras del Sistema` y `Casos de Usos de Alto Nivel`, aunque sea remitiendo formalmente a `Casos-de-Uso.md`.
