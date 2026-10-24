# Guía de los diagramas de interacción de diseño (DSD) en estilo Larman

Cómo se dibuja un DSD de SPLG. La plantilla de Diseño de la cátedra pide, por cada caso de
uso, un diagrama de interacción **por operación del sistema** («Operación: nombre(params)»), y
el tribunal lee la notación de Larman (*UML y patrones*). Los modelos hechos son CU-005
(`crearPedido`), CU-025 (`resolverReclamo`), CU-166 (`tomarReclamo`), CU-012
(`asignarChoferAPedido`) y, planificado, CU-122 (`agregarItemAlCarrito`): se copian, no se
reinventan.

## 1. La unidad: una operación, un diagrama

- Un diagrama por cada par (caso de uso, operación del sistema) del catálogo
  `operaciones-sistema.json`. Un caso con dos operaciones lleva dos diagramas.
- Archivo: `diagramas/DSD_CU-xxx_<operacion>.mmd`, con el nombre exacto de la operación del
  catálogo. Si el catálogo la lista en varios casos, un solo archivo los nombra a todos, en el
  orden del catálogo: `DSD_CU-005_CU-044_crearPedido.mmd`. El diagrama vive en el primer caso;
  en los otros se deja una línea «Operación X: ver el DSD de CU-005».
- Título: `title DSD — CU-025 Resolver Reclamo · resolverReclamo` (con varios casos:
  `DSD — CU-005 / CU-044 · crearPedido`, sin nombre).
- En los documentos (Doc 3 §4 y `Casos-de-Uso.md`) el bloque es: encabezado del caso,
  `##### Operación: firma`, el diagrama, el epígrafe de figura (sólo Doc 3), el párrafo de
  clases participantes y la tabla de implementación (§7).

**Idiomas.** Los objetos del dominio llevan el nombre castellano del modelo conceptual (`Pedido`, `Cliente`); las fabricaciones puras, los puertos y los servicios de infraestructura llevan su nombre real (`NotificationPort`, `OrderPricingService`), porque no pertenecen al modelo conceptual. Un mismo diagrama mezcla los dos idiomas a propósito, y el Documento 3 (§4) lo explica.

## 2. Primer mensaje y Controlador

El primer mensaje sale del actor (`actor ADM as Administrador (ACT-03)`, igual que en el DSS) y
lleva la **firma exacta del catálogo**: `resolverReclamo(reclamoId, resolucion, estadoFinal)`.

Llega al **controlador de aplicación**, con su nombre real: el `…UseCase` si el módulo tiene uno
para esa operación (`:CreateOrderUseCase`), si no el servicio fachada del módulo
(`:ClaimsService`, `:OrderService`). Criterio: es el primer objeto detrás de la interfaz que
representa el caso de uso o el subsistema (Larman, patrón Controlador) y es el que el código
ya usa para orquestar. No se dibujan los `…Controller` de Nest (son la interfaz HTTP del
actor), ni guards, pipes, interceptores, DTO, mappers, `QueryRunner` ni `DataSource`. Un objeto
de dominio no es controlador. Si el controlador acumula demasiada lógica, se baja a Experto.

## 3. Participantes

Etiqueta de objeto, siempre con dos puntos: `participant REC as reclamo:Reclamo` o
`participant SRV as :ClaimsService`.

| Qué | Cómo | Ejemplo |
|---|---|---|
| Objeto de dominio | clase del modelo conceptual (nombres en castellano) | `:Pedido`, `:ItemPedido`, `producto:Producto` |
| Controlador y fabricaciones puras | clase real del código | `:OrderPricingService`, `:PaymentsService` |
| Puertos y repositorios | sólo si el código los usa y son fabricación pura justificada | `:DispatchOfferRepositoryPort` |
| Colección | `Map` o `List` del dominio; en Mermaid va `#lt;` y `#gt;` | `:Map#lt;String, Reclamo#gt;` |

**Tope: 8 líneas de vida (el actor cuenta); el verificador avisa a partir de 10.** Un DSD con
la mitad de servicios es una traza del código, no un diseño. Reglas para no pasarse:

