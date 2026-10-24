# Referencias

Material de consulta que no describe a SPLG sino a **lo que hay alrededor**: qué
existe en el mercado y qué se puede aprovechar de otros sistemas propios. Se
revisa cuando hay que justificar una decisión, no en el día a día.

---

## Parte I — Estudio de mercado

Por qué el sistema tiene razón de existir: qué escenario resuelve y contra qué
alternativas compite. Es el respaldo de la justificación del proyecto.

**Materia:** Proyecto de Software (LSI) / Trabajo Final (ASC)  
**Alumno:** Nahuel Wagner

---

### 1. Escenario Identificado

Un distribuidor de gas envasado gestiona actualmente toda su operación de forma completamente analógica. El negocio opera con una flota de choferes propios que realizan entregas a domicilio de garrafas de distintos tamaños (10kg, 15kg y 45kg), atendiendo tanto a clientes residenciales como comerciales.

El flujo actual funciona de la siguiente manera: el cliente llama por teléfono para hacer su pedido, el operador del distribuidor anota el pedido en papel o planilla, coordina verbalmente con el chofer disponible más cercano y le indica la dirección. El chofer no tiene forma de confirmar la entrega más allá de una llamada de vuelta al operador. El stock se descuenta manualmente al final del día, lo que genera inconsistencias frecuentes entre el inventario real y el registrado.

Esta operatoria genera múltiples problemas concretos: los clientes no saben cuándo va a llegar el chofer ni pueden rastrear su pedido, los choferes no tienen una hoja de ruta digital y dependen de instrucciones verbales, el administrador no puede ver en tiempo real cuántas garrafas quedan en stock ni el desempeño de cada chofer, y cuando surge un reclamo por entrega incorrecta o faltante no existe evidencia objetiva para resolverlo.

No existe actualmente ninguna herramienta específica que digitalice la operación completa: desde que el cliente realiza el pedido hasta que el chofer confirma la entrega con evidencia. Las plataformas de delivery genéricas (como Rappi) no son viables por sus comisiones y falta de herramientas de gestión propias, y las soluciones SaaS del rubro (como Custogas) carecen de seguimiento GPS en tiempo real y app para choferes.

---

### 2. Necesidades Específicas a Resolver

1. **Digitalizar la recepción de pedidos** — reemplazar el canal telefónico por una app móvil donde el cliente realice pedidos de forma autónoma, eligiendo producto, cantidad, dirección y franja horaria.
2. **Automatizar la asignación de choferes** — eliminar la coordinación manual asignando automáticamente el repartidor disponible más cercano al domicilio de entrega.
3. **Proveer seguimiento en tiempo real** — permitir al cliente ver la ubicación del chofer en un mapa mientras su pedido está en camino.
4. **Controlar el inventario en tiempo real** — reservar y descontar stock automáticamente al confirmar cada pedido, evitando ventas sin producto disponible.
5. **Centralizar la gestión operativa** — brindar al administrador una herramienta única para gestionar choferes, productos, precios, reclamos y reportes de ventas.

---

### 3. Solución Propuesta

Se propone desarrollar **Delivery Gas**: un sistema software compuesto por una app móvil para clientes (Android/iOS), una app para choferes con GPS en tiempo real, y un panel web administrativo. El backend centraliza la lógica de negocio e implementa un algoritmo de despacho automático por geolocalización.

---

### 4. Estudio de Mercado

Se analizaron dos productos que abordan total o parcialmente las necesidades identificadas en el escenario.

### Alternativa 1 — Rappi

Plataforma de delivery on-demand que incluye entre sus categorías el envío de gas envasado. Permite a los usuarios pedir desde la app, con seguimiento GPS del repartidor y confirmación de entrega.

**Factibilidad técnica:**
- Requiere que el distribuidor se inscriba como comercio aliado (proceso de onboarding con aprobación de Rappi).
- Cobra comisión por cada pedido gestionado (entre 15% y 30% del valor de venta).
- Requiere conexión a internet en el dispositivo del cliente y del repartidor.
- No requiere infraestructura propia — todo corre en los servidores de Rappi.
- No se puede personalizar la lógica de negocio (franjas horarias, promociones por volumen, reglas de cancelación propias).
- Los datos del negocio quedan en servidores de Rappi, sin acceso total por parte del distribuidor.

