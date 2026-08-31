# Revisión de Módulos Inteligentes contra los lineamientos de la cátedra

> Revisión de los **3 módulos inteligentes presentados a la cátedra** contra sus
> criterios, más la evaluación de los demás procesos del sistema como posibles
> reemplazos. Verificado contra el código, no contra la documentación.
>
> **Presentados a la cátedra:** despacho por proximidad, reintento con radio
> expandido, y reserva y restitución atómica de stock. El resto de los procesos
> de Doc 2 §3 son módulos del sistema, no se presentaron como inteligentes.
>
> Fecha: 2026-08-27.

---

## 1. Criterios aplicados

| # | Criterio | Enunciado de la cátedra |
|---|---|---|
| **C1** | Valor agregado | Automatiza un flujo que genera ganancias o reduce costos de forma automática |
| **C2** | No intrínseco al PMV | No puede ser algo que el sistema tendría que hacer sí o sí para funcionar |
| **C3** | Más que una consulta SQL | Un módulo que termina siendo un `SELECT ... ORDER BY` no es un módulo inteligente |
| **C4** | Parametrizable | Debe poder configurarse desde el sistema (como mínimo, cuándo se ejecuta) |
| **C5** | Decisión onerosa humana | Las decisiones que comprometen dinero las asume una persona |

### El patrón de los ejemplos

Los tres ejemplos de la cátedra (reagendado de turnos, presupuestos a
proveedores, lista de espera de biblioteca) comparten una misma forma:
**recorrer una lista secuencialmente, ofrecer algo con vigencia limitada,
esperar respuesta, pasar al siguiente ante rechazo o timeout, y cerrar con una
decisión humana cuando hay dinero de por medio.**

No premian el cálculo. Premian el **flujo de interacción**. Es el criterio que
más discrimina y el que hay que usar para decidir.

---

## 2. Hallazgo transversal: los módulos actuales no son parametrizables

`src/order/application/dispatch-orchestrator.service.ts`:

```typescript
static readonly OFFER_TTL_SECONDS = 30;
private static readonly RADIUS_STEPS_KM = [5, 10, 15, 20];
```

Son constantes de clase. Ni el TTL de la oferta ni los pasos de radio se pueden
configurar desde el sistema, por lo que **M1 y M2 incumplen C4 tal como están**.

**Acción requerida:** mover ambos a configuración por distribuidora (tabla de
parámetros o columna en `distributor`), editable desde el panel admin.

---

## 3. Resultado de la revisión

### 3.0 Los tres presentados

| # | Módulo | C1 | C2 | C3 | C4 | Veredicto |
|---|---|:--:|:--:|:--:|:--:|---|
| 1 | Despacho automático por proximidad | ✅ | ⚠️ | ✅ | ❌ | Se sostiene con reparos |
| 2 | Reintento con radio expandido | ✅ | ⚠️ | ✅ | ❌ | Se sostiene, pero es el mismo pipeline que el 1 |
| 3 | Reserva y restitución atómica de stock | ⚠️ | ❌ | ❌ | — | **Se cae** |

El tercero hay que reemplazarlo. Los dos primeros incumplen C4 tal como están
(ver §2) y su C2 es zona gris que hay que argumentar, no dar por obvia.


### 3.0.1 El riesgo de C2 alcanza a los tres, no solo al tercero

La revisión externa marcó únicamente la reserva de stock, pero el criterio C2
—*"no puede ser algo que sí o sí tendría que hacer el sistema de todas formas
para funcionar normalmente"*— tiene la misma forma en los tres. El paralelo con
el ejemplo del comedor de la cátedra es directo:

> *"Es inaceptable que manualmente haya que decrementar los stocks en un sistema
> de comedor después de cada comida"*

- Es inaceptable que el operador **asigne a mano cada pedido a un chofer** → módulo 1
- Es inaceptable que el operador **reintente a mano** cuando nadie aceptó → módulo 2
- Es inaceptable que alguien **descuente el stock a mano** → módulo 3

**No están los tres igual de expuestos:**

- **El 3 no tiene defensa.** Es una transacción ACID.
- **El 1 y el 2 sí la tienen, pero solo presentados juntos.** El despacho
  secuencial (ofrecer al más cercano → esperar 30 s → si no responde, ofrecer al
  siguiente → ampliar el radio) **es el ejemplo de la lista de espera de la
  biblioteca**, con choferes en vez de lectores. Ese patrón la cátedra ya lo
  aprobó por escrito.

Separados es donde quedan débiles: el 1 aislado es "consulta Redis y notifica",
y el 2 aislado es "un cron que reintenta".

**Argumento de PMV disponible:** el relevamiento del roadmap (Bloque D) registra
que las distribuidoras de garrafas hoy operan por teléfono. El mínimo viable es
el operador asignando; la negociación automática secuencial es el valor
agregado. El argumento se sostiene con datos propios del trabajo.

