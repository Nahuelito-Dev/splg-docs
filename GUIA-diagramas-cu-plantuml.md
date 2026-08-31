# Guía de Diagramas UML — SPLG (PlantUML)
**Proyecto:** SPLG – Sistema de Pedidos y Logística de Garrafas de Gas
**Autor:** Nahuel Wagner — FCEQyN, UNaM
**Propósito:** Construir los diagramas que pide la cátedra (RUP/UP) en **notación UML formal**, con relaciones `«include»` / `«extend»`, listas para renderizar a PNG e insertar en los Docs 0, 1, 2 y 3.

> Esta guía cubre **los diagramas de casos de uso del sistema y de subsistemas**, porque
> Mermaid `flowchart` no dibuja la notación UML de casos de uso (óvalos, monigotes y
> flechas `«include»` / `«extend»` punteadas). Los diagramas de secuencia sí están en
> Mermaid, en `Casos-de-Uso.md` sección 6 y en `2-Analisis.md` sección 2.1.

---

## 0. Cómo renderizar PlantUML (elegí una)

| Método | Pasos | Cuándo usarlo |
|--------|-------|---------------|
| **Web (lo más rápido)** | Ir a **https://www.plantuml.com/plantuml/uml/** → borrar el ejemplo → pegar el código → la imagen aparece sola → click derecho → *Guardar imagen como* PNG | Para entregar ya |
| **VS Code** | Instalar extensión *PlantUML* (jebbs) + Java + Graphviz → abrir un `.puml` → `Alt+D` previsualiza → click derecho *Export Current Diagram* → PNG/SVG | Si vas a iterar mucho |
| **PlantText** | **https://www.planttext.com/** → pegar → *Refresh* → descargar | Alternativa web |

> **Tip de calidad:** exportá en **SVG** si la cátedra acepta, o PNG a `@scale 1.5` para que no se pixele en el Word/PDF. Para PNG nítido agregá `skinparam dpi 150` al inicio del bloque.

**Convención de nombres** (guardar todo en `docs/`):

| Archivo PNG | Inserta en |
|-------------|-----------|
| `diagrama-cu-sistema.png` | Doc 0 §6 y Doc 1 §3 |
| `diagrama-subsistemas.png` | Doc 1 §4 |
| `cu-ss02-pedidos.png` | Doc 1 §6 |
| `cu-ss03-despacho.png` | Doc 1 §6 |
| `cu-ss04-seguimiento.png` | Doc 1 §6 |
| `cu-ss05-reclamos.png` | Doc 1 §6 |
| `cu-ss09-franjas.png` | Doc 1 §6 |

---

## 1. Cómo se leen `«include»` y `«extend»` (para defenderlo en la mesa)

| Relación | Significado | Dirección de la flecha (punteada) | Regla mnemotécnica |
|----------|-------------|-----------------------------------|--------------------|
| **`«include»`** | El comportamiento **siempre** ocurre. Se factoriza para no repetirlo en varios CU. | **CU base ⇢ CU incluido** | "Para hacer A, **obligatoriamente** hago B" |
| **`«extend»`** | Comportamiento **opcional/condicional**. Se agrega solo si se cumple una condición en un *punto de extensión*. | **CU que extiende ⇢ CU base** | "A veces, sobre B, **además** pasa A" |

Las flechas SIEMPRE son **punteadas** (`..>`) con el estereotipo escrito. El error más común es invertir la dirección del `extend`: la flecha va **desde** el caso opcional **hacia** el caso base.

### Relaciones definidas en SPLG

**`«include»` (siempre se ejecutan):**

| CU base | incluye | Justificación |
|---------|---------|---------------|
| CU-005 Crear Pedido | → Reservar Stock | Toda creación reserva stock en transacción (DSS de stock) |
| CU-005 Crear Pedido | → CU-013 Despacho Automático | El despacho se dispara siempre al confirmar el pedido |
| CU-044 Seleccionar Franja | → CU-045 Consultar Franjas Disponibles | Para elegir, primero siempre se consultan las disponibles |
| CU-015 / CU-018 / CU-020 | → Notificar Cliente | Los tres disparan la misma notificación WS+FCM |

**`«extend»` (condicionales):**

| CU que extiende | extiende a | Punto de extensión |
|-----------------|-----------|--------------------|
| CU-014 Reintentar Asignación | → CU-013 Despacho Automático | *no hay choferes en el radio* |
| Aplicar Promoción | → CU-005 Crear Pedido | *cantidad ≥ umbral de promoción* |
| Recargo por Transferencia | → CU-005 Crear Pedido | *método de pago = transferencia* |
| CU-019 Avisar Llegada | → CU-018 Marcar En Camino | *el chofer está cerca del destino* |
| Adjuntar Foto al Reclamo | → CU-023 Registrar Reclamo | *el cliente adjunta evidencia* |
| CU-048 Procesar Pago (MercadoPago) | → CU-005 Crear Pedido | *método de pago = MercadoPago* |