**Funcionalidades relevantes:**

| Funcionalidad | Disponible |
|---------------|:----------:|
| Pedidos desde app móvil (Android/iOS) | ✅ |
| Seguimiento GPS del repartidor en tiempo real | ✅ |
| Notificaciones push de estado del pedido | ✅ |
| Múltiples métodos de pago | ✅ |
| Historial de pedidos para el cliente | ✅ |
| Franjas horarias de entrega configurables | ❌ |
| Panel de administración propio para el distribuidor | ❌ |
| Gestión de stock del distribuidor | ❌ |
| Módulo de reclamos gestionable por el distribuidor | ❌ |
| Reportes de ventas por chofer o por producto | ❌ |
| Sin comisión por pedido | ❌ |

---

### Alternativa 2 — Custogas

Plataforma argentina especializada en la gestión de distribuidores de gas envasado. Ofrece un sistema de pedidos online y herramientas de gestión para distribuidoras.

**Factibilidad técnica:**
- Requiere suscripción mensual al servicio (modelo SaaS).
- Requiere conexión a internet.
- No requiere infraestructura propia de servidores.
- Personalización limitada a lo que la plataforma permite configurar.
- Los datos del distribuidor residen en los servidores de Custogas.
- No tiene app móvil nativa para choferes con GPS en tiempo real.

**Funcionalidades relevantes:**

| Funcionalidad | Disponible |
|---------------|:----------:|
| Pedidos online para clientes | ✅ |
| Panel de gestión para el distribuidor | ✅ |
| Gestión de productos y precios | ✅ |
| Historial de pedidos | ✅ |
| Seguimiento GPS del repartidor en tiempo real | ❌ |
| App móvil nativa para choferes | ❌ |
| Asignación automática de choferes por proximidad | ❌ |
| Notificaciones push en tiempo real al cliente | ❌ |
| Módulo de reclamos con evidencia fotográfica | ❌ |
| Promociones por volumen automáticas | ❌ |
| Sin suscripción mensual | ❌ |

---

### 5. Matriz de Comparación

| CARACTERÍSTICA | Rappi | Custogas | Delivery Gas (propuesto) |
|----------------|:-----:|:--------:|:------------------------:|
| App móvil para clientes (Android/iOS) | ✅ | ❌ | ✅ |
| Seguimiento GPS del repartidor en tiempo real | ✅ | ❌ | ✅ |
| App móvil para choferes | ✅ | ❌ | ✅ |
| Asignación automática de chofer por proximidad | ✅ | ❌ | ✅ |
| Notificaciones push al cliente | ✅ | ❌ | ✅ |
| Panel de administración propio del distribuidor | ❌ | ✅ | ✅ |
| Gestión de stock en tiempo real | ❌ | ✅ | ✅ |
| Gestión de precios y productos | ❌ | ✅ | ✅ |
| Franjas horarias de entrega configurables | ❌ | ❌ | ✅ |
| Promociones por volumen automáticas | ❌ | ❌ | ✅ |
| Módulo de reclamos con evidencia fotográfica | ❌ | ❌ | ✅ |
| Reportes de ventas por chofer y por producto | ❌ | ❌ | ✅ |
| Sin comisión por pedido | ❌ | ✅ | ✅ |
| Sin suscripción mensual obligatoria | ✅ | ❌ | ✅ |
| Datos propios del distribuidor (no en terceros) | ❌ | ❌ | ✅ |
| Desplegable en servidor propio (on-premise) | ❌ | ❌ | ✅ |

---

### 6. Conclusión

Ninguna de las alternativas estudiadas satisface en forma completa las necesidades específicas del escenario. **Rappi** cubre el aspecto del tracking y la experiencia del cliente, pero impone comisiones por pedido y no entrega control operativo al distribuidor. **Custogas** ofrece herramientas de gestión pero carece completamente del seguimiento GPS en tiempo real y de una app para choferes, que son los elementos centrales de la operación logística.

**Delivery Gas** se propone como solución integral que combina las fortalezas de ambas alternativas — tracking en tiempo real al estilo Rappi, gestión operativa completa al estilo Custogas — agregando funcionalidades específicas no disponibles en el mercado: asignación automática por geolocalización, franjas horarias configurables, promociones por volumen y despliegue en infraestructura propia del distribuidor.