**Consecuencia práctica:** conviene llevar **tres candidatos de reemplazo**, no
uno. Si además se objeta el módulo fusionado por C2, hace falta un tercero
disponible. Candidatos: mantenimiento predictivo de flota, recompra predictiva y
batching de pedidos por chofer.

### 3.1 Ningún proceso existente sirve como reemplazo

Se evaluaron los demás procesos automáticos del sistema (Doc 2 §3) por si alguno
podía ascender a la terna para cubrir el hueco del tercero. **Ninguno llega**, y
todos por el mismo criterio: C3.

| # | Proceso | Criterios que falla | Fundamento (código) |
|---|---|---|---|
| 3 | Reserva atómica de stock | C2, C3 | `stock-reservation.service.ts` — 80 líneas: lock, resta, guarda. Es atomicidad ACID. Y descontar stock automáticamente es intrínseco |
| 4 | Restitución de stock | C2, C3 | Misma clase, método `restore()`. La política de cancelación es un árbol de `if` |
| 5 | Actualización de estado de pago | C2, C3 | Un `UPDATE` de estado al confirmar entrega. Marcar cada pago a mano es inaceptable |
| 6 | Notificaciones WebSocket | C2, C3 | Es un `emit`. Sin esto no existe el producto de tracking |
| 7 | Notificaciones FCM | C3 | Es enviar un mensaje a un dispositivo |
| 8 | Limpieza del radar GPS | C2, C3 | Un `ZREM` en Redis. Fue **P0-4 de la revisión de arquitectura**: era un bug (choferes fantasma), no una funcionalidad |
| 9 | Promociones por volumen | C3 | `order-pricing.service.ts` — `sort()` por umbral + `find()`. Es el contraejemplo textual de la cátedra |
| 10 | Recargo por método de pago | C3 | Un `if` sobre el método y una multiplicación por 1.1 |

Todos son módulos del sistema correctamente implementados: cumplen su función y
están bien resueltos. Simplemente **no son candidatos a módulo inteligente**, y
por eso el reemplazo del tercero tiene que ser algo nuevo.

### 3.2 Los dos que se sostienen: qué hay que hacerles

Tres acciones para que el despacho quede sólido:

1. **Unificar 1 y 2 en un solo módulo.** Separados, uno queda en "hacer un
   GEORADIUS" y el otro en "un cron". Juntos son un flujo de oferta secuencial
   con timeout y relajación progresiva de restricción — el patrón de la lista de
   espera de biblioteca.
2. **Parametrizar radios y TTL** (ver §2). Es el incumplimiento más concreto y
   afecta a los dos módulos que sí presentaste.
3. **Argumentar C2 explícitamente**: el PMV sería la asignación manual por un
   operador; la automatización con oferta secuencial y radio progresivo es el
   valor agregado. Es zona gris y hay que defenderla, no darla por obvia.

### 3.3 Procesos automatizados legítimos, pero no módulos inteligentes

Tres crons en `reservation.service.ts` que **no figuran en la documentación**:

| Proceso | Frecuencia | C1 | C2 | C3 | C4 |
|---|---|:--:|:--:|:--:|:--:|
| `activateDueReservations()` | 5 min | ✅ | ✅ | ⚠️ | ✅ |
| `expireUnpaidReservations()` | 1 hora | ✅ | ✅ | ⚠️ | ✅ |
| `expireUnpaidMercadoPagoOrders()` | 30 min | ✅ | ✅ | ⚠️ | ✅ |

Tienen disparador temporal propio y `depositTtlHours` ya es configurable. Pero
son **barridos de estado**: select, transición, update. No hay flujo de
interacción, por lo que no llegan a C3.

**Van a la tabla de procesos automatizados, no a la de módulos inteligentes.**
Suman al trabajo sin exponerse a objeción.

---

## 4. Procesos automatizados vs. módulos inteligentes

La separación ya está bien planteada: a la cátedra se presentaron 3 módulos
inteligentes, y el resto de Doc 2 §3 son módulos del sistema. Lo único a ajustar
es la tabla de procesos automatizados, que debe llevar las cinco columnas de la
consigna e incorporar los 3 crons hoy sin documentar.

| Categoría | Qué incluye | Dónde va |
|---|---|---|
| **Procesos automatizados** | Todo lo que corre solo, incluidos los 3 crons sin documentar | Tabla en Doc 2, con las 5 columnas que pide la consigna |
| **Módulos inteligentes** | Solo los que pasan los 5 criterios | Doc 3 §6, especificados en profundidad |

Lo técnicamente valioso de la reserva de stock (lock pesimista, prevención de
oversell, carrera pago-vs-expiración del webhook de MercadoPago) se reubica en
el capítulo de arquitectura/calidad como *mecanismo de integridad
transaccional*, donde el criterio de evaluación es "¿está bien resuelto?" — y lo
está.

---

## 5. Dos caminos posibles

Como a la cátedra se presentaron **tres** módulos, unificar el 1 y el 2 abre un
lugar en vez de cerrarlo. De ahí salen dos opciones:

### Opción A — mínima: reemplazar solo el tercero