- **La navegación va por los objetos de dominio y las asociaciones del modelo conceptual**, no
  por servicios de búsqueda: `cliente:Cliente` → `getDireccion(id)`; `zona:ZonaCobertura` →
  `cubre(direccion)`; `franja:FranjaHoraria` → `tieneCupo(fecha)`; `producto:Producto` →
  `reservar(cantidad)`. El servicio que el código usa para llegar a cada uno se declara en la
  tabla de implementación (§7), no se dibuja.
- Los servicios, puertos y repositorios sólo aparecen como **fabricación pura justificada**:
  pasarela de pago, notificador, despacho, colección (`:Map#lt;String, Reclamo#gt;` cuando hay
  que buscar por identificador y no hay otro objeto desde el cual navegar).
- Un subproceso largo que es **otra operación del catálogo** (el pago con MercadoPago, la oferta
  al chofer) no se despliega: va una nota `Note over A,B: Pago: ver DSD de crearCheckoutDePago
  (CU-048)` y su propio diagrama. Mermaid no tiene marco `ref`; la nota cumple ese papel. Si la
  postcondición del contrato la realiza ese subproceso, la nota nombra la clase («Crea la
  OfertaDespacho») y el verificador la da por realizada.
- La persistencia (guardar, transacción, bloqueo) **no se dibuja**: se declara en el párrafo de
  clases participantes.

## 4. GRASP visible

- **Experto**: el que tiene el dato responde. `:Pedido` → `calcularTotal()` → `:ItemPedido` →
  `getSubtotal()`.
- **Creador**: crea el que contiene o agrega (composición `*` del modelo conceptual); la parte
  nunca la crea otro. `:Pedido` crea sus `:ItemPedido`; `:Cliente` crea su `:Carrito`. El
  controlador puede crear el agregado raíz que inicializa con los datos de la operación.
- **Controlador**: ver §2. **Bajo Acoplamiento y Alta Cohesión**: la lógica de cálculo
  transversal o de infraestructura vive en una fabricación pura (`OrderPricingService`), no en
  el objeto de dominio ni en el controlador.
- **Asignar estado = mensaje al experto.** Nunca `reclamo.estado igual X`: se manda
  `reclamo:Reclamo` ← `resolver(resolucion, estadoFinal)`; si la regla de transición es suya,
  `reclamo` se manda `validarTransicion(estadoFinal)` a sí mismo.

## 5. Notación Mermaid

Probado en mermaid-cli 12 y en el 10.9.1 que carga el sitio.

```
sequenceDiagram
    title DSD — CU-025 Resolver Reclamo · resolverReclamo
    autonumber
    actor ADM as Administrador (ACT-03)
    participant SRV as :ClaimsService
    participant REC as reclamo:Reclamo
    ADM->>+SRV: resolverReclamo(reclamoId, resolucion, estadoFinal)
    SRV->>+REC: resolver(resolucion, estadoFinal)
    REC->>REC: validarTransicion(estadoFinal)
    deactivate REC
    SRV-->>-ADM: reclamo
```

| Elemento | Sintaxis |
|---|---|
| Creación | `create participant PED as :Pedido` y, justo después, `CRT->>PED: «create»(cliente, direccion)` |
| Destrucción | `destroy PED` y `CRT-xPED: «destroy»` (casi nunca hace falta) |
| Activación | `->>+` abre y `-->>-` cierra; `deactivate X` si no hay retorno |
| Retorno punteado `-->>` | sólo cuando el valor lo usa un mensaje posterior (`cliente`, `total`) y en el cierre hacia el actor |
| Mensaje asíncrono | `CRT-)NOT: sendOrderConfirmation(cliente, pedido)` |
| Fragmentos | `alt metodoDePago es MERCADOPAGO` / `else efectivo` / `end`, `opt`, `loop Por cada item de items`; la guarda va **sin corchetes** (Mermaid los agrega) |
| Numeración | `autonumber` siempre |
| Notas | `Note over A,B: texto`, cortas; una nota ancha estira el diagrama |

Los argumentos son de diseño (`pedido`, `cliente`), no ids de HTTP. Sin `=`, `:=` ni «igual» en
un mensaje.

## 6. Coherencia con el contrato

Cada postcondición del contrato (Doc 2 §2.2) se ve realizada por un mensaje:

