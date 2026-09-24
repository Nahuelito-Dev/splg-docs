# Base de datos

Dos cosas en un solo lugar: **en qué estado está el esquema** frente a las formas
normales, y **cómo se lo modifica** sin romper nada.

---

## Parte I — Normalización: qué cumple y qué no

Auditoría de las 21 tablas del dominio contra las formas normales. Todo lo que
dice está verificado **contra los datos reales** de la base, no deducido del
modelo: donde se afirma que algo está duplicado o derivado, se muestra en cuántas
filas.

---

## Resumen

| Forma normal | Estado |
|---|---|
| **1FN** — atomicidad, sin grupos repetitivos | **No se cumple en 3 columnas** |
| **2FN** — sin dependencias parciales | **Se cumple** por construcción |
| **3FN** — sin dependencias transitivas | **No se cumple en 3 lugares** |
| **BCNF** | Se cumple donde se cumple 3FN |
| **4FN / 5FN** | Sin dependencias multivaluadas ni de join detectadas |

La 2FN se cumple sola: **todas las claves primarias son de una sola columna**
(UUID). Sin claves compuestas no puede haber dependencias parciales.

---

## 1FN — lo que no es atómico

### 1. Las coordenadas están modeladas de tres formas distintas

El mismo concepto —un punto en el mapa— se guarda de tres maneras en la misma
base de datos:

| Dónde | Cómo | Atómico |
|---|---|---|
| `user_address` | `latitude` y `longitude`, dos columnas `varchar` | Sí, pero como texto |
| `customer.lat_lang` | **una** columna `text`: `"-27.3671,-55.8961"` | **No** |
| `delivery.latLng` | **una** columna `text`: `"-27.3671,-55.8961"` | **No** |
| `order.deliveryLatitude` / `deliveryLongitude` | dos columnas `varchar` | Sí, pero como texto |
| `coverage_zone.area` | geometría **PostGIS** | Sí, y es el modelo correcto |

Las dos del medio violan la 1FN: hay dos valores en una celda. No se pueden
indexar, ni comparar, ni usar para buscar por cercanía sin partir el texto en
cada consulta.

Lo llamativo es que **el modelo correcto ya está en uso en esta misma base**:
`coverage_zone.area` es una geometría PostGIS, y la extensión está instalada.
Se usa para resolver si una dirección entra en una zona.

**Qué haría:** `geography(Point,4326)` en las cuatro. Permite indexar con GiST,
calcular distancias de verdad y se acabó el partir strings. Es además lo que
necesita el despacho por proximidad, que hoy resuelve las distancias a mano.

### 2. `gas_cylinder.promotions` es un grupo repetitivo

```json
[{"quantity": 2, "discountPercentage": 5}, {"quantity": 4, "discountPercentage": 12}]
```

Un arreglo JSON dentro de una celda: es exactamente lo que la 1FN prohíbe.
Consecuencias concretas:

- No se puede exigir que no haya dos promociones para la misma cantidad.
- No se puede responder "qué productos tienen promoción a partir de 3 unidades"
  sin recorrer el JSON de todas las filas.
- No hay forma de fechar una promoción (desde cuándo, hasta cuándo) sin
  reescribir el JSON entero.
- No se puede saber qué promoción se aplicó a un pedido pasado.

**Qué haría:** una tabla `promocion_producto` con
`(gas_cylinder_id, cantidad_minima, descuento_porcentaje, vigente_desde,
vigente_hasta)` y un `UNIQUE (gas_cylinder_id, cantidad_minima)`.

### 3. `payment.metadata` (jsonb) — **aceptable**

Guarda la respuesta cruda de la pasarela. No es una violación: es un documento
opaco de un tercero, cuyo esquema no controlamos y que sirve para auditar. Lo
que sí conviene es no leer campos de adentro para tomar decisiones de negocio.

---

## 3FN — dependencias transitivas

### 4. El estado del pago está guardado dos veces, con dos vocabularios

`order` tiene `paymentStatus`, `paymentMethod` y `paymentType`. `payment` tiene
`status`, `method` y `gateway`. Sobre los 57 pedidos que tienen pago registrado:

```
order.paymentStatus distinto de payment.status  ->  49 de 57
order.paymentMethod distinto de payment.method  ->  57 de 57
```

Pero no están desincronizados: son **dos vocabularios para el mismo hecho**.

| En el pedido | En el pago | Filas |
|---|---|---|
| `paid` | `approved` | 44 |
| `pending` | `pending` | 8 |
| `failed` | `rejected` | 5 |

Es peor que una duplicación común: para comparar los dos campos hace falta una
tabla de traducción que no existe en ningún lado, y **nada garantiza que un
webhook que actualiza uno actualice el otro**.

**Qué haría:** que el estado del pago viva sólo en `payment`. Si el pedido
necesita consultarlo seguido, una vista o una columna calculada, pero **una sola
fuente de verdad y un solo vocabulario**.

### 5. `order_item.subtotal` es una columna derivada

Verificado: `subtotal = quantity × unitPrice` en **411 de 411 filas**. Es una
dependencia funcional entre atributos que no son clave, que es justo lo que la
3FN busca eliminar.

`unitPrice`, en cambio, **no es una violación**: es el precio al momento de la
compra, un dato histórico que no se puede derivar del producto actual. Tiene que
quedarse.

**Qué haría:** columna generada
(`GENERATED ALWAYS AS (quantity * "unitPrice") STORED`). Se sigue leyendo igual,
se sigue indexando, y deja de poder quedar mal.

### 6. `order.deliveryLatitude` / `deliveryLongitude` dependen de `address_id`

El pedido ya guarda `address_id`, y la dirección tiene sus coordenadas: las del
pedido se pueden derivar. **Puede ser deliberado** —una foto del punto de
entrega al momento del pedido, para que no cambie si el cliente después edita la
dirección— y en ese caso está bien.

Pero si es eso, hoy está a medias: se fotografían las coordenadas y **no el
resto de la dirección** (calle, ciudad). Si el cliente edita la calle, el pedido
histórico muestra la calle nueva con las coordenadas viejas.

**Qué haría:** decidirlo explícitamente. O se deriva de la dirección, o se
fotografía la dirección **completa** en el pedido.

---

## Lo que no es normalización pero sale del mismo análisis

### 7. Reglas de negocio que el código promete y la base no garantiza

El código valida antes de insertar, pero **no hay restricción `UNIQUE`** que lo
respalde. Es un *leer y después escribir* que pierde las carreras. Verificado en
los datos de hoy:

| Regla que el código dice garantizar | Duplicados existentes |
|---|---:|
| Un tipo de garrafa por distribuidora | **1** (`Garrafa 5kg` dos veces) |
| Una franja horaria por nombre y distribuidora | **1** (`Mañana` dos veces) |

No es teórico: la base **ya tiene** los duplicados que el código decía impedir.

**Qué haría:** `UNIQUE (distributor_id, type)` en `gas_cylinder` y
`UNIQUE (distributor_id, name)` en `time_slot` y `coverage_zone`. La base es el
único lugar donde una regla de unicidad se cumple siempre.

Faltaría también un índice parcial
`UNIQUE (user_id) WHERE "isDefault"` en `user_address`, para que un usuario no
pueda tener dos direcciones por defecto. Hoy no hay ninguna, pero nada lo impide.

### 8. Marcas de tiempo con y sin zona horaria en la misma tabla

En `order`:

```
timestamp with time zone     -> createdAt, updatedAt
timestamp without time zone  -> acceptedAt, onTheWayAt, deliveredAt
```

Restar una de otra para medir cuánto tardó una entrega da un resultado corrido
por el desfasaje horario. En Argentina son tres horas.

**Qué haría:** `timestamptz` en las cinco. Es una migración de una línea por
columna y elimina una familia entera de errores silenciosos.

### 9. Los estados del pedido son columnas, no historia

`acceptedAt`, `onTheWayAt`, `deliveredAt`: una columna por transición. Funciona,
pero agregar un estado nuevo obliga a migrar el esquema, no se puede saber quién
hizo cada cambio, y un pedido que vuelve a `pending` —como pasa cuando el chofer
lo libera— deja las marcas viejas cargadas sin que nada las limpie.