> "Reservar Stock", "Notificar Cliente", "Aplicar Promoción", "Recargo por Transferencia" y "Adjuntar Foto" son **casos de uso factorizados**: no eran CU numerados, los introducimos justamente para expresar la relación. No hace falta darles un CU-XXX; alcanza con nombrarlos en el diagrama.

---

## 2. Diagrama de Casos de Uso del Sistema  → `diagrama-cu-sistema.png`

**Qué muestra:** el límite del sistema (rectángulo), los 4 actores, los CU principales agrupados por subsistema y las relaciones `«include»`/`«extend»`.

> Para que no quede ilegible, este diagrama del **sistema** muestra los CU **críticos + los que tienen include/extend**. El detalle de cada subsistema va en los diagramas de la sección §4.

```plantuml
@startuml diagrama-cu-sistema
skinparam dpi 150
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam usecase {
  BackgroundColor #F4F9F4
  BorderColor #2E7D32
}
title Diagrama de Casos de Uso del Sistema — SPLG

actor "Cliente"        as C
actor "Chofer"         as CH
actor "Administrador"  as A
actor "Sistema\n(tiempo / cron)" as S

rectangle "SPLG — Sistema de Pedidos y Logística de Garrafas de Gas" {

  ' --- Autenticación ---
  usecase "Iniciar Sesión"            as UC001
  usecase "Registrarse como Cliente"  as UC002

  ' --- Pedidos ---
  usecase "Crear Pedido"              as UC005
  usecase "Reservar Stock"            as UCSTK
  usecase "Aplicar Promoción"         as UCPRO
  usecase "Recargo por Transferencia" as UCREC
  usecase "Consultar Pedido"          as UC006
  usecase "Cancelar Pedido"           as UC008
  usecase "Listar Pedidos"            as UC011

  ' --- Despacho ---
  usecase "Despacho Automático\npor Proximidad" as UC013
  usecase "Reintentar Asignación\n(Cron)"       as UC014
  usecase "Aceptar Pedido"            as UC015

  ' --- Seguimiento ---
  usecase "Actualizar GPS"            as UC017
  usecase "Marcar En Camino"          as UC018
  usecase "Avisar Llegada"            as UC019
  usecase "Confirmar Entrega"         as UC020
  usecase "Notificar Cliente"         as UCNOT
  usecase "Activar/Desactivar\nDisponibilidad" as UC022

  ' --- Reclamos ---
  usecase "Registrar Reclamo"         as UC023
  usecase "Adjuntar Foto"             as UCFOT
  usecase "Resolver Reclamo"          as UC025

  ' --- Choferes / Productos / Franjas / Reportes ---
  usecase "Registrar Chofer"          as UC031
  usecase "Validar Chofer"            as UC032
  usecase "Gestionar Catálogo"        as UC036
  usecase "Seleccionar Franja"        as UC044
  usecase "Consultar Franjas"         as UC045
  usecase "Ver Dashboard"             as UC026

  ' --- CU agregados (046-051) ---
  usecase "Gestionar Direcciones\nde Entrega" as UC046
  usecase "Recuperar Contraseña"      as UC047
  usecase "Procesar Pago\n(MercadoPago)" as UC048
  usecase "Consultar Balance\ndel Chofer" as UC049
  usecase "Bloquear/Desbloquear\nUsuario" as UC050
  usecase "Gestionar Vehículos"       as UC051
}

' ===== Asociaciones actor – CU =====
C  -- UC001
C  -- UC002
C  -- UC005
C  -- UC006
C  -- UC008
C  -- UC023
C  -- UC044
C  -- UC046
C  -- UC047

CH -- UC001
CH -- UC015
CH -- UC017
CH -- UC018
CH -- UC020
CH -- UC022
CH -- UC049

A  -- UC001
A  -- UC011
A  -- UC025
A  -- UC031
A  -- UC032
A  -- UC036
A  -- UC026
A  -- UC050
A  -- UC051

S  -- UC013
S  -- UC014
S  -- UC048

' ===== INCLUDE (siempre) =====
UC005 ..> UCSTK : <<include>>
UC005 ..> UC013 : <<include>>
UC044 ..> UC045 : <<include>>
UC015 ..> UCNOT : <<include>>
UC018 ..> UCNOT : <<include>>
UC020 ..> UCNOT : <<include>>

' ===== EXTEND (condicional) =====
UC014 ..> UC013 : <<extend>>\n(sin choferes en radio)
UCPRO ..> UC005 : <<extend>>\n(cantidad >= umbral)
UCREC ..> UC005 : <<extend>>\n(pago = transferencia)
UC019 ..> UC018 : <<extend>>\n(chofer cerca)
UCFOT ..> UC023 : <<extend>>\n(adjunta evidencia)
UC048 ..> UC005 : <<extend>>\n(pago = MercadoPago)

@enduml
```

