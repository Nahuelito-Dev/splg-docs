# Modelo de dominio — 24/09/2026

El modelo se rehízo para que contenga los 152 casos de uso y no sólo lo que ya
está construido. Hasta ahora el modelo de datos era la base actual con parches
marcados como "propuesto", sin una organización del negocio detrás, y le
faltaba todo lo que se agregó después: vigencia de zonas, auditoría, historial
de estados, dirección resuelta contra el mapa y lo que necesitan los cuatro
módulos inteligentes.

**Dónde está cada cosa:**

| Artefacto | Archivo | Cómo se actualiza |
|---|---|---|
| Modelo de dominio (UML, Larman) — es el mismo artefacto que el modelo conceptual del Documento 2: vista general y seis vistas por área | `diagramas/modelo-conceptual/MC_*.png/.svg` (fuente en `modelo_conceptual.py`); `drawio/SPLG-MC.drawio` | `python3 generar-modelo-conceptual.py`, y `python3 generar-drawio.py` para el `.drawio` |
| Modelo entidad-relación conceptual — no confundir con el anterior: éste es del diseño de la base y usa la misma nomenclatura que el modelo conceptual | `diagramas/base-de-datos/conceptual/SPLG-der-*.png/.svg` | `python3 generar-modelo-datos.py` |
| Modelo físico, una lámina por contexto | `diagramas/base-de-datos/fisico/SPLG-fisico-*.png/.svg` | ídem |
| SQL de lo propuesto | `diagramas/base-de-datos/SPLG-base-de-datos-propuesta.sql` | ídem |
| Diccionario de datos | `diagramas/base-de-datos/SPLG-modelo-de-datos.md` | ídem |

Lo implementado sale de la base en ejecución; lo propuesto, de la constante
`PROPUESTO` del generador. Así ningún diagrama puede mostrar como hecho algo que
no está en la base.

---

## 1. Los números

> **Implementado el 25/09/2026.** Las 17 tablas y 26 columnas propuestas están
> en la base (migración `ModeloPropuesto`), las 13 relaciones sin clave foránea
> se declararon, y la normalización sumó `gas_cylinder_promotion`. Un script
> comparó el esquema contra la especificación columna por columna: 0
> diferencias.

| | Tablas | Columnas nuevas | Claves foráneas | Tipos enumerados |
|---|---:|---:|---:|---:|
| Antes (24/09) | 20 | — | 30 declaradas + 13 sin declarar | 16 |
| Agregado el 25/09 | 17 del modelo + 1 de la normalización | 26 en tablas existentes | 41 nuevas + las 13 declaradas | 17 |
| **25/09, en la base** | **38** | | **84, todas declaradas** | **33** |

> Este cuadro describe el cambio del 24/09 al 25/09. Migraciones posteriores agregaron
> `maintenance_task_attachment`, `vehicle_assignment` y columnas de zona de cobertura y de pedido; el total
> actual es 46 tablas, 101 claves foráneas y 35 tipos enumerados, todas declaradas —
> ver `diagramas/base-de-datos/SPLG-modelo-de-datos.md`, que se regenera desde la base
> en ejecución y nunca queda desactualizado.

## 2. Ocho contextos

Cada entidad pertenece a un contexto, que es el área del negocio que la define y
la modifica. El contexto es el que después dice qué módulo del backend es dueño
de la tabla (convención 4: cada módulo es dueño de sus entidades).