---

## Parte II — Qué se puede traer del backend de Tutu

Análisis del 23/09/2026 sobre `gearthlogic/tutu-dev/backend`.

**Tutu corre el mismo stack que SPLG**: NestJS + TypeORM + PostgreSQL + PostGIS +
Redis + Socket.io, más el cliente oficial de Google Maps. Verificado: cero
`mongoose` en su `package.json`, y `app.module.ts:79` declara `type: 'postgres'`.
Se puede portar tal cual, no hay que traducir nada de la persistencia.

**Pero SPLG ya está por delante en 3 de los 4 temas.** Tiene despacho secuencial
con ofertas durables y TTL, adapter Redis para Socket.io, redlock, idempotencia y
zonas de cobertura con `ST_Contains` scopeadas por distribuidora. Tutu no tiene
nada de eso. La cosecha real es chica y puntual.

### Lo que conviene traer

| Qué | Por qué | Esfuerzo |
|---|---|---|
| Columnas `floor` / `apartment` en `UserAddress` | Hoy el piso y el depto van embutidos en `street` o en `additionalInstructions`, texto libre que nadie puede consultar. En un reparto donde el cliente espera adentro, el piso es dato operativo | Bajo |
| Recargo **porcentual** en la zona, además del fijo | `surcharge` fijo se desactualiza con la inflación y obliga a reeditar zona por zona; un porcentaje no | Bajo |
| `tag` + `color` en la zona | El panel pinta cada zona con metadata del back en vez de inventar la paleta en el front | Bajo |
| `ST_AsGeoJSON(geom)::json` en el SELECT de zonas | Devuelve Features listos para el mapa, sin conversión en el front | Bajo |
| Estado "casi libre" del chofer | Un chofer con la última garrafa del reparto entra al próximo despacho sin esperar el confirm: menos hueco muerto entre pedidos | Bajo |
| **Geocoding y reverse-geocoding** al crear/editar una dirección | **SPLG no tiene geocoding** (verificado: cero dependencias de Google Maps). Hoy el lat/lng entra sin que nadie valide que corresponde a la calle escrita. El chofer llega a la puerta equivocada y el cliente está adentro de la casa | Medio |
| Mandarle al cliente **ETA y distancia** junto con la posición | El que espera la garrafa necesita "llega en 12 minutos", no un punto moviéndose. **Calculado en el servidor y cacheado**, nunca como Tutu (tres llamadas a Google por cada tick de GPS) | Medio |
| Vigencia temporal de la zona | Recargos por zona anegada, corte de calle, feriado. Con cron, no con `node-schedule` en memoria como Tutu, que se pierde al reiniciar | Medio |

### Lo que NO conviene traer

- **Coordenadas como texto.** Tutu guarda `"lat,lng"` en una columna `text` y la parsea con `split(',')`. Tira PostGIS a la basura. **SPLG arrastra una versión suave del mismo problema**: `UserAddress.latitude`/`longitude` son `varchar(50)`. Conviene ir para el otro lado y pasarlas a `geometry(Point,4326)` con índice.
- **Persistir la posición en Postgres en cada ping.** Tutu hace un SELECT + un UPDATE de la fila entera del chofer por cada actualización de GPS. SPLG ya usa Redis GEO, que es lo correcto.
- **Llamar a la Distance Matrix de Google en cada movimiento.** Tres requests por tick, costo lineal en la frecuencia del GPS y en la cantidad de choferes.
- **El registro de clientes conectados en memoria del proceso.** No sobrevive a más de una instancia. SPLG ya lo resolvió con el adapter Redis.
- **Rooms nombradas con un dato que manda el cliente.** Es el agujero que SPLG también tiene; ver abajo.
- **El tarifario doble por "demanda".** Cuenta usuarios conectados en memoria, no es geográfico, y en garrafas con precio regulado no tiene sentido cobrar más porque mucha gente abrió la app.
- **Todo lo atado a origen-destino**: peajes, tarifa por tramos, paradas intermedias, "vuelvo a casa". Un pedido de SPLG tiene un solo domicilio y el cliente no viaja.

### Lo que el análisis destapó en SPLG (no viene de Tutu)

El defecto de las salas por dato del cliente **lo tiene SPLG igual**, y se
verificó contra la API corriendo: ver H-51.