| Postcondición | Mensaje |
|---|---|
| «Se creó una instancia de Pedido» | `«create»` a `:Pedido` |
| «Se creó una asociación Pedido–Chofer» | el mensaje que la forma, `asignarChofer(chofer, vehiculo)` |
| «El atributo estado de Reclamo pasó a…» | un mensaje al `:Reclamo` (`resolver`) |
| «Se notificó al Cliente» | un mensaje al puerto de notificación |

Las excepciones del contrato van como `alt` sólo si cambian qué objetos participan; si no,
quedan en el DSS y en el párrafo de clases.

## 7. Relación con el código: la tabla de implementación

Si el código implementa la operación de diseño con otro nombre, otra clase o inline en un
servicio, se dice, para no inventar ni ocultar. Después del diagrama, en Doc 3 y en
`Casos-de-Uso.md`:

```
**Clases participantes:** … **GRASP.** … **No se dibuja:** …

| Operación de diseño | Implementación |
|---|---|
| `Reclamo.resolver(...)` | `ClaimsService.resolve`: asigna `Claim.resolutionNote` y `Claim.status` |
```

- Una fila por cada mensaje cuya clase y operación **no** coincidan con un método del código. Los
  objetos de dominio siempre llevan fila (la clase `Pedido` es la entidad `Order`).
- La columna de la izquierda es `Clase.operacion(...)`, o `Clase.«create»`. Los símbolos de la
  derecha van entre comillas simples: `Clase.metodo`, `Clase.atributo` o `funcion()`; el cruce
  los busca en `src/`.
- Una operación que el código tiene con ese nombre y clase no lleva fila.
- **Planificados** (estado «Planificado» en el catálogo): mismo estilo, sin tabla; el párrafo
  dice «colaboración propuesta» y las clases `CartService` y similares son las de
  `PROPUESTAS_CLASE` (`dsd_larman.py`).

## 8. Qué pasa con los DSD viejos y con el cruce

- Los `.mmd`, PNG y SVG de traza de cada caso rehecho se borran con `git rm` (quedan en el
  historial): `git rm diagramas/DSD_CU-025_Resolver-Reclamo.mmd`, ídem `diagramas/png/…png` y
  `diagramas/svg/…svg`.
- Los tres lugares (`.mmd`, `3-Diseño.md` §4 o su caso, `Casos-de-Uso.md`) llevan el mismo
  bloque, byte a byte.
- El cruce `cruzar-dsd-clases.py` ya no compara trazas con el código: lee las clases de diseño
  que salen de los DSD (clase y operaciones recibidas, el DC de diseño) y las contrasta con el
  código **a través de la tabla** (§7). Los DSD viejos siguen bajo las reglas anteriores hasta
  que se rehacen.
- Hay que correr `python3 herramientas/numerar-figuras.py --aplicar` para el epígrafe y el índice de figuras.

## 9. Cómo se verifica

```
python3 herramientas/verificar-dsd-larman.py             # informa lo que falta
python3 herramientas/verificar-dsd-larman.py --estricto  # falla por cada operación sin DSD
python3 herramientas/verificar-dsd-larman.py DSD_CU-025_resolverReclamo.mmd
python3 herramientas/cruzar-dsd-clases.py
python3 herramientas/renderizar-dsd.py --sitio diagramas/DSD_CU-025_resolverReclamo.mmd
```

`verificar-dsd-larman.py` (reglas en `dsd_larman.py`) comprueba, por cada DSD en estilo Larman:
nombre y casos del archivo contra el catálogo; título; `autonumber`; primer mensaje = firma
exacta de una operación del catálogo, desde el actor del catálogo, a un controlador de
aplicación; participantes `:Clase` permitidos (modelo conceptual, código o planificadas), sin
infraestructura (avisa si hay más de 9 líneas de vida); sin asignaciones como mensaje; `«create»` con `create participant` y la parte
creada por su todo; al menos un objeto de dominio si la operación cambia estado; cada instancia
creada o modificada que dice la postcondición, realizada; el bloque idéntico en los dos
documentos y la tabla de implementación. Además informa las operaciones del catálogo sin DSD;
el gate (`verificar-conformidad.py`) no falla por ellas hasta correr con `DSD_ESTRICTO=1`, que
es lo que se activa al cerrar la reescritura.

`renderizar-dsd.py` genera el SVG y el PNG (tema neutral, fondo blanco, escala 2, tamaño
natural) y, con `--sitio`, comprueba que el diagrama dibuja con el Mermaid del sitio.