| Contexto | Entidades | Módulos del backend |
|---|---|---|
| Organización y acceso | Distribuidora, Usuario, Rol, Administrador, Configuración de módulo*, Asiento de auditoría* | `distributor`, `users`, `role`, `admin`, `auth` |
| Clientes | Cliente, Dirección de entrega, Invitación de recompra*, Ítem sugerido‡ | `customer`, `user-address` |
| Catálogo e inventario de envases | Producto, Promoción, Envase, Movimiento de envase, Revisión de envase*, Caso de recupero*, Aviso de recupero* | `gascylinder`, `cylinder` |
| Venta y pedidos | Carrito*, Ítem del carrito*, Pedido, Ítem del pedido, Cambio de estado*, Cambio de dirección*, Zona de cobertura, Franja horaria | `order`, `coverage-zone`, `time-slot` |
| Pagos | Pago | `payments` |
| Despacho y logística | Oferta de despacho, Lote de recorrido*, Parada del lote*, Oferta de lote* | `order` (despacho) |
| Flota y choferes | Chofer, Vehículo, Plan de mantenimiento*, Tarea de mantenimiento*, Adjunto de tarea de mantenimiento*, Propuesta de ventana de taller*, Registro de uso del vehículo* | `delivery`, `car`, `fleet` |
| Posventa | Reclamo, Incidencia, Calificación | `claims`, `incident`, `rating` |

\* agregado el 25/09 (antes figuraba como propuesto). ‡ agregado el 30/09, al verificar el
modelo contra la base (asociación ItemSugerido–Producto y el adjunto de las tareas de
mantenimiento, que ya existían en el código pero no en este documento).

**Casi toda entidad pertenece a una distribuidora** (el sistema es
multi-tenant). En el diagrama conceptual esa relación se declara una vez en la
leyenda y no se dibuja desde cada entidad: con las líneas, el diagrama era
ilegible. Las excepciones son Usuario, Cliente y Dirección: un cliente le compra
a varias distribuidoras, así que no pertenece a ninguna; para una distribuidora,
"sus" clientes son los que le compraron (`common/tenancy/pertenencia.ts`). Lo de
otra distribuidora responde 404 (H-77 a H-84).

## 3. El patrón que atraviesa los módulos inteligentes

Los cuatro módulos inteligentes hacen lo mismo con objetos distintos: **le
proponen algo a alguien, con una vigencia, y esperan que lo acepte, lo rechace o
lo deje vencer.** Si lo rechaza o vence, pasan a la alternativa siguiente.

La numeración de los módulos es la de `3-Diseño.md` §6, que es la que se entrega: M1 es
el despacho automático que ya existía antes del 24/09.

| Propuesta | A quién | Módulo |
|---|---|---|
| Oferta de despacho | Chofer | M1 — Despacho automático (ya existía, CU-013) |
| Propuesta de ventana de taller | Chofer | M2 — CU-105 |
| Invitación de recompra | Cliente | M3 — CU-106 |
| Oferta de lote | Chofer | M4 — CU-107 |
| Aviso de recupero (oferta de retiro) | Cliente | M5 — CU-108 |

En el modelo de dominio es una clase abstracta, **Propuesta con vigencia**
(estado + vencimiento), de la que heredan las cinco. En la base cada una tiene
su tabla, porque apuntan a cosas distintas, pero todas comparten el mismo ciclo
de estados (`proposal_status_enum`: pendiente, aceptada, rechazada, vencida).

Es un argumento para la defensa: los módulos inteligentes no son cuatro
piezas sueltas, son cuatro aplicaciones de un mismo mecanismo que el sistema ya
tenía probado en el despacho.

## 4. Decisiones, con su porqué

### Flota: una sola abstracción para mantenimiento y habilitaciones

La propuesta anterior ponía seguro y VTV como columnas de `car`, la licencia
como columnas de `delivery`, y los mantenimientos en una tabla aparte. Se
reemplaza por **Plan** (la regla) y **Tarea** (cada vencimiento), que es lo que
especifica M1:

- El seguro es un plan de fecha fija que **bloquea** el vehículo al vencer.
- El cambio de aceite es un plan por kilómetros que **no bloquea**.
- La licencia es un plan de fecha fija que bloquea, pero es **del chofer**: por
  eso la tarea apunta a un vehículo o a un chofer.

Con columnas sueltas no había dónde guardar la regla (cada cuánto, con qué
anticipación, si inhabilita), y sin la regla M1 no puede proyectar nada.
CU-136 a CU-141 se cumplen igual: cargar un seguro es crear la tarea de ese plan
con la aseguradora, la póliza y el vencimiento.