| | Módulo | Estado |
|---|---|---|
| 1 | Despacho automático por proximidad | Existe (parametrizar) |
| 2 | Reintento con radio expandido | Existe (parametrizar) |
| 3 | **Mantenimiento predictivo de flota** | A construir |

**Un módulo nuevo.** Menos trabajo. Contra: 1 y 2 siguen siendo el mismo
pipeline presentado como dos, y el 2 queda expuesto al mismo tipo de objeción
que ya recibió el 3.

### Opción B — sólida: unificar 1+2 y sumar dos

| | Módulo | Patrón de la cátedra | Aporta | Estado |
|---|---|---|---|---|
| **A** | Despacho secuencial (1+2 unificados) | Lista de espera de biblioteca | Opera el presente | Existe (unificar + parametrizar) |
| **B** | Mantenimiento predictivo de flota | Reagendado + presupuestos | Protege el activo (**costos**) | A construir |
| **C** | Recompra predictiva | Reagendado de turnos | Genera demanda (**ingresos**) | A construir |

**Dos módulos nuevos.** Más trabajo, pero cada uno cubre una naturaleza distinta
y ninguno queda con flanco débil. Uno opera, uno cuida los costos, uno genera
ingresos.

**Recomendación:** la B si el tiempo lo permite. La A es defendible, pero deja
al 2 expuesto y conviene no pasar dos veces por esta discusión.

**Suplente en cualquiera de los dos casos:** batching de pedidos por chofer (D1
del roadmap). Pasa los cuatro criterios pero carece del flujo de interacción
secuencial que premian los ejemplos. Reservarlo por si se objeta el despacho
por C2.

### Detalle de B y C

- **B — Mantenimiento predictivo de flota:** especificado en
  `M3-Mantenimiento-Predictivo-Flota.md`. La etapa ③bis (negociación secuencial
  de la ventana de taller con el chofer, con vigencia y escalamiento al admin)
  es la que le da la forma de flujo que exige C3.

- **C — Recompra predictiva (D4 del roadmap):** estimar cuándo se le agota el
  gas a cada cliente a partir de su historial de compras y ofrecerle recomprar
  antes de que se quede sin gas, con oferta de vigencia limitada.
  - **C1:** genera ingresos directos y fideliza; se adelanta a la competencia en
    consumo recurrente.
  - **C2:** el sistema vende igual sin esto.
  - **C3:** estimación de consumo por cliente + campaña secuencial + procesamiento
    de respuesta + conversión en pedido. Es el análogo del reagendado de turnos:
    el sistema sale a buscar ingreso que de otro modo se pierde.
  - **C4:** umbral de anticipación, vigencia de la oferta, canal, frecuencia máxima
    por cliente.
  - Combina con D2 (canal WhatsApp) del roadmap.

---

## 6. Nota sobre integración con terceros

El último lineamiento admite explícitamente la **integración con tecnología de
terceros** como proceso automatizado, y nombra MercadoPago, autenticación con
Google y APIs de resolución de rutas de transporte — con la salvedad de
**consultarlo con la cátedra**.

Conviene preguntar antes de descartar la pasarela de pagos: puede acreditar, y
el sistema ya la tiene implementada con webhook idempotente.

---

## 7. Acciones pendientes

1. Renombrar la tabla de Doc 2 §3 a **procesos automatizados** y agregarle las
   cinco columnas de la consigna (tiempos, grado de automatización, disparadores,
   resultados esperados, impacto en registros).
2. Incorporar los 3 crons sin documentar a esa tabla.
3. Corregir las discrepancias entre documentación y código (ver §8).
4. Parametrizar `OFFER_TTL_SECONDS` y `RADIUS_STEPS_KM`.
5. Decidir entre Opción A y Opción B (§5).
6. Si va la Opción B: unificar M1+M2 en Doc 3 §6 y especificar los dos módulos
   nuevos con ese formato. Si va la A: especificar solo el de flota.
7. Consultar a la cátedra por la integración con terceros.

---

## 8. Discrepancias entre la documentación y el código

Verificadas contra el código. **Ninguno de los cuatro datos numéricos de la
tabla actual coincide con la implementación:**

| La documentación dice | El código hace |
|---|---|
| Radio "5 → 10 → 15 km" | `RADIUS_STEPS_KM = [5, 10, 15, 20]` — cuatro pasos, llega a 20 km |
| "si ningún chofer acepta en los primeros 2 minutos" | `OFFER_TTL_SECONDS = 30` — 30 segundos por oferta |
| "cron cada 1 minuto" | `@Cron('*/15 * * * * *')` — cada 15 segundos |
| "si supera el máximo de intentos, notifica al administrador" | **No existe.** No hay máximo de intentos ni aviso al admin |

La última es la más riesgosa: describe una funcionalidad no implementada. El
comentario del código dice lo contrario de forma explícita — *"Best-effort: si
no hay candidatos, no hace nada (el cron reintentará cuando aparezcan
choferes)"*. El reintento es indefinido mientras el pedido siga pendiente.

Corregir esto es independiente de la decisión sobre los módulos.