---

## 3. Diagrama de Subsistemas  → `diagrama-subsistemas.png`

**Qué muestra:** los 9 subsistemas como paquetes, los frontends que los consumen y la infraestructura, con dependencias `..>`.

```plantuml
@startuml diagrama-subsistemas
skinparam dpi 150
skinparam packageStyle rectangle
skinparam shadowing false
title Diagrama de Subsistemas — SPLG

package "Capa de Presentación" #EEF6FF {
  component "App Cliente\n(Flutter)"  as AC
  component "App Chofer\n(Flutter)"   as ACH
  component "Panel Admin\n(React)"    as PA
}

package "Backend NestJS" #F4F9F4 {
  package "SS-01 Autenticación"        as SS01
  package "SS-02 Gestión de Pedidos"   as SS02
  package "SS-03 Despacho y Asignación" as SS03
  package "SS-04 Seguimiento RT"       as SS04
  package "SS-05 Reclamos"             as SS05
  package "SS-06 Reportes"             as SS06
  package "SS-07 Choferes y Vehículos" as SS07
  package "SS-08 Productos e Inventario" as SS08
  package "SS-09 Franjas Horarias"     as SS09
}

package "Infraestructura" #FFF6E5 {
  database "PostgreSQL"        as PG
  database "Redis GEO"         as RD
  component "Firebase\nAuth + FCM" as FB
}

' Consumo de subsistemas por cada frontend
AC  ..> SS01
AC  ..> SS02
AC  ..> SS04
AC  ..> SS05
AC  ..> SS08
AC  ..> SS09
ACH ..> SS01
ACH ..> SS04
PA  ..> SS01
PA  ..> SS02
PA  ..> SS05
PA  ..> SS06
PA  ..> SS07
PA  ..> SS08
PA  ..> SS09

' Dependencias internas
SS02 ..> SS03
SS03 ..> SS04

' Infraestructura
SS01 ..> FB
SS02 ..> PG
SS05 ..> PG
SS06 ..> PG
SS07 ..> PG
SS08 ..> PG
SS09 ..> PG
SS03 ..> RD
SS04 ..> RD
SS04 ..> FB

@enduml
```

---

## 4. Diagramas de Casos de Uso por Subsistema

Solo se incluyen acá los subsistemas que tienen `include`/`extend` (los demás —SS-01, SS-06, SS-07, SS-08— son CU planos asociados a su actor; podés generarlos con la misma plantilla quitando las flechas punteadas).

### 4.1 SS-02 — Gestión de Pedidos  → `cu-ss02-pedidos.png`

```plantuml
@startuml cu-ss02-pedidos
skinparam dpi 150
left to right direction
skinparam packageStyle rectangle
title SS-02 — Gestión de Pedidos

actor Cliente as C
actor Administrador as A

rectangle "SS-02 Gestión de Pedidos" {
  usecase "Crear Pedido"              as UC005
  usecase "Reservar Stock"            as UCSTK
  usecase "Aplicar Promoción"         as UCPRO
  usecase "Recargo por Transferencia" as UCREC
  usecase "Consultar Detalle"         as UC006
  usecase "Historial de Pedidos"      as UC007
  usecase "Cancelar Pedido"           as UC008
  usecase "Listar Pedidos"            as UC011
}

C -- UC005
C -- UC006
C -- UC007
C -- UC008
A -- UC011

UC005 ..> UCSTK : <<include>>
UCPRO ..> UC005 : <<extend>>\n(cantidad >= umbral)
UCREC ..> UC005 : <<extend>>\n(pago = transferencia)
@enduml
```

### 4.2 SS-03 — Despacho y Asignación  → `cu-ss03-despacho.png`

```plantuml
@startuml cu-ss03-despacho
skinparam dpi 150
left to right direction
title SS-03 — Despacho y Asignación

actor Chofer as CH
actor "Sistema (cron)" as S

rectangle "SS-03 Despacho y Asignación" {
  usecase "Despacho Automático\npor Proximidad" as UC013
  usecase "Reintentar Asignación\n(Cron)"       as UC014
  usecase "Aceptar Pedido"   as UC015
  usecase "Rechazar Pedido"  as UC016
}

S  -- UC013
S  -- UC014
CH -- UC015
CH -- UC016

UC014 ..> UC013 : <<extend>>\n(sin choferes en radio)
@enduml
```