### Historial de estados del pedido

Decidido el 23/09. Hoy el pedido guarda el estado actual y algunas marcas de
tiempo (`acceptedAt`, `onTheWayAt`, `deliveredAt`), pero no quién hizo cada
cambio ni por qué. Las marcas se conservan porque los listados las leen sin unir
tablas; el historial es la fuente de la verdad.

### Auditoría

CU-152 y CU-153. Una tabla de sólo escritura: no hay modificación ni baja para
ningún rol. Si se borra el usuario o la distribuidora, las referencias quedan
vacías pero el asiento no se pierde. Necesita índices por fecha, por autor y por
distribuidora desde el primer día.

### Las 13 relaciones sin clave foránea se declaran

Columnas que el código usa como referencia pero la base nunca validó: el pago
apunta a un pedido que podría no existir, el movimiento de envase a un envase
que podría no existir. Hoy **no hay filas huérfanas**, así que se pueden
declarar sin limpiar datos. Dos reglas de borrado cambian respecto de lo que se
había propuesto: **pago → pedido** y **movimiento → envase** pasan de `CASCADE`
a `RESTRICT`. Son registro contable y de trazabilidad: borrar un pedido no puede
llevarse sus pagos.

### Coordenadas en PostGIS

`user_address.latitude` y `longitude` son `varchar` y no se pueden indexar ni
consultar por cercanía. Se agrega `location geography(Point)`. Las dos columnas
viejas se conservan hasta que las apps dejen de mandarlas.

### Entrega express sin redundancia

La propuesta anterior tenía `delivery_mode` y además `is_express`, que repetía
lo mismo. Queda sólo `delivery_mode`: con una columna no hay forma de que las
dos digan cosas distintas.

### Configuración de los procesos automáticos

La cátedra exige que un proceso automático sea configurable desde el sistema.
Cada proceso —los cuatro módulos inteligentes y el despacho express, que
necesita su recargo, su radio y la vigencia de su oferta— guarda sus parámetros
en un JSON por distribuidora, validado por el DTO del proceso. Una tabla por
proceso sería una tabla de una sola fila con columnas que no se parecen entre
sí.

## 5. Lo que queda abierto

- **Reembolso al cancelar (regla del 90%, 23/09):** no está en el modelo porque
  CU-008 todavía no lo especifica. Cuando se escriba, suma una entidad
  `Reembolso` en el contexto de Pagos.
- **Comienzo de vigencia de una zona:** CU-150 lo deja como decisión pendiente.
  El modelo tiene sólo el fin.
- **Los dos modelos de inventario** (`gas_cylinder.stock` numérico y `cylinder`
  por unidad) siguen conviviendo. Es una decisión de MVP documentada; unificarlos
  no lo pide ningún caso de uso.
- ~~Promociones siguen como JSON dentro de `gas_cylinder`~~ — resuelto: la
  normalización del 25/09 sumó `gas_cylinder_promotion` como tabla propia, con
  sus `CHECK` de cantidad y descuento. Este punto queda cerrado.

## 6. Qué cambia en el resto de la documentación

- **Casos de uso, especificaciones y DSS: nada.** Describen qué hace el sistema,
  y el modelo nuevo no cambia ningún comportamiento especificado: los agrega.
- ~~Diagrama de clases de dominio (`3-Diseño.md` §5.1): tiene que tomar los
  contextos y la Propuesta con vigencia~~ — resuelto: §5.1 se deriva de los DSD y del
  modelo conceptual (`material-de-trabajo/generar-clases-diseno.py`), dibuja
  todas las clases del modelo conceptual, con la generalización de
  `PropuestaConVigencia` como clase abstracta, y sus operaciones salen de los
  mensajes que reciben en los DSD. La correspondencia con las clases del
  código (`Order`, `DispatchOffer`…) queda en las tablas de implementación de
  cada DSD y en §5.6.
- **DSD:** cambian los que nombran clases que se mueven o se parten. Es el punto
  12 de la lista de módulo terminado (`splg-app-backend/CONVENCIONES.md`).