**Qué haría:** una tabla `orden_historial_estado`
(`order_id, estado, ocurrido_en, actor_user_id, motivo`). Las columnas actuales
se pueden mantener como caché mientras se migra.

---

## En qué orden

| # | Qué | Cuesta | Rinde |
|---|---|---|---|
| 1 | Los `UNIQUE` que faltan (punto 7) | Una migración | Corta duplicados que **ya están pasando** |
| 2 | `timestamptz` en las cinco columnas (punto 8) | Una migración | Elimina errores de cálculo silenciosos |
| 3 | `subtotal` como columna generada (punto 5) | Una migración | No puede volver a quedar mal |
| 4 | Un solo vocabulario para el estado del pago (punto 4) | Migración + código | Una sola fuente de verdad |
| 5 | Coordenadas a `geography(Point)` (punto 1) | Migración + código | Habilita el despacho por proximidad de verdad |
| 6 | Promociones a su propia tabla (punto 2) | Migración + código | Permite fechar y auditar promociones |
| 7 | Historial de estados (punto 9) | Tabla nueva | Trazabilidad |

Los tres primeros son migraciones sin tocar código y se pueden hacer ya.


---

## Parte II — Cómo se cambia el esquema

Todo lo que propone la Parte I se ejecuta por acá. Ninguna de esas correcciones
se aplica a mano sobre la base: cada una es una migración revisada y commiteada
junto con el cambio de entidad que la motiva.

El esquema se gestiona con **migraciones** — son la fuente de verdad, en todos
los ambientes. `synchronize` está en **false** por defecto (en dev se puede
optar por `DB_SYNC=true` para iterar rápido, nunca en prod).

### Comandos

```bash
# Generar una migración con el diff entre las entidades y la DB actual
npm run migration:generate -- src/migrations/NombreDescriptivo

# Aplicar las migraciones pendientes
npm run migration:run

# Revertir la última
npm run migration:revert

# Ver estado
npm run migration:show
```

La config del CLI vive en `src/data-source.ts` (lee el `.env`). En runtime la app
usa la config de `app.module.ts`.

### Flujo de trabajo

1. Cambiás una entidad (columna, índice, relación).
2. `npm run migration:generate -- src/migrations/LoQueHiciste`.
3. **Revisás** el archivo generado (que no tenga DROPs inesperados por drift).
4. `npm run migration:run` para aplicarla.
5. Commiteás la migración junto con el cambio de entidad.

### La migración inicial

Desde el 24/09/2026 el repo tiene **una sola migración de partida**,
`1790281980739-InitialSchema`, con el esquema completo: 20 tablas, 16 tipos
enumerados, 38 índices y 30 claves foráneas, más las extensiones `uuid-ossp` y
`postgis`. Se generó desde las entidades contra una base vacía.

Reemplazó a las tres migraciones anteriores (`AddHotIndexes`,
`DistributorIdNotNull` y `OrderCustomerRestrictOnDelete`), que suponían las
tablas ya creadas por `synchronize` y no servían para una base nueva. Lo que
hacían quedó incluido en la inicial.

**Cómo se verificó:** una base vacía, sin extensiones, con `migration:run` y nada
más, quedó con un esquema idéntico al de desarrollo (el `pg_dump` de los dos da
las mismas 506 líneas). La migración se revierte y se vuelve a aplicar sin
errores, y la app arranca contra esa base.

**Una base nueva** se crea así, sin pasos manuales:

```bash
npm run migration:run
```

**Una base que ya tenía las tres migraciones viejas** tiene el esquema, pero no
el registro. Hay que anotarle la inicial como aplicada, una sola vez:

```sql
DELETE FROM migrations WHERE name IN ('AddHotIndexes1784228702584',
  'DistributorIdNotNull1784234639090', 'OrderCustomerRestrictOnDelete1784236103204');
INSERT INTO migrations(timestamp, name) VALUES (1790281980739, 'InitialSchema1790281980739');
```

Así se hizo con la base de desarrollo (`splg_db`).