### 4.3 SS-04 — Seguimiento en Tiempo Real  → `cu-ss04-seguimiento.png`

```plantuml
@startuml cu-ss04-seguimiento
skinparam dpi 150
left to right direction
title SS-04 — Seguimiento en Tiempo Real

actor Cliente as C
actor Chofer  as CH

rectangle "SS-04 Seguimiento en Tiempo Real" {
  usecase "Actualizar GPS"        as UC017
  usecase "Marcar En Camino"      as UC018
  usecase "Avisar Llegada"        as UC019
  usecase "Confirmar Entrega"     as UC020
  usecase "Notificar Cliente"     as UCNOT
  usecase "Activar/Desactivar\nDisponibilidad" as UC022
  usecase "Recibir Notificaciones" as UC021
}

CH -- UC017
CH -- UC018
CH -- UC020
CH -- UC022
C  -- UC021

UC018 ..> UCNOT : <<include>>
UC020 ..> UCNOT : <<include>>
UC019 ..> UC018 : <<extend>>\n(chofer cerca)
@enduml
```

### 4.4 SS-05 — Reclamos  → `cu-ss05-reclamos.png`

```plantuml
@startuml cu-ss05-reclamos
skinparam dpi 150
left to right direction
title SS-05 — Reclamos

actor Cliente as C
actor Administrador as A

rectangle "SS-05 Reclamos" {
  usecase "Registrar Reclamo" as UC023
  usecase "Adjuntar Foto"     as UCFOT
  usecase "Listar Reclamos"   as UC024
  usecase "Resolver Reclamo"  as UC025
}

C -- UC023
A -- UC024
A -- UC025

UCFOT ..> UC023 : <<extend>>\n(adjunta evidencia)
@enduml
```

### 4.5 SS-09 — Franjas Horarias  → `cu-ss09-franjas.png`

```plantuml
@startuml cu-ss09-franjas
skinparam dpi 150
left to right direction
title SS-09 — Franjas Horarias

actor Cliente as C
actor Administrador as A

rectangle "SS-09 Franjas Horarias" {
  usecase "Crear Franja"          as UC042
  usecase "Modificar Capacidad"   as UC043
  usecase "Seleccionar Franja"    as UC044
  usecase "Consultar Franjas\nDisponibles" as UC045
}

A -- UC042
A -- UC043
C -- UC044

UC044 ..> UC045 : <<include>>
@enduml
```

---

## 5. Checklist de inserción en los documentos

1. Renderizá cada bloque `@startuml … @enduml` y guardá el PNG con el nombre de la tabla §0.
2. En cada documento, reemplazá el placeholder `> **[ INSERTAR IMAGEN: xxx.png ]**` por:
   ```markdown
   ![Diagrama de Casos de Uso del Sistema](diagrama-cu-sistema.png)
   *Figura X — Diagrama de Casos de Uso del Sistema (SPLG)*
   ```
3. Verificá que el texto de cada CU mencione su relación (ya agregado en Doc 1 §6.4 "Relaciones entre Casos de Uso").

---

## 6. Cómo armar un diagrama de CU desde cero (método, para defenderlo)

1. **Dibujá el límite del sistema:** un rectángulo con el nombre del sistema. Todo lo de adentro es funcionalidad; los actores quedan **afuera**.
2. **Ubicá los actores:** un monigote por cada rol que interactúa (Cliente, Chofer, Admin) **+ actores no humanos** (Sistema/cron, pasarela de pago si aplica). Regla: un actor es algo *externo* que dispara o recibe valor del sistema.
3. **Un óvalo por caso de uso:** nombre en **verbo + sustantivo** ("Crear Pedido", no "Pedido").
4. **Asociaciones actor–CU:** línea sólida del actor al óvalo que inicia.
5. **Factorizá lo repetido con `«include»`:** si el mismo sub-flujo aparece en 2+ CU y es obligatorio, sacalo a un CU aparte y apuntá `base ..> incluido : «include»`.
6. **Modelá lo opcional con `«extend»`:** si un comportamiento ocurre solo bajo condición, hacé un CU aparte y apuntá `opcional ..> base : «extend»` anotando el punto de extensión.
7. **No mezcles `«include»`/`«extend»` con asociaciones de actor:** las punteadas son CU↔CU; las sólidas son actor↔CU.
8. **Mantené granularidad pareja:** un CU debe representar un objetivo completo del actor, no un clic ni un módulo entero.
</content>
</invoke>
